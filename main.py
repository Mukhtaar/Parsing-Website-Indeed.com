import json
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://id.indeed.com/jobs?'
site = 'https://id.indeed.com/'
parameters = {
    'q': 'Python Developer',
    'l': 'Jakarta'
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/96.0.4664.110 Safari/537.36'}

res = requests.get(url, params=parameters, headers=headers)


def get_total_pages():
    parameters = {
        'q': 'Python Developer',
        'l': 'Jakarta'
    }

    res = requests.get(url, params=parameters, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    total_pages = []
    # Scraping step
    soup = BeautifulSoup(res.text, 'html.parser')
    pagination = soup.find('ul', 'pagination-list')
    pages = pagination.find_all('li')
    for page in pages:
        total_pages.append(page.text)

    total = int(max(total_pages))
    return total


def get_all_items():
    parameters = {
        'q': 'Python Developer',
        'l': 'Jakarta'
    }
    res = requests.get(url, params=parameters, headers=headers)

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()
    soup = BeautifulSoup(res.text, 'html.parser')

    # Scraping Proses
    contents = soup.find_all('table', 'jobCard_mainContent')

    # Pick item
    # *Tittle
    # *Company name
    # *Company link
    # *Company address

    jobs_list = []
    for item in contents:
        title = item.find('h2', 'jobTitle').text
        company = item.find('span', 'companyName')
        company_name = company.text
        try:
            company_link = site + company.find('a')['href']
        except:
            company_link = 'Link is not available'

        # Shorting data
        data_dict = {
            'Title': title,
            'Company_name': company_name,
            'Link': company_link
        }
        jobs_list.append(data_dict)

    # Writing json file
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    with open('json_result/job_list.json', 'w+') as json_data:
        json.dump(jobs_list, json_data)
    print('Json created success!')

    # Created Csv
    df = pd.DataFrame(jobs_list)
    df.to_csv('Indeed_data.csv', index=False)

    # Data Created
    print('Data created success!')


if __name__ == '__main__':
    get_all_items()
