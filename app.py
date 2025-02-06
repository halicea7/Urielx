import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from crewai import Crew
from tasks import research, analyze, summarize
from agents import researcher, analyst, summarizer
from logger_config import logger
from web_search import search_and_extract

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize Crew with agents and tasks
crew = Crew(
    agents=[researcher, analyst, summarizer],
    tasks=[research, analyze, summarize],
    verbose=2
)

def run_research(topic):
    """Runs the research process and returns results."""
    inputs = {"topic": topic}

    # Debugging: Test the search tool separately before running CrewAI
    logger.info(f"🧪 Testing WebSearchTool separately for topic: {topic}")
    print(f"🧪 Running test search for: {topic}")

    test_results = search_and_extract(topic, num_results=3)  # Test with 3 results
    if not test_results:
        logger.error("❌ Search tool returned no results!")
        print("❌ Search tool returned no results!")
        return {"status": "error", "error": "Search tool did not return any results"}

    logger.info("✅ Search tool test successful!")
    print(f"✅ Search Tool Results:\n{test_results}")

    try:
        logger.info(f"🚀 Starting CrewAI research for: {topic}")
        print(f"🚀 Running research pipeline for: {topic}")

        result = crew.kickoff(inputs=inputs)

        os.makedirs('research_outputs', exist_ok=True)  # Ensure output directory exists
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'research_outputs/research_summary_{timestamp}.md'

        # Extract only the "Final Answer" if the result is structured
        if isinstance(result, dict) and "Final Answer" in result:
            result_text = result["Final Answer"]
        else:
            result_text = str(result)

        # Save research summary to a file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result_text)

        logger.info(f"✅ Research summary saved: {output_file}")
        print(f"✅ Research summary saved: {output_file}")

        return {"status": "success", "rawOutput": result_text, "outputFile": output_file}

    except Exception as e:
        logger.error(f"❌ Error during execution: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        return {"status": "error", "error": str(e)}


@app.route('/run_research', methods=['POST'])
def run_research_route():
    """API endpoint for running research."""
    data = request.get_json()

    if not data or 'topic' not in data:
        return jsonify({"status": "error", "error": "Missing topic"}), 400

    topic = data['topic']
    result = run_research(topic)
    return jsonify(result)


if __name__ == '__main__':
    # Run Flask on port 5000
    app.run(debug=True, port=5000)
