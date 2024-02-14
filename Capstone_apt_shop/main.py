from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

GOOGLE_SHEETS = "https://docs.google.com/forms/d/e/1FAIpQLScUqMTGXE7Fc8wKoWq0oolTjyLQNZqyPbOUWDuWnBfb6aylsA/viewform?usp=sf_link"
ZILLOW = "https://appbrewery.github.io/Zillow-Clone/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

response = requests.get(ZILLOW)
apts = response.text

soup = BeautifulSoup(apts, "html.parser")

apt_links = soup.find_all(class_="StyledPropertyCardDataArea-anchor", name="a")
apt_address = soup.find_all(name="address")

address_link = []
for dress in apt_address:
    address_link.append(dress.text.strip())

link_list = []
for link in apt_links:
    link_list.append(link.get("href"))

print(link_list)
print(address_link)

apt_price = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")

price_list = []
for price in apt_price:
    price_list.append(price.text.rstrip(" +/mobd1"))

print(price_list)

driver = webdriver.Chrome(options=chrome_options)

for num in range(len(apt_links)):
    driver.get(GOOGLE_SHEETS)
    time.sleep(2)
    price = driver.find_element(by=By.XPATH,
                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address = driver.find_element(by=By.XPATH,
                                  value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address.send_keys(address_link[num])
    price.send_keys(price_list[num])
    link.send_keys(link_list[num])
    submit_button.click()
