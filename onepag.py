from utils import parse_job_card

import asyncio
from curl_cffi.requests import AsyncSession
from bs4 import BeautifulSoup, Tag
import logging
import time
import sys
from datetime import datetime
import json
LOCATION = "egypt"
SEARCH_KEYWORDS = "data engineer"

logger = logging.getLogger(__name__)
JOB_SEARCH_PAGE_URL = "https://www.linkedin.com/jobs/search"
JOB_SEARCH_API_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"


async def get_job_desc(session, job_link):
    try:
        response = await  session.get(
            f"https://www.linkedin.com/jobs/view/{job_link.split('-')[-1]}", timeout=5
        )
    except:
        return None
    if "linkedin.com/signup" in response.url:
        return None


    soup = BeautifulSoup(response.text, "html.parser")
    description_text = None
    description_div = soup.find("div", class_="description__text")
    if description_div:
        description_text = description_div.get_text(separator='\n', strip=True)

    job_function = None
    h3_tag = soup.find("h3", string=lambda text: text and "Job function" in text.strip())
    if h3_tag:
        span_tag = h3_tag.find_next("span")
        if span_tag:
            job_function = span_tag.text.strip()

    return {
        "description": description_text,
       "job_function": job_function,
    }
async def main(location=LOCATION, keywords=SEARCH_KEYWORDS):
    session = AsyncSession(impersonate="chrome120")
    logger.info(f"Starting LinkedIn job search for '{keywords}' in '{location}'...")

    prime_params = {'keywords': keywords, 'location': location}
    logger.info("Warming up session to acquire necessary cookies...")
    await session.get(JOB_SEARCH_PAGE_URL, params=prime_params)


    start=0
    job_list=[]
    page_num=1
    while 1:
        logger.info(f"Fetching page {page_num} (starting at index {start})...")
        prime_params.update({'start': start})
        api_response = await session.get(JOB_SEARCH_API_URL, params=prime_params)

        if api_response.status_code==400: break
        else:
            start+=10
            page_num+=1

        soup = BeautifulSoup(api_response.text, 'html.parser')
        job_cards = soup.find_all("div", class_="base-search-card")

        all_jobs = [parse_job_card(card) for card in job_cards]
        print("getting job descriptions...")

        for job in all_jobs:
            if job['job_url']:
                desc_data = await get_job_desc(session, job['job_url'])
                if desc_data:
                    job.update(desc_data)
                time.sleep(0.5)
        job_list.extend(all_jobs)
        if page_num>=1:
            break

        logger.info(f"Found {len(all_jobs)} jobs on this page.")
        if len(all_jobs)==0: break
        time.sleep(0.7)
    logger.info("Scraping complete.")
    return job_list



if __name__ == "__main__":
    # Configure the logging system
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
    )

    found_jobs = asyncio.run(main())

    print(f"Total jobs found: {len(found_jobs)}")

    # --- SAVE TO JSON LOGIC ---
    if not found_jobs:
        logger.warning("No jobs found, JSON file will not be created.")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{LOCATION}_{SEARCH_KEYWORDS.replace(' ', '_')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(found_jobs, f, ensure_ascii=False, indent=4)

            logger.info(f"Successfully saved results to {filename}")
        except Exception as e:
            logger.error(f"An error occurred while saving the JSON file: {e}")

