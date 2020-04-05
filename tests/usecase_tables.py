from selenium import webdriver
import time
import secrets
import string

chromedriver = "C:/Users/deniz/chromedriver/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get('http://127.0.0.1:8000/')

#intro page
moreinfo_btn = '//*[@id="hero"]/div/div/div[1]/div[1]/a[1]'
getstarted_btn = '//*[@id="hero"]/div/div/div[1]/div[1]/a[2]'
back_to_top_btn = '/html/body/a'

#Inside the fof
#dashboard_btn = '//*[@id="accordionSidebar"]/li[1]/a'
tables_btn = '//*[@id="accordionSidebar"]/li[2]/a'
sidebar_toggle_btn = '//*[@id="sidebarToggle"]'

#Selected Data dropdown
selected_data_dropdown = '//*[@id="dataName"]'
selected_data_dropdown_element_1 = '//*[@id="dataName"]/option[2]' #Flow of Funds
selected_data_dropdown_element_2 = '//*[@id="dataName"]/option[3]' #Balance Sheet - Annual
selected_data_dropdown_element_3 = '//*[@id="dataName"]/option[4]' #Balance Sheet - Monthly

#Time Frames dropdown
time_frames_dropdown = '//*[@id="timeFrames"]'
time_frames_dropdown_element_1 = '//*[@id="timeFrames"]/option[2]'
time_frames_dropdown_element_2 = '//*[@id="timeFrames"]/option[3]'

#Show Entries dropdown
show_entries_dropdown = '//*[@id="dataTable_length"]/label/select'
show_entries_dropdown_element_1 = '//*[@id="dataTable_length"]/label/select/option[1]'
show_entries_dropdown_element_2 = '//*[@id="dataTable_length"]/label/select/option[2]'
show_entries_dropdown_element_3 = '//*[@id="dataTable_length"]/label/select/option[3]'
show_entries_dropdown_element_4 = '//*[@id="dataTable_length"]/label/select/option[4]'

#Search field
search_field = '//*[@id="dataTable_filter"]/label/input'
alphabet = string.ascii_letters + string.digits
weird_text_1 = ''.join(secrets.choice(alphabet) for i in range(12))
alphabet = string.ascii_letters + string.digits
weird_text_2 = ''.join(secrets.choice(alphabet) for i in range(8))
input_actual_1 = 'Securi'
input_actual_2 = 'Security'

#Table Order
entry_no_order_btn = '//*[@id="dataTable"]/thead/tr/th[1]'
assets_order_btn =  '//*[@id="dataTable"]/thead/tr/th[2]'
quarter_1_order_btn = '//*[@id="dataTable"]/thead/tr/th[3]'
liabilities_order_btn = '//*[@id="dataTable"]/thead/tr/th[4]'
quarter_2_order_btn = '//*[@id="dataTable"]/thead/tr/th[5]'

#Back to Top
back_to_top_tables_btn = '//*[@id="wrapper"]/a'

#Next/Previous buttons
next_btn = '//*[@id="dataTable_next"]/a'
previous_btn = '//*[@id="dataTable_previous"]/a'

#START **************

#Click more info and get started
print("Getting started.")
time.sleep(3)
driver.find_element_by_xpath(moreinfo_btn).click()
time.sleep(4)
driver.find_element_by_xpath(back_to_top_btn).click()
time.sleep(3)
driver.find_element_by_xpath(getstarted_btn).click()

#Tables tab clicked, side toolbar hide clicked
print("Tables tab, side toolbar hide")
time.sleep(3)
driver.find_element_by_xpath(tables_btn).click()
time.sleep(2)
driver.find_element_by_xpath(sidebar_toggle_btn).click()
time.sleep(2)
driver.find_element_by_xpath(sidebar_toggle_btn).click()

#Balance sheet annual
print("Balance sheet annual")
time.sleep(3)
driver.find_element_by_xpath(selected_data_dropdown).click()
time.sleep(3)
driver.find_element_by_xpath(selected_data_dropdown_element_2).click()

