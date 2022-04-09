import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome('/usr/bin/chromedriver',
                              chrome_options=chrome_options)
    return driver


if __name__ == '__main__':
    driver = create_driver()
    page = 0
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
        else:
            print('[page {}] Something is wrong. Restarting driver and sleeping for 60 seconds...'.format(page))
            driver = create_driver()
            time.sleep(60)
