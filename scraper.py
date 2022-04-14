import json
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def feedback2dict(item):
    spans = item.find_all('span')
    links = item.find_all('a')
    date = spans[0].text
    user_type = spans[1].text[3:]
    if len(spans) > 3:
        text = spans[3].text
    else:
        text = spans[2].text
    user = links[0].text
    return {
        'user': user,
        'user_type': user_type,
        'date': date,
        'text': text
    }


def scrape_page(page, timeout=10):
    driver.get('https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/13375-Prolongation-du-reglement-sur-le-certificat-COVID-numerique-de-l%E2%80%99UE/feedback_fr?p_id=27926341&page={}'.format(page))
    t = 0
    while not 'Résultats' in driver.page_source:
        time.sleep(1)
        t += 1
        if t > timeout:
            return None
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all('feedback-item')
    return [feedback2dict(item) for item in items]


def create_driver():
    while True:
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(
                executable_path='/usr/local/bin/geckodriver', options=options)
            return driver
        except Exception as e:
            print(e)
            print('Something went wrong creating driver, sleeping for 60s.')
            sys.sleep(60)


def get_current_page():
    try:
        with open('curpage.txt', 'rt') as f:
            return int(f.read())
    except:
        return 0


def set_current_page(page):
    with open('curpage.txt', 'wt') as f:
        f.write('{}'.format(page))


if __name__ == '__main__':
    driver = create_driver()
    page = get_current_page()
    while True:
        try:
            feedbacks = scrape_page(page)
        except Exception as e:
            print(e)
            feedbacks = None
        if feedbacks and len(feedbacks) > 0:
            with open('certificat-covid-eu.json', 'at') as f:
                for feedback in feedbacks:
                    f.write('{}\n'.format(json.dumps(feedback)))
            print('page {} scrapped'.format(page))
            page += 1
            set_current_page(page)
        else:
            print('Something went wrong. Sleeping for 60s.')
            sys.sleep(60)
