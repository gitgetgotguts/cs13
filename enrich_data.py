from openai import OpenAI  # Or your preferred LLM library
import pandas as pd
import json
import re
import os
from tenacity import retry, stop_after_attempt, wait_random_exponential
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
# THIS SCRIPT TAkes a dataset created by the full script and adds colums : 'match_context', 'hard_skills', 'domain_keywords', 'job_title', 'required_min_years' to the dataset using an LLM
filename='20251103_200732_tunisia_data_science.json'
client = OpenAI(base_url="https://api.llm7.io/v1",api_key="4LPcl/IAgbPijsDc3iQXFSSYy9Mb1Xj1ieIZnRb1ZDtzNDW0Kmwisz7mphyed3oN+srfcqMqx2PnbOc19cvE0TgJE02HeZgndZPxUU5haEVpOCKj0Fq3xTrUZaSirYgxUSE=")
df = pd.read_json(filename)


JOB_EXTRACTION_PROMPT ='''You are a seasoned Principal Engineer acting as a hiring manager. Your task is to review a job description and distill it into a structured JSON object for an internal recruiting tool. Your primary goal is to identify the true, non-negotiable technical requirements.

Your response must be ONLY the valid JSON object.

---
### **JSON SCHEMA,Instructions AND GUIDELINES**


{
  "match_context": "string",
  "hard_skills": ["string"],
  "domain_keywords": ["string"],
  "job_title": "string",
  "required_min_years": "integer | null"
}

*   **`match_context`**:
    *   In your own words as an engineer, write a brief, 3-4 sentence summary of the role's mission and key responsibilities.
    *   **Focus on the actions and business outcomes** (e.g., 'modernizing data platforms,' 'enabling real-time analytics').
    *   **Do not list specific technologies or tools in this summary.**

*   **`mandatory_hard_skills`**:
    *   As a hiring manager, identify the absolute **"deal-breaker"** technologies. This list should be very short (typically 2-5 skills).
    *   Use strong signals like **"Proficient in"** and **"Hands-on experience with"** to find the lines containing the true requirements.
    *   **CRITICAL FORMATTING RULE:** The final list must contain **ONLY the technology name itself.** For example, if the text says "Proficient in SQL", the value in the list must be `"SQL"`, not `"Proficient in SQL"`.
    *   If the description offers a choice (e.g., "AWS or Azure"), represent it as a single string with a pipe separator (e.g., "AWS | Azure").
    *   Use your expert judgment to distinguish a true requirement from a 'wishlist' of examples.

*   **`nice_to_have_hard_skills`**:
    *   List any technologies that are explicitly mentioned as "preferred," "a plus," or "nice to have," listing only the technology name.

*   **`domain_keywords`**:
    *   List the key business or process-related terms that define the role's environment.

*   **`job_title`**:
    *   Extract the primary job title for the role.
*   **`required_min_years`**:
    *   Extract the minimum years of experience as an integer. If not specified, return null.

ABSOLUTELY CRITICAL - READ THIS CAREFULLY:
1. NO markdown formatting whatsoever
2. NO ```json or ``` in your response
3. Start with "{{" and end with "}}"
---

### **BEGIN REVIEW**

Review the following job description and produce the JSON object.

**Job Description Text:**'''
ERROR_STRUCTURE = {
    "match_context": None,
    "hard_skills": [],
    "domain_keywords": [],
    "job_title": None,
    "required_min_years": None
}



# --- 3. Define the Robust LLM Worker Function ---
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def get_structured_job_data(description: str) -> dict:
    """Takes a job description string and returns a structured dictionary."""
    if not isinstance(description, str) or not description.strip():
        return ERROR_STRUCTURE
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-pro", # Use a model that's good at following JSON instructions
            messages=[
                {"role": "user", "content": JOB_EXTRACTION_PROMPT + description}
            ],
            response_format={"type": "json_object"} # Enforce JSON output
        )
        content = response.choices[0].message.content
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            return ERROR_STRUCTURE
    except Exception as e:
        # Catching any exception during the API call or parsing
        print(f"A single request failed with error: {e}")
        return ERROR_STRUCTURE
def main():
    texts_to_process = df["description"].fillna('').tolist()
    results_list = [None] * len(texts_to_process)
    MAX_CONCURRENT_REQUESTS=5
    print(f"\nStarting parallel data extraction for {len(texts_to_process)} descriptions...")
    print(f"Using up to {MAX_CONCURRENT_REQUESTS} concurrent workers.")

    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
        future_to_index = {executor.submit(get_structured_job_data, text): i for i, text in enumerate(texts_to_process)}

        for future in tqdm(as_completed(future_to_index), total=len(texts_to_process), desc="Processing in parallel"):
            index = future_to_index[future]
            try:
                results_list[index] = future.result()
            except Exception as e:
                print(f"A task generated an exception: {e}")
                results_list[index] = ERROR_STRUCTURE

    print("\nParallel processing complete. Integrating results into the DataFrame...")

    # --- 5. Unpack and Join Results ---
    extracted_df = pd.json_normalize(results_list)

    # MODIFIED: No need to clean column names, as the schema is already flat.
    # The `json_normalize` function will create the columns we want directly.

    # Join the new structured data with the original DataFrame
    final_df = df.join(extracted_df)
    OUTPUT_CSV_PATH=f"enriched_{filename.split('.')[0]}.csv"
    # --- 6. Save the Final, Enriched Dataset ---
    try:
        final_df.to_csv(OUTPUT_CSV_PATH, index=False)
        print(f"✅ Successfully saved enriched data to: {OUTPUT_CSV_PATH}")
        print("\nFinal DataFrame columns:", final_df.columns.tolist())
    except Exception as e:
        print(f"❌ ERROR: Failed to save the new CSV file. Reason: {e}")

main()