#Balance sheet monthly
print("Balance sheet monthly")
time.sleep(3)
driver.find_element_by_xpath(selected_data_dropdown).click()
time.sleep(3)
driver.find_element_by_xpath(selected_data_dropdown_element_3).click()

#Time Frames
print("Time Frames")
time.sleep(3)
driver.find_element_by_xpath(time_frames_dropdown).click()
time.sleep(3)
driver.find_element_by_xpath(time_frames_dropdown_element_2).click()
time.sleep(3)
driver.find_element_by_xpath(selected_data_dropdown_element_1).click()

#Show Entries
print("Show Entries")
time.sleep(3)
driver.find_element_by_xpath(show_entries_dropdown).click()
time.sleep(2)
driver.find_element_by_xpath(show_entries_dropdown_element_1).click()

time.sleep(2)
driver.find_element_by_xpath(show_entries_dropdown_element_2).click()
time.sleep(2)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)
driver.find_element_by_xpath(back_to_top_tables_btn).click()

time.sleep(2)
driver.find_element_by_xpath(show_entries_dropdown_element_3).click()
time.sleep(2)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)
driver.find_element_by_xpath(back_to_top_tables_btn).click()

time.sleep(2)
driver.find_element_by_xpath(show_entries_dropdown_element_4).click()
time.sleep(2)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)
driver.find_element_by_xpath(back_to_top_tables_btn).click()

time.sleep(2)
driver.find_element_by_xpath(show_entries_dropdown_element_1).click()

#Back to Tables main
time.sleep(2)
driver.find_element_by_xpath(tables_btn).click()

#Ascend/Descend Ordering
print("Ascend/Descend Ordering")
#EntryNo
time.sleep(3)
driver.find_element_by_xpath(entry_no_order_btn).click()
time.sleep(3)
driver.find_element_by_xpath(entry_no_order_btn).click()

#Assets
time.sleep(3)
driver.find_element_by_xpath(assets_order_btn).click()
time.sleep(3)
driver.find_element_by_xpath(assets_order_btn).click()

#Quarter 1
time.sleep(3)
driver.find_element_by_xpath(quarter_1_order_btn).click()
time.sleep(3)
driver.find_element_by_xpath(quarter_1_order_btn).click()

#Liabilities
time.sleep(3)
driver.find_element_by_xpath(liabilities_order_btn).click()
time.sleep(3)
driver.find_element_by_xpath(liabilities_order_btn).click()

#Quarter 2
time.sleep(3)
driver.find_element_by_xpath(quarter_2_order_btn).click()
time.sleep(3)
driver.find_element_by_xpath(quarter_2_order_btn).click()

#Back to Tables main
time.sleep(2)
driver.find_element_by_xpath(tables_btn).click()

#Next/Previous
print("Next/Previous")
time.sleep(2)
driver.find_element_by_xpath(next_btn).click()
time.sleep(3)
driver.find_element_by_xpath(next_btn).click()
time.sleep(3)
driver.find_element_by_xpath(next_btn).click()
time.sleep(2)
driver.find_element_by_xpath(previous_btn).click()
time.sleep(3)
driver.find_element_by_xpath(previous_btn).click()
time.sleep(3)
driver.find_element_by_xpath(previous_btn).click()

#Search field
print("Search Field")
time.sleep(2)
driver.find_element_by_xpath(search_field).click()

#Incorrect search
time.sleep(2)
driver.find_element_by_xpath(search_field).send_keys(weird_text_1)
time.sleep(2)
driver.find_element_by_xpath(search_field).clear()
time.sleep(2)
driver.find_element_by_xpath(search_field).send_keys(weird_text_2)
time.sleep(2)
driver.find_element_by_xpath(search_field).clear()

#Correct search
time.sleep(2)
driver.find_element_by_xpath(search_field).send_keys(input_actual_1)
time.sleep(2)
driver.find_element_by_xpath(search_field).clear()
time.sleep(2)
driver.find_element_by_xpath(search_field).send_keys(input_actual_2)
time.sleep(2)
driver.find_element_by_xpath(search_field).clear()

print("End.")