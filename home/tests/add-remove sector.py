from selenium import webdriver
import time

chromedriver = "C:/Users/deniz/chromedriver/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get('http://127.0.0.1:8000/')

dashboard = '//*[@id="accordionSidebar"]/li[1]/a'
sectors_1 = '//*[@id="sectors"]'
sectors_1_element = '//*[@id="sectors"]/option[4]'

add_sector = '//*[@id="select_filter_form"]/div[1]/input[1]'
remove_sector = '//*[@id="select_filter_form"]/div[1]/input[2]'

sectors_2 = '//*[@id="sectors2"]'
sectors_2_element = '//*[@id="sectors2"]/option[4]'

time.sleep(2)
driver.find_element_by_xpath(dashboard).click()
time.sleep(5)
driver.find_element_by_xpath(sectors_1).click()
time.sleep(2)
driver.find_element_by_xpath(sectors_1_element).click()
time.sleep(5)
driver.find_element_by_xpath(add_sector).click()
time.sleep(5)
driver.find_element_by_xpath(sectors_2).click()
time.sleep(2)
driver.find_element_by_xpath(sectors_2_element).click()
time.sleep(5)
driver.find_element_by_xpath(remove_sector).click()

