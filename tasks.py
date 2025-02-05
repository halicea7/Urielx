from crewai import Task
from agents import researcher, analyst, summarizer

# Define tasks
research = Task(
    description=(
        "1. Conduct thorough web searches on {topic}.\n"
        "2. Gather information from reliable sources.\n"
        "3. Document key findings with sources.\n"
        "4. Identify main themes and trends.\n"
        "5. Note any conflicting information or debates in the field."
    ),
    expected_output="A detailed research document with findings and sources for each key point.",
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
    expected_output="An analytical report highlighting key insights, patterns, and supported conclusions.",
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
    expected_output="A comprehensive research summary in markdown format, including executive summary, key findings, methodology, and citations.",
    agent=summarizer
)
