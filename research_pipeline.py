import os
from datetime import datetime
from crewai import Crew
from tasks import research, analyze, summarize
from agents import researcher, analyst, summarizer
from logger_config import logger

# Initialize Crew with agents and tasks
crew = Crew(
    agents=[researcher, analyst, summarizer],
    tasks=[research, analyze, summarize],
    verbose=2
)

def run_research(topic):
    inputs = {"topic": topic}

    try:
        logger.info(f"Starting research compilation for topic: {topic}")
        logger.info("Initializing crew and starting tasks")

        result = crew.kickoff(inputs=inputs)

        # Create output directory
        os.makedirs('research_outputs', exist_ok=True)
        logger.info("Created research_outputs directory")

        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'research_outputs/research_summary_{timestamp}.md'

        # Save result to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        logger.info(f"Research summary saved to file: {output_file}")

        logger.info("Research process completed successfully")
        print(result)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        logger.error("Research process failed")
        raise

if __name__ == "__main__":
    topic = "Latest developments in quantum computing and its practical applications"
    run_research(topic)