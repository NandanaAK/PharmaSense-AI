from scripts.llm_client import call_llm
from scripts.sql_tool import run_sql_query


def trial_data_agent(question):
    """
    Trial Data Analyst Agent

    Uses the SQL tool to retrieve clinical trial data,
    then asks Gemini to analyze the retrieved data.
    """

    # SQL query for low-enrollment trials
    query = """
    SELECT
        trial_id,
        compound_id,
        trial_phase,
        therapeutic_area,
        target_enrollment,
        actual_enrollment,
        ROUND(
            actual_enrollment * 100.0
            / target_enrollment,
            2
        ) AS enrollment_percentage
    FROM clinical_trials
    WHERE actual_enrollment < target_enrollment * 0.60
    ORDER BY enrollment_percentage;
    """

    # Retrieve data from DuckDB
    sql_result = run_sql_query(query)

    # Convert DataFrame to readable text
    sql_result_text = sql_result.to_string(index=False)

    # Create prompt for Gemini
    prompt = f"""
You are the Trial Data Analyst Agent for PharmaSense AI.

Your job is to analyze structured clinical trial data.

User question:
{question}

Structured data retrieved from the PharmaSense AI database:
{sql_result_text}

Instructions:
1. Answer the user's question using only the provided database data.
2. Do not invent missing information.
3. Explain the result clearly.
4. Mention important trial IDs, compound IDs, phases, enrollment numbers,
   and enrollment percentages when relevant.
5. If multiple trials match the question, mention the relevant trials.
6. If the data is insufficient to answer the question, clearly say so.
"""

    # Ask Gemini to analyze the SQL result
    response = call_llm(prompt)

    return response


if __name__ == "__main__":

    question = "Which clinical trials have low enrollment?"

    result = trial_data_agent(question)

    print("\nTrial Data Analyst Agent Response:")
    print("=" * 60)
    print(result)