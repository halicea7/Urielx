from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
import logging
from datetime import datetime
from config import OLLAMA_BASE_URL

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG to capture more detailed information
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('research_summary.log', mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    model = "deepseek-r1:32b",
    base_url = OLLAMA_BASE_URL
)

# Log LLM initialization
logger.info("Initializing LLM with model: deepseek-r1:32b")

planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic} in 'https://medium.com/'."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "You have to prepare a detailed "
              "outline and the relevant topics and sub-topics that has to be a part of the"
              "blogpost."
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    llm=llm,
    allow_delegation=False,
 verbose=True
)
logger.debug("Content Planner agent created successfully")

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic} in 'https://medium.com/'. "
              "You base your writing on the work of "
              "the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provide by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)
logger.debug("Content Writer agent created successfully")

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization 'https://medium.com/'. ",
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)
logger.debug("Editor agent created successfully")

plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)
logger.debug("Research task created successfully")

write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
  "3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)
logger.debug("Analysis task created successfully")

edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    agent=editor
)
logger.debug("Summary task created successfully")

# Log crew creation
logger.info("Creating and configuring crew")
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)
logger.debug("Crew created successfully")

inputs = {"topic":"Comparative study of LangGraph, Autogen and Crewai for building multi-agent system."}

try:
    logger.info(f"Starting research compilation for topic: {inputs['topic']}")
    logger.info("Initiating crew kickoff")
    result = crew.kickoff(inputs=inputs)
    logger.info("Crew tasks completed successfully")
    
    # Create output directory if it doesn't exist
    os.makedirs('research_outputs', exist_ok=True)
    logger.debug("Created/verified research_outputs directory")
    
    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'research_outputs/research_summary_{timestamp}.md'
    logger.debug(f"Generated output filename: {output_file}")
    
    # Save the result to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
        logger.debug(f"Written {len(result)} characters to output file")
    
    logger.info(f"Research summary successfully generated and saved to {output_file}")
    logger.debug("Printing result to console")
    print(result)

except Exception as e:
    logger.error(f"An error occurred: {str(e)}")
    logger.exception("Detailed error information:")  # This logs the full stack trace
    raise

finally:
    logger.info("Script execution completed")