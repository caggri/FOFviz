from selenium import webdriver
import time

chromedriver = "C:/Users/deniz/chromedriver/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get('http://127.0.0.1:8000/')

moreinfo_btn = '//*[@id="hero"]/div/div/div[1]/div[1]/a[1]'
about_btn = '//*[@id="header"]/div/nav/ul/li[2]/a'
capabilities_btn = '//*[@id="header"]/div/nav/ul/li[3]/a'
team_btn = '//*[@id="header"]/div/nav/ul/li[4]/a'
back_to_top_btn = '/html/body/a'

print("Getting started.")
time.sleep(4)
driver.find_element_by_xpath(about_btn).click()
time.sleep(4)
driver.find_element_by_xpath(capabilities_btn).click()
time.sleep(4)
driver.find_element_by_xpath(team_btn).click()
time.sleep(4)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(4)
driver.find_element_by_xpath(back_to_top_btn).click()

print("End.")