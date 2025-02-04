from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
import os
import logging
from datetime import datetime
from config import OLLAMA_BASE_URL

# Set up logging configuration
log_directory = 'logs'
os.makedirs(log_directory, exist_ok=True)

# Force clear any existing handlers to avoid duplicate logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_directory, 'research_summary.log'), mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add initial log entry to verify logging is working
logger.info("Logging system initialized")

# Initialize tools
search_tool = DuckDuckGoSearchRun()

os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    model="deepseek-r1:32b",
    base_url=OLLAMA_BASE_URL
)

researcher = Agent(
    role="Research Analyst",
    goal="Conduct comprehensive research on {topic} using web searches",
    backstory="You're a thorough research analyst skilled at "
              "finding and validating information from multiple sources. "
              "You focus on gathering factual, up-to-date information "
              "and identifying key trends and insights.",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze and synthesize research findings on {topic}",
    backstory="You're an analytical expert who excels at "
              "organizing information, identifying patterns, "
              "and drawing meaningful conclusions from research data. "
              "You ensure all findings are well-supported by evidence.",
    llm=llm,
    verbose=True
)

summarizer = Agent(
    role="Research Summarizer",
    goal="Create a clear, concise summary of the research findings",
    backstory="You're skilled at distilling complex information "
              "into clear, actionable insights. You focus on "
              "presenting findings in a structured, readable format "
              "with proper citations and evidence.",
    llm=llm,
    verbose=True
)

research = Task(
    description=(
        "1. Conduct thorough web searches on {topic}.\n"
        "2. Gather information from reliable sources.\n"
        "3. Document key findings with sources.\n"
        "4. Identify main themes and trends.\n"
        "5. Note any conflicting information or debates in the field."
    ),
    expected_output="A detailed research document with findings "
                    "and sources for each key point.",
    agent=researcher
)

analyze = Task(
    description=(
        "1. Review all research findings.\n"
        "2. Identify patterns and relationships.\n"
        "3. Evaluate the reliability of sources.\n"
        "4. Compare and contrast different viewpoints.\n"
        "5. Draw evidence-based conclusions."
    ),
    expected_output="An analytical report highlighting key insights, "
                    "patterns, and supported conclusions.",
    agent=analyst
)

summarize = Task(
    description=(
        "1. Create a structured summary of all findings.\n"
        "2. Highlight key conclusions and insights.\n"
        "3. Include relevant citations and sources.\n"
        "4. Organize information in a clear, logical manner.\n"
        "5. Add recommendations for further research if applicable."
    ),
    expected_output="A comprehensive research summary in markdown format, "
                    "including executive summary, key findings, "
                    "methodology, and citations.",
    agent=summarizer
)

crew = Crew(
    agents=[researcher, analyst, summarizer],
    tasks=[research, analyze, summarize],
    verbose=2
)

inputs = {"topic": "Latest developments in quantum computing and its practical applications"}

try:
    logger.info(f"Starting research compilation for topic: {inputs['topic']}")
    logger.info("Initializing crew and starting tasks")
    result = crew.kickoff(inputs=inputs)
    
    # Create output directory if it doesn't exist
    os.makedirs('research_outputs', exist_ok=True)
    logger.info("Created research_outputs directory")
    
    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'research_outputs/research_summary_{timestamp}.md'
    
    # Save the result to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    logger.info(f"Research summary saved to file: {output_file}")
    
    logger.info("Research process completed successfully")
    print(result)

except Exception as e:
    logger.error(f"An error occurred: {str(e)}", exc_info=True)
    logger.error("Research process failed")
    raise