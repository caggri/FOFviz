from selenium import webdriver
import time

chromedriver = "C:/Users/deniz/chromedriver/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get('http://127.0.0.1:8000/')

usr = "hasan"
pwd = "123456"

user_dropdown = '//*[@id="userDropdown"]'
username_input = '//*[@id="id_username"]'
password_input = '//*[@id="id_password"]'
login_submit = '//*[@id="loginBtn"]'
logout_btn = '//*[@id="content"]/nav/ul/li[4]/div/a[4]'
logout = '//*[@id="logoutModal"]/div/div/div[3]/a'

time.sleep(3)
driver.find_element_by_xpath(user_dropdown).click()

time.sleep(3)
driver.find_element_by_xpath(username_input).send_keys("asafsdasdaf")
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys("afsdsafasdfa")
time.sleep(1)
driver.find_element_by_xpath(login_submit).click()

time.sleep(3)
driver.find_element_by_xpath(username_input).clear()
driver.find_element_by_xpath(username_input).send_keys(usr)
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys(pwd)
time.sleep(1)
driver.find_element_by_xpath(login_submit).click()

time.sleep(5)
driver.find_element_by_xpath(user_dropdown).click()
time.sleep(2)
driver.find_element_by_xpath(logout_btn).click()
time.sleep(2)
driver.find_element_by_xpath(logout).click()
