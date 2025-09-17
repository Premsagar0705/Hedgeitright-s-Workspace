import requests
import csv
import time

# OpenCorporates API base
BASE_URL = "https://api.opencorporates.com/v0.4/companies/search"

# Search settings
params = {
    "q": "india",  # You can change this to any Indian keyword or name
    "jurisdiction_code": "sg",  # Singapore
    "current_status": "Live",  # Only live companies
    "per_page": 50,
    "page": 1
}

# Output CSV file
output_file = "indian_promoted_sg_companies.csv"

# CSV headers
headers = [
    "Company Name", "Company Number", "Jurisdiction",
    "Status", "Incorporation Date", "Registered Address", "OpenCorporates URL"
]

with open(output_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    while True:
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print("Error fetching data:", response.status_code)
            break

        data = response.json()
        companies = data.get("results", {}).get("companies", [])
        if not companies:
            break

        for entry in companies:
            company = entry["company"]
            row = [
                company.get("name"),
                company.get("company_number"),
                company.get("jurisdiction_code"),
                company.get("current_status"),
                company.get("incorporation_date"),
                company.get("registered_address", "N/A"),
                f"https://opencorporates.com/companies/{company.get('jurisdiction_code')}/{company.get('company_number')}"
            ]
            writer.writerow(row)

        print(f"✅ Page {params['page']} completed with {len(companies)} companies.")
        if params["page"] >= data["results"]["total_pages"]:
            break

        params["page"] += 1
        time.sleep(1)  # Be polite to the API
