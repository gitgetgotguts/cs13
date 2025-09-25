
def parse_job_card(job_card):
    href_tag = job_card.find("a", class_="base-card__full-link")
    job_url = href_tag["href"].split("?")[0] if href_tag else None
    job_id = job_url.split("-")[-1] if job_url else None

    title_tag = job_card.find("span", class_="sr-only")
    title = title_tag.get_text(strip=True) if title_tag else None

    company_tag = job_card.find("h4", class_="base-search-card__subtitle")
    company = company_tag.get_text(strip=True) if company_tag else None

    location_tag = job_card.find("span", class_="job-search-card__location")
    location = location_tag.get_text(strip=True) if location_tag else None

    datetime_tag = job_card.find("time", class_="job-search-card__listdate")
    date_posted = datetime_tag["datetime"] if datetime_tag and "datetime" in datetime_tag.attrs else None

    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "location": location,
        "date_posted": date_posted,
        "job_url": job_url,
    }
