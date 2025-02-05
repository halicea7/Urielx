from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from config import OLLAMA_BASE_URL

# Initialize tools
search_tool = DuckDuckGoSearchRun()

# Initialize LLM
llm = ChatOpenAI(
    model="deepseek-r1:1.5b",
    base_url=OLLAMA_BASE_URL
)

# Define agents
researcher = Agent(
    role="Research Analyst",
    goal="Conduct comprehensive research on {topic} using web searches",
    backstory="You're a thorough research analyst skilled at finding and validating information from multiple sources. "
              "You focus on gathering factual, up-to-date information and identifying key trends and insights.",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze and synthesize research findings on {topic}",
    backstory="You're an analytical expert who excels at organizing information, identifying patterns, "
              "and drawing meaningful conclusions from research data. You ensure all findings are well-supported by evidence.",
    llm=llm,
    verbose=True
)

summarizer = Agent(
    role="Research Summarizer",
    goal="Create a clear, concise summary of the research findings",
    backstory="You're skilled at distilling complex information into clear, actionable insights. You focus on "
              "presenting findings in a structured, readable format with proper citations and evidence.",
    llm=llm,
    verbose=True
)
