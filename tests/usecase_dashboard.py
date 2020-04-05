from selenium import webdriver
import time

chromedriver = "C:/Users/deniz/chromedriver/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get('http://127.0.0.1:8000/')

#intro page
moreinfo_btn = '//*[@id="hero"]/div/div/div[1]/div[1]/a[1]'
getstarted_btn = '//*[@id="hero"]/div/div/div[1]/div[1]/a[2]'
back_to_top_btn = '/html/body/a'

#Inside the fof
dashboard_btn = '//*[@id="accordionSidebar"]/li[1]/a'
#tables_btn = '//*[@id="accordionSidebar"]/li[2]/a'
sidebar_toggle_btn = '//*[@id="sidebarToggle"]'

#important graphs
important_graphs_dropdown = '//*[@id="importantGraph"]'
important_graphs_dropdown_element_1 = '//*[@id="importantGraph"]/option[2]'
important_graphs_dropdown_element_2 = '//*[@id="importantGraph"]/option[3]'
important_graphs_dropdown_element_3 = '//*[@id="importantGraph"]/option[4]'

#Data dropdown
data_dropdown = '//*[@id="dataName"]'
data_dropdown_element_1 = '//*[@id="dataName"]/option[1]' #Flow of Funds
data_dropdown_element_2 = '//*[@id="dataName"]/option[2]' #Balance Sheet - Annual
data_dropdown_element_3 = '//*[@id="dataName"]/option[3]' #Balance Sheet - Monthly

#Plot Types dropdown
plot_type_dropdown = '//*[@id="plotType"]'
plot_type_dropdown_element_1 = '//*[@id="plotType"]/option[1]' #Line Plot
plot_type_dropdown_element_2 = '//*[@id="plotType"]/option[2]' #Stacked Bar Chart
plot_type_dropdown_element_3 = '//*[@id="plotType"]/option[3]' #Grouped Bar Chart
plot_type_dropdown_element_4 = '//*[@id="plotType"]/option[4]' #Scatter Plot
plot_type_dropdown_element_5 = '//*[@id="plotType"]/option[5]' #Alluvial Diagram
plot_type_dropdown_element_6 = '//*[@id="plotType"]/option[6]' #Area Graph
plot_type_dropdown_element_7 = '//*[@id="plotType"]/option[7]' #Density Contour
plot_type_dropdown_element_8 = '//*[@id="plotType"]/option[8]' #Heat Map

#Sector dropdowns
sector1_dropdown = '//*[@id="sectors1"]'
sector1_dropdown_element_1 = '//*[@id="sectors1"]/option[2]'
sector1_dropdown_element_2 = '//*[@id="sectors1"]/option[3]'

sector2_dropdown = '//*[@id="sectors2"]'
sector2_dropdown_element_1 = '//*[@id="sectors2"]/option[2]'
sector2_dropdown_element_2 = '//*[@id="sectors2"]/option[3]'

sector3_dropdown = '//*[@id="sectors3"]'
sector3_dropdown_element_1 = '//*[@id="sectors3"]/option[2]'
sector3_dropdown_element_2 = '//*[@id="sectors3"]/option[3]'

sector4_dropdown = '//*[@id="sectors4"]'
sector4_dropdown_element_1 = '//*[@id="sectors4"]/option[2]'
sector4_dropdown_element_2 = '//*[@id="sectors4"]/option[3]'

add_sector_btn = '//*[@id="select_filter_form"]/div[2]/input[1]'
remove_sector_btn = '//*[@id="select_filter_form"]/div[2]/input[2]'

#START **************

#Click more info and get started
print("Getting started.")
time.sleep(3)
driver.find_element_by_xpath(moreinfo_btn).click()
time.sleep(4)
driver.find_element_by_xpath(back_to_top_btn).click()
time.sleep(3)
driver.find_element_by_xpath(getstarted_btn).click()

