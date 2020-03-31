from selenium import webdriver
import time
import secrets
import string


chromedriver = "C:/Users/deniz/chromedriver/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get('http://127.0.0.1:8000/')

alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(12))

usr = "havuc"
email = "havuc@home.com"
pwd = password

usr_old = "haydar"
email_old = "haydar@home.com"
pwd_old = "123"

getstarted_btn = '//*[@id="hero"]/div/div/div[1]/div[1]/a[2]'
user_dropdown = '//*[@id="userDropdown"]'
username_input = '//*[@id="id_username"]'
password_input = '//*[@id="id_password"]'
email_input = '//*[@id="id_email"]'
logout_btn = '//*[@id="content"]/nav/ul/li/div/a[3]'
logout = '//*[@id="logoutModal"]/div/div/div[3]/a'
create_account = '/html/body/div/div/div/form/div/div/div[4]/a[2]'
register_btn = '//*[@id="loginBtn"]'

#Go to register
time.sleep(3)
driver.find_element_by_xpath(getstarted_btn).click()
time.sleep(3)
driver.find_element_by_xpath(user_dropdown).click()
time.sleep(3)
driver.find_element_by_xpath(create_account).click()

#faulty credentials
time.sleep(3)
driver.find_element_by_xpath(username_input).send_keys(usr_old)
time.sleep(1)
driver.find_element_by_xpath(email_input).send_keys(email_old)
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys(pwd_old)
time.sleep(1)
driver.find_element_by_xpath(register_btn).click()

#correct register
time.sleep(3)
driver.find_element_by_xpath(username_input).clear()
driver.find_element_by_xpath(email_input).clear()
driver.find_element_by_xpath(password_input).clear()
driver.find_element_by_xpath(username_input).send_keys(usr)
time.sleep(1)
driver.find_element_by_xpath(email_input).send_keys(email)
time.sleep(1)
driver.find_element_by_xpath(password_input).send_keys(pwd)
time.sleep(1)
driver.find_element_by_xpath(register_btn).click()