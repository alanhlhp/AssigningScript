#!Python27
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from login import *

def ssoLogin():
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(usrnm)
    password.send_keys(psswrd)
    driver.find_element_by_name("submitFrm").click()

driver = webdriver.Ie() # Get local session of IE
#driver = webdriver.Firefox() # Get local session of Firefox
driver.get("http://supportcentral.ge.com/processmaps/ProcessQFrmSet.asp") # Load page
time.sleep(0.2) # Let the page load
#ssoLogin() #this function fills the SSO login page with credentials provided on login.py (this needs fixing)
driver.implicitly_wait(3) # 3 seconds
driver.switch_to_frame("mycase") #switching to the correct frame to find the ID we need
driver.find_element_by_link_text('SELECT BY COMMUNITY ID').click()
comm = driver.find_element_by_id("commId").send_keys('322555')