#Dashboard tab clicked, side toolbar hide clicked
print("Dashboard tab click, side toolbar hide click")
time.sleep(3)
driver.find_element_by_xpath(dashboard_btn).click()
time.sleep(2)
driver.find_element_by_xpath(sidebar_toggle_btn).click()
time.sleep(2)
driver.find_element_by_xpath(sidebar_toggle_btn).click()

#Important Graphs
print("Important Graphs")
time.sleep(3)
driver.find_element_by_xpath(important_graphs_dropdown).click()
time.sleep(3)
driver.find_element_by_xpath(important_graphs_dropdown_element_1).click()
time.sleep(3)
driver.find_element_by_xpath(important_graphs_dropdown_element_2).click()
time.sleep(3)
driver.find_element_by_xpath(important_graphs_dropdown_element_3).click()

#Data dropdown
print("Data dropdown")
time.sleep(3)
driver.find_element_by_xpath(data_dropdown).click()
time.sleep(3)
driver.find_element_by_xpath(data_dropdown_element_1).click()
time.sleep(3)
driver.find_element_by_xpath(data_dropdown_element_2).click()
time.sleep(3)
driver.find_element_by_xpath(data_dropdown_element_3).click()

#Plot type dropdown
print("Plot type dropdown")
time.sleep(3)
driver.find_element_by_xpath(plot_type_dropdown).click()
time.sleep(2)
driver.find_element_by_xpath(plot_type_dropdown_element_1).click()
time.sleep(2)
driver.find_element_by_xpath(plot_type_dropdown_element_2).click()
time.sleep(2)
driver.find_element_by_xpath(plot_type_dropdown_element_3).click()
time.sleep(2)
driver.find_element_by_xpath(plot_type_dropdown_element_4).click()
time.sleep(2)
driver.find_element_by_xpath(plot_type_dropdown_element_5).click()
time.sleep(2)
driver.find_element_by_xpath(plot_type_dropdown_element_6).click()
time.sleep(2)
driver.find_element_by_xpath(plot_type_dropdown_element_7).click()
time.sleep(2)
driver.find_element_by_xpath(plot_type_dropdown_element_8).click()

#Sector1 dropdown
print("Sector 1 dropdown")
time.sleep(2)
driver.find_element_by_xpath(sector1_dropdown).click()
time.sleep(2)
driver.find_element_by_xpath(sector1_dropdown_element_1).click()
time.sleep(2)
driver.find_element_by_xpath(sector1_dropdown_element_2).click()

#Sector2 dropdown
print("Sector 2 dropdown")
time.sleep(2)
driver.find_element_by_xpath(sector2_dropdown).click()
time.sleep(2)
driver.find_element_by_xpath(sector2_dropdown_element_1).click()
time.sleep(2)
driver.find_element_by_xpath(sector2_dropdown_element_2).click()

#Add sectors
print("Add sectors")
time.sleep(3)
driver.find_element_by_xpath(add_sector_btn).click()
time.sleep(3)
driver.find_element_by_xpath(add_sector_btn).click()

#Sector3 dropdown
print("Sector 3 dropdown")
time.sleep(2)
driver.find_element_by_xpath(sector3_dropdown).click()
time.sleep(2)
driver.find_element_by_xpath(sector3_dropdown_element_1).click()
time.sleep(2)
driver.find_element_by_xpath(sector3_dropdown_element_2).click()

#Sector4 dropdown
print("Sector 4 dropdown")
time.sleep(2)
driver.find_element_by_xpath(sector4_dropdown).click()
time.sleep(2)
driver.find_element_by_xpath(sector4_dropdown_element_1).click()
time.sleep(2)
driver.find_element_by_xpath(sector4_dropdown_element_2).click()

#Remove sectors
print("Remove sectors")
time.sleep(3)
driver.find_element_by_xpath(remove_sector_btn).click()
time.sleep(3)
driver.find_element_by_xpath(remove_sector_btn).click()
time.sleep(3)
driver.find_element_by_xpath(remove_sector_btn).click()

print("End.")
