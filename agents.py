from crewai import Agent
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL
from web_search import WebSearchTool  # Import the new tool

# Initialize LLM
llm = ChatOpenAI(
    model="deepseek-r1:1.5b",
    base_url=OLLAMA_BASE_URL
)

# Initialize web search tool
web_search_tool = WebSearchTool()

# Define agents

researcher = Agent(
    role="Research Analyst",
    goal="Gather and verify comprehensive, relevant, and up-to-date information on {topic}.",
    backstory="You are a research analyst skilled in finding and validating factual information from multiple sources.",
    tools=[web_search_tool],  # Now properly formatted as a CrewAI tool
    llm=llm,
    verbose=True
)

analyst = Agent(
    role="Insights Analyst",
    goal="Analyze and interpret research findings on {topic}.",
    backstory="You extract key insights from research data and synthesize meaningful conclusions.",
    llm=llm,
    verbose=True
)

summarizer = Agent(
    role="Knowledge Synthesizer",
    goal="Create a structured, clear, and well-supported summary of research findings on {topic}.",
    backstory="You distill complex research into structured summaries with clarity and precision.",
    llm=llm,
    verbose=True
)