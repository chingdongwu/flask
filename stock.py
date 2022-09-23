from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = 'https://tw.stock.yahoo.com/'


def get_stocks():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = Service('chromedriver.exe')
    chrome = webdriver.Chrome(service=service, options=options)
    chrome.get(url)
    xpath = '/html/body/div[1]/div/div/div/div/div[5]/div[1]/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[2]/div/div[2]/button'
    element = chrome.find_element(by=By.XPATH, value=xpath)
    element.click()
    soup = BeautifulSoup(chrome.page_source, 'lxml')
    lis = soup.find('ul', class_="P(0) M(0)").find_all('li')
    datas = []
    for li in lis:
        data = []
        for span in li.find('span'):
            data.append(span.strip())

        for spandown in li.find_all('span', class_="Fw(600) Fz(16px) D(f) Ai(c) C($c-trend-down)"):
            if spandown.text:
                data.append(spandown.text.strip())
        for spanup in li.find_all('span', class_="Fw(b) Fz(16px) D(f) Ai(c) C($c-trend-up)"):
            if spanup.text:
                data.append(spandown.text.strip())
        datas.append(data)

    return datas


if __name__ == '__main__':
    print(get_stocks())
