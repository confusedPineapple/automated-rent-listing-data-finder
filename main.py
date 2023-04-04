import os
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By


service = Service(os.environ['SERVICE'])
options = ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
zillow_headers = {
'User-Agent':os.environ['USER-AGENT'],
    "Accept-Language": os.environ['ACCEPT-LANGUAGE']
}
response = requests.get(os.environ['ZILLOW-LINK'],headers=zillow_headers)
response_data = response.text
soup = BeautifulSoup(response_data,'html.parser')
driver.get(url=os.environ['GOOGLESHEET-LINK'])
driver.maximize_window()


address_tags = soup.find_all(name='address')
price_tags = soup.find_all(class_ = 'StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0 bqsBln')
link_tags = soup.find_all(class_='property-card-link', name='a')
addresses = []
prices = []
links = []
for address in address_tags:
    addresses.append(address.get_text())
for price in price_tags:
    pprice = price.get_text().split('+')[0]
    prices.append(pprice.split('/')[0])

for i in range(0,len(link_tags),2):
    link = link_tags[i].get('href')
    if link.startswith('https') == False:
        link = f'https://www.zillow.com{link}'
    links.append(link)

time.sleep(3)
for i in range(0,len(links)):
    address_entry = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_entry = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_entry = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    send = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address_entry.send_keys(addresses[i])
    price_entry.send_keys(prices[i])
    link_entry.send_keys(links[i])
    send.click()

    driver.find_element(By.LINK_TEXT,"Submit another response").click()





print(addresses)
print(prices)
print(links)
