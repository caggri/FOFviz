from selenium import webdriver
import time

chromedriver = "C:/Users/deniz/chromedriver/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get('http://127.0.0.1:8000/')

getstarted_btn = '//*[@id="hero"]/div/div/div[1]/div[1]/a[2]'
dashboard = '//*[@id="accordionSidebar"]/li[1]/a'
add_sector = '//*[@id="select_filter_form"]/div[1]/input[1]'
remove_sector = '//*[@id="select_filter_form"]/div[1]/input[2]'

#add/remove sector on refresh error case
time.sleep(3)
driver.find_element_by_xpath(getstarted_btn).click()
time.sleep(3)
driver.find_element_by_xpath(dashboard).click()
time.sleep(3)
driver.find_element_by_xpath(remove_sector).click()
time.sleep(3)
driver.refresh()
time.sleep(3)
driver.find_element_by_xpath(add_sector).click()
time.sleep(3)
driver.refresh()

