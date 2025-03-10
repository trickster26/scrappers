import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set a common headers dictionary for all requests.
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_cognizant():
    url = "https://careers.cognizant.com/global/en"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors based on Cognizant's actual page structure
        for job in soup.select('.job-card'):  # example selector
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'Cognizant',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping Cognizant:", e)
    return jobs

def scrape_tcs():
    url = "https://www.tcs.com/careers"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors based on TCS career page
        for job in soup.select('.job-listing'):  # example selector
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'TCS',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping TCS:", e)
    return jobs

def scrape_infosys():
    url = "https://careers.infosys.com"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors based on Infosys' actual structure
        for job in soup.select('.job-card'):
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'Infosys',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping Infosys:", e)
    return jobs

def scrape_ibm():
    url = "https://www.ibm.com/employment/"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors for IBM careers
        for job in soup.select('.job-listing'):
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'IBM',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping IBM:", e)
    return jobs

def scrape_tech_mahindra():
    url = "https://careers.techmahindra.com"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors for Tech Mahindra
        for job in soup.select('.job-listing'):
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'Tech Mahindra',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping Tech Mahindra:", e)
    return jobs

def scrape_hcl():
    url = "https://www.hcltech.com/careers"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors for HCL Technologies
        for job in soup.select('.job-listing'):
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'HCL Technologies',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping HCL Technologies:", e)
    return jobs

def scrape_hpe():
    url = "https://careers.hpe.com"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors for HPE
        for job in soup.select('.job-card'):
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'HPE',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping HPE:", e)
    return jobs

def scrape_aditya_birla():
    url = "https://careers.adityabirla.com"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors for Aditya Birla Group
        for job in soup.select('.job-listing'):
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'Aditya Birla Group',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping Aditya Birla Group:", e)
    return jobs

def scrape_mccain():
    url = "https://www.mccain.com/careers"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors for McCain Foods
        for job in soup.select('.job-listing'):
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'McCain Foods',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping McCain Foods:", e)
    return jobs

def scrape_ajanta_pharma():
    url = "https://www.ajantapharma.com/careers"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors for Ajanta Pharma
        for job in soup.select('.job-card'):
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'Ajanta Pharma',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping Ajanta Pharma:", e)
    return jobs

def scrape_fingent():
    url = "https://www.fingent.com/careers"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors for Fingent
        for job in soup.select('.job-listing'):
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'Fingent',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping Fingent:", e)
    return jobs

def scrape_clarion():
    url = "https://www.clariontech.com/careers"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update selectors for Clarion Technologies
        for job in soup.select('.job-listing'):
            title = job.select_one('.job-title').get_text(strip=True)
            location = job.select_one('.job-location').get_text(strip=True)
            link = job.find('a')['href']
            jobs.append({
                'company': 'Clarion Technologies',
                'title': title,
                'location': location,
                'link': link
            })
    except Exception as e:
        print("Error scraping Clarion Technologies:", e)
    return jobs

def main():
    all_jobs = []
    all_jobs.extend(scrape_cognizant())
    all_jobs.extend(scrape_tcs())
    all_jobs.extend(scrape_infosys())
    all_jobs.extend(scrape_ibm())
    all_jobs.extend(scrape_tech_mahindra())
    all_jobs.extend(scrape_hcl())
    all_jobs.extend(scrape_hpe())
    all_jobs.extend(scrape_aditya_birla())
    all_jobs.extend(scrape_mccain())
    all_jobs.extend(scrape_ajanta_pharma())
    all_jobs.extend(scrape_fingent())
    all_jobs.extend(scrape_clarion())
    
    # Optional: Filter for roles relevant to development, e.g., those containing "Developer" or "Engineer"
    keywords = ['Developer', 'Engineer']
    filtered_jobs = [job for job in all_jobs if any(kw.lower() in job['title'].lower() for kw in keywords)]
    
    # Save the data into a CSV file
    df = pd.DataFrame(filtered_jobs)
    df.to_csv("mnc_jobs.csv", index=False)
    print("Scraping complete, data saved to mnc_jobs.csv")

if __name__ == "__main__":
    main()
