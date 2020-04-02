from selenium import webdriver
import time
import secrets
import string

chromedriver = "C:/Users/deniz/chromedriver/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get('http://127.0.0.1:8000/')

usr = "haydar"
pwd = "123"

alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(12))

getstarted_btn = '//*[@id="hero"]/div/div/div[1]/div[1]/a[2]'
user_dropdown = '//*[@id="userDropdown"]'
username_input = '//*[@id="id_username"]'
password_input = '//*[@id="id_password"]'
login_btn = '//*[@id="loginBtn"]'
logout_btn = '//*[@id="content"]/nav/ul/li/div/a[3]'
logout = '//*[@id="logoutModal"]/div/div/div[3]/a'

#Go to user
time.sleep(3)
driver.find_element_by_xpath(getstarted_btn).click()
time.sleep(3)
driver.find_element_by_xpath(user_dropdown).click()

#faulty credentials
time.sleep(3)
driver.find_element_by_xpath(username_input).send_keys("haysashasc")
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys(password)
time.sleep(1)
driver.find_element_by_xpath(login_btn).click()

time.sleep(3)
driver.find_element_by_xpath(username_input).clear()
time.sleep(1)
driver.find_element_by_xpath(username_input).send_keys("HAYDAR")
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys("123")
time.sleep(1)
driver.find_element_by_xpath(login_btn).click()

time.sleep(3)
driver.find_element_by_xpath(username_input).clear()
time.sleep(1)
driver.find_element_by_xpath(username_input).send_keys("      ")
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys("26431546464646456546454646454646")
time.sleep(1)
driver.find_element_by_xpath(login_btn).click()

time.sleep(3)
driver.find_element_by_xpath(username_input).clear()
time.sleep(1)
driver.find_element_by_xpath(username_input).send_keys("jphnsx")
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys("   ")
time.sleep(1)
driver.find_element_by_xpath(login_btn).click()

time.sleep(3)
driver.find_element_by_xpath(username_input).clear()
time.sleep(1)
driver.find_element_by_xpath(username_input).send_keys("????")
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys("!:;")
time.sleep(1)
driver.find_element_by_xpath(login_btn).click()

time.sleep(3)
driver.find_element_by_xpath(username_input).clear()
time.sleep(1)
driver.find_element_by_xpath(username_input).send_keys("bronson@cdcdc.com")
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys("x")
time.sleep(1)
driver.find_element_by_xpath(login_btn).click()

#correct login
time.sleep(3)
driver.find_element_by_xpath(username_input).clear()
time.sleep(1)
driver.find_element_by_xpath(username_input).send_keys(usr)
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys(pwd)
time.sleep(1)
driver.find_element_by_xpath(login_btn).click()

#logout
time.sleep(4)
driver.find_element_by_xpath(user_dropdown).click()
time.sleep(2)
driver.find_element_by_xpath(logout_btn).click()
time.sleep(2)
driver.find_element_by_xpath(logout).click()
