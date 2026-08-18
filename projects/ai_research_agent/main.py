"""main script for ai research agent"""
import asyncio
from dotenv import load_dotenv
from agents import trace
from src.agents.search.search_agent import SearchAgent
from src.agents.planner.planner_agent import PlannerAgent
from src.agents.email.emailer_agent import EmailerAgent
from src.agents.writer.writer_agent import WriterAgent
from src.agents.planner.planner_config import WebSearchItem
from src.agents.writer.writer_config import ReportData

load_dotenv(override=True)

search_agent = SearchAgent()
planner_agent = PlannerAgent()
emailer_agent = EmailerAgent()
writer_agent = WriterAgent()

async def search(item: WebSearchItem):
    input_message = f"Search term: {item.query} \n Reason for searching: {item.reason}"
    result = await search_agent.agentic_search(input_message)
    return result

async def run_searches(query: str):
    print("Planning searches...")
    searches = await planner_agent.agentic_plan(query)
    print(f"Will perform {len(searches)} searches")
    tasks = [search(item) for item in searches]
    results = await asyncio.gather(*tasks)
    print("Finished searching")
    return results

async def write_report(query: str, search_result: list[str]):
    print("Thinking about report...")
    input_message = f"Original query: {query}\nSummarized search results: {search_result}"
    result = await writer_agent.agentic_write(input_message)
    print("Finished writing report")
    return result

async def send_report_email(report: ReportData):
    print("Writing email...")
    result = await emailer_agent.agentic_send(report.markdown_report)
    print("Email sent")
    return result


async def main():
    query = "Most popular AI Agent frameworks in 2026"

    with trace("Research trace"):
        print("Starting research...")
        search_results = await run_searches(query)
        report = await write_report(query, search_results)
        await send_report_email(report)
        print("Hooray!")

if __name__ == "__main__":
    asyncio.run(main())
