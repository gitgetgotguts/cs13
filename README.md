# LinkedIn Job Scraper

A simple, standalone Python script that scrapes job listings from LinkedIn.

## What it Does

*   Asynchronously scrapes all job listings for a given search query and location.
*   Saves the results to a dynamically named JSON file (e.g., `YYYYMMDD_HHMMSS_location_keyword.json`).

## How to Use

### 1. Setup

*   Ensure you have a `utils.py` file in the same directory containing the `parse_job_card` function.
*   Install the required libraries:
    ```bash
    pip install curl_cffi beautifulsoup4
    ```

### 2. Configure

*   Open the main script and change the `LOCATION` and `SEARCH_KEYWORDS` variables at the top to your desired search.

    ```python
    LOCATION = "Canada"
    SEARCH_KEYWORDS = "Data Scientist"
    ```

### 3. Run

*   Execute the script from your terminal:
    ```bash
    python full.py
    ```

## Output

A JSON file containing a list of all found jobs will be created in the same directory. The file will be named using the timestamp, location, and keywords from your search.


### An other script to scrape job details and merge data will be added soon Insha'Allah
this was made possible by JobSpy : https://github.com/speedyapply/JobSpy
