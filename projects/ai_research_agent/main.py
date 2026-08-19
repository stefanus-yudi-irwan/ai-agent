"""main script for ai research agent"""
import asyncio
from loguru import logger
from agents import trace, function_tool
from dotenv import load_dotenv
from config.config import load_config
from src.agents.config.agent import AgentConfig
from src.agents.planner.agent import PlannerAgent
from src.agents.planner.model import WebSearchItem
from src.agents.search.agent import SearchAgent
from src.agents.writer.agent import WriterAgent
from src.agents.writer.model import ReportData
from src.agents.email.agent import EmailerAgent
from src.tools.search_tavily.tavily import TavilyWebSearch
from src.tools.search_tavily.config import TavilyWebSearchConfig, TavilySearchDepth
from src.tools.search_tavily.model import TavilySearchResult
from src.tools.email_smtp.smtp import SMTPEmailSender
from src.tools.email_smtp.config import SMTPSenderConfig
from src.tools.email_smtp.model import SMTPResponse

load_dotenv(override=True)
app_config = load_config("config/config.yaml")

tavily = TavilyWebSearch(
    config = TavilyWebSearchConfig(
        api_key = app_config.tool.search.TAVILY_API_KEY,
        search_depth = TavilySearchDepth.BASIC
    ))

smtp = SMTPEmailSender(
    config = SMTPSenderConfig(
        smtp_server = app_config.tool.email.EMAIL_SMTP_SERVER,
        app_password = app_config.tool.email.EMAIL_APP_PASSWORD,
        sender_email = app_config.tool.email.EMAIL_ADDRESS_SENDER,
        receiver_email = app_config.tool.email.EMAIL_ADDRESS_RECEIVER
    ))

planner_agent = PlannerAgent(
    config = AgentConfig(
        name = app_config.agent.planner.name,
        instructions = app_config.agent.planner.instructions,
        model = app_config.agent.planner.model
    ))

search_agent = SearchAgent[TavilySearchResult](
    config = AgentConfig(
        name = app_config.agent.searcher.name,
        instructions = app_config.agent.searcher.instructions,
        model = app_config.agent.searcher.model
    ), tool = function_tool(tavily.search))

writer_agent = WriterAgent(
    config = AgentConfig(
        name = app_config.agent.writer.name,
        instructions = app_config.agent.writer.instructions,
        model = app_config.agent.writer.model
    ))

emailer_agent = EmailerAgent[SMTPResponse](
    config = AgentConfig(
        name = app_config.agent.emailer.name,
        instructions = app_config.agent.emailer.instructions,
        model = app_config.agent.emailer.model
    ), tool = function_tool(smtp.send))

async def search(item: WebSearchItem):
    input_message = f"Search term: {item.query} \n Reason for searching: {item.reason}"
    result = await search_agent.search(input_message)
    return result

async def run_searches(query: str):
    logger.info("PLANNING SEARCH")
    searches = await planner_agent.plan(query)
    logger.info(f"WILL PERFORM {len(searches)} SEARCHES")
    tasks = [search(item) for item in searches]
    results = await asyncio.gather(*tasks)
    logger.info("FINISHED SEARCHING")
    return results

async def write_report(query: str, search_result: list[str]):
    logger.info("THINKING ABOUT REPORT")
    input_message = f"Original query: {query}\nSummarized search results: {search_result}"
    result = await writer_agent.write(input_message)
    logger.info("FINISHED WRITING REPORT")
    return result

async def send_report_email(report: ReportData):
    logger.info("WRITING EMAIL")
    result = await emailer_agent.send(report.markdown_report)
    logger.info("EMAIL SENT")
    return result

async def main():
    query = "Most popular AI Agent frameworks in 2026"

    with trace("Research trace"):
        logger.info("STARTING RESEARCH")
        search_results = await run_searches(query)
        report = await write_report(query, search_results)
        await send_report_email(report)
        logger.success("HOORAY!!")

if __name__ == "__main__":
    asyncio.run(main())