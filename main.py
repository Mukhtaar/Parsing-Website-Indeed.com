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


def get_total_pages(query, location):
    parameters = {
        'q': query,
        'l': location
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


def get_all_items(query, location, start, page):
    parameters = {
        'q': query,
        'l': location,
        'start': start
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

    with open(f'json_result/{query}_in_{location}_page_{page}.json', 'w+') as json_data:
        json.dump(jobs_list, json_data)
    print('Json created success!')
    return jobs_list


def create_document(dataFrame, filename, jobs_list=None):
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass

    df = pd.DataFrame(dataFrame)
    df.to_csv(f'Indeed_data/{filename}.csv', index=False)
    print('Data created success!')


def run():
    query = input('Enter your query : ')
    location = input('Enter your location : ')

    total = get_total_pages(query, location)
    counter = 0
    final_result = []
    for page in range(total):
        page += 1
        counter += 10
        final_result += get_all_items(query, location, counter, page)

    # Formating data
    try:
        os.mkdir('Reports')
    except FileExistsError:
        pass

    with open('reports/{}.json'.format(query), 'w+') as final_data:
        json.dump(final_result, final_data)

    print('Data json created success')

    # Created document
    create_document(final_result, query)


if __name__ == '__main__':
    run()
