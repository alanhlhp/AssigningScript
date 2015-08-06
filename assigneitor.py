#!Python27
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from config import *

# This function will fill out the SSO Login Form
def ssoLogin():
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(usrnm)
    password.send_keys(psswrd)
    driver.find_element_by_name("submitFrm").click()

# This function will find the desired dropdown and select the appropriate option 
def select_dropdown(driver, dropdown_id, option_value):
    dd = driver.find_element_by_name(dropdown_id)
    xpath = ".//option[@value='{}']".format(option_value)
    dd.find_element_by_xpath(xpath).click()

driver = webdriver.Ie() # Get local session of IE
#driver = webdriver.Firefox() # Get local session of Firefox
driver.get(queue) # Load page
time.sleep(0.2) # Let the page load
#ssoLogin()
driver.implicitly_wait(3) # 3 seconds
driver.switch_to_frame("mycase")
select_dropdown(driver, "allComm", "322555") # Selects the community
select_dropdown(driver, "selIdProcessAjax", "1820234") # Selects the process
select_dropdown(driver, "selIdStepAjax", "1820246") #Selects the step
driver.find_element_by_xpath("//a[contains(@href, 'fnSubmit')]").click() #clickbutton

data = []
table = driver.find_element_by_xpath("//table[@bgColor = '#dddddd']")
rowCount = table.find_elements_by_xpath("//tbody/tr[@bgColor = '#ffffff']") #length of table
print len(rowCount)
#this cycle get all case numbers in a list
for row in rowCount:
    numCase = row.find_elements_by_xpath("//td[@class = 'reqId']")
data.append([td.text for td in numCase])
print data
