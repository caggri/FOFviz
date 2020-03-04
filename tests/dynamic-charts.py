from selenium import webdriver
import time

chromedriver = "C:/Users/deniz/chromedriver/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get('http://127.0.0.1:8000/')

dashboard = '//*[@id="accordionSidebar"]/li[1]/a'
plotdropdown = '//*[@id="plotType"]'

plot_scatter = '//*[@id="plotType"]/option[1]'
plot_gbarchart = '//*[@id="plotType"]/option[2]'
plot_dotplot = '//*[@id="plotType"]/option[3]'
plot_linechart = '//*[@id="plotType"]/option[4]'

time.sleep(2)
driver.find_element_by_xpath(dashboard).click()
time.sleep(3)

driver.find_element_by_xpath(plotdropdown).click()
time.sleep(2)
driver.find_element_by_xpath(plot_scatter).click()
time.sleep(3)

driver.find_element_by_xpath(plotdropdown).click()
time.sleep(2)
driver.find_element_by_xpath(plot_gbarchart).click()
time.sleep(3)

driver.find_element_by_xpath(plotdropdown).click()
time.sleep(2)
driver.find_element_by_xpath(plot_dotplot).click()
time.sleep(3)

driver.find_element_by_xpath(plotdropdown).click()
time.sleep(2)
driver.find_element_by_xpath(plot_linechart).click()
time.sleep(3)