#!Python27

# Import native libraries & config file
import time
import calendar
import datetime
import sys
from config import *

# Import Selenium with error handling
try:
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.keys import Keys
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait 
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.firefox.webdriver import WebDriver
    print "Selenium was successfully loaded"
except ImportError:
    # Error handling if Selenium is not installed on users system
    lib = "Selenium"
    print "ImportError: %s is not found on your system" % (lib)
    print "You must install %s to operate this program" % (lib)
    sys.exitfunc()

_WEEK_DAYS = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

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

def weekdayCalc(someDay):#Weekday is calculated in format (yyyy, mm, dd) > from format mm/dd/yyyy
    try:
        weekDay = calendar.weekday(int(someDay[6:9]), int(someDay[0:1]), int(someDay[3:4]))
    except ValueError or TypeError:
        weekDay = calendar.weekday(int(someDay[6:9]), int(someDay[1]), int(someDay[3:4]))
    return unicode(weekDay)
    
# This function will access the individual case and fill in the information regarding date and country exclusion
# >> Andres
def dateCountry(caseNum):
    today = datetime.datetime.today().strftime('%m/%d/%Y')
    driver = webdriver.Ie()#this is a place holder and should be removed later
    driver.get(baseURL + caseNum) #Load the case in new window
    driver.implicitly_wait(3) #3 second wait
    driver.switch_to_frame("mycase")
    lD = driver.find_element_by_id('el12853492') #Lookup the Last Day Worked
    lastDay = lD.get_attribute('value')
    LD = datetime.datetime.strptime(lastDay,'%m/%d/%Y').date()
    print 'Last day Worked: ', lastDay
    w_lastDay = weekdayCalc(lastDay)
    print 'Last day Worked was: ', _WEEK_DAYS[int(w_lastDay)]
    print 'Exit Type ------------------/'
    if today == lastDay:
        print 'Immediate Exit'
        dueDate = today
        dueDate = datetime.datetime.strptime(dueDate,'%m/%d/%Y').date()
        print 'Report Due Date is: ', dueDate.strftime('%m/%d/%Y')
        w_dueDate = weekdayCalc(dueDate)
        print 'Report Due Date falls on a: ', _WEEK_DAYS[int(w_dueDate)]
    if today > lastDay:
        print 'Already Exited'
        dueDate = today
        dueDate = datetime.datetime.strptime(dueDate,'%m/%d/%Y').date()
        print 'Report Due Date is: ', dueDate.strftime('%m/%d/%Y')
        w_dueDate = weekdayCalc(dueDate)
        print 'Report Due Date falls on a: ', _WEEK_DAYS[int(w_dueDate)]
    if today < lastDay:
        two_days = datetime.timedelta(days=2)
        print 'Regular Exit'
        dueDate = LD - two_days
        print 'Report Due Date is: ', dueDate.strftime('%m/%d/%Y')
        w_dueDate = weekdayCalc(dueDate)
        print 'Report Due Date falls on a: ', _WEEK_DAYS[int(w_dueDate)]
    
# This function will access the investigation tool to check the console for an individual user (SSO)
# >> Alan
def verify_DG(sso):
    open_tab()
    isDgInstalled = True
    driver.get("http://dgtools-prod01.dlp.corporate.ge.com/GE.DLP.Web.DLPInvestigation/Default.aspx")
    ypath = driver.find_element_by_xpath("//input[@name = 'ctl00$BodyContent$txtReportSSO']")
    ypath.send_keys(sso)
    driver.find_element_by_xpath("//input[@name = 'ctl00$BodyContent$btnReportSubmit']").click()

    wait = WebDriverWait (driver, 10)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id = 'ctl00_BodyContent_RadGridDg']//tr[@id='ctl00_BodyContent_RadGridDg_ctl00__0']/td[14]")))

        console  = driver.find_element_by_xpath("//div[@id = 'ctl00_BodyContent_RadGridDg']//tr[@id='ctl00_BodyContent_RadGridDg_ctl00__0']/td[14]").text
        estadoDG = driver.find_element_by_xpath("//div[@id = 'ctl00_BodyContent_RadGridDg']//tr[@id='ctl00_BodyContent_RadGridDg_ctl00__0']/td[11]").text
        verifAct = driver.find_element_by_xpath("//div[@id = 'ctl00_BodyContent_RadGridDg']//tr[@id='ctl00_BodyContent_RadGridDg_ctl00__0']/td[6]").text
    
        if estadoDG == 'Not Installed': #verifying agent status
            if not verifAct:
                print "DG Not Installed"
                isDgInstalled = False
            else:
                print "DG Not Installed but last activity: %s" % verifAct
                
    except:
        print "No DG records Found"
        console = "Null"
        isDgInstalled = False

    return (console, isDgInstalled)
    
def check_elements():
    countries = {0: 'Belgium', 1: 'Bulgaria', 2: 'Croatia', 3: 'Cyprus', 4: 'Denmark', 5: 'Germany', 6: 'Estonia', 7: 'Finland', 8: 'France', 9: 'Greece', 10: 'United Kingdom', 11: 'Hungary', 12: 'Ireland', 13: 'Italy', 14: 'Latvia', 15: 'Lithuania', 16: 'Luxembourg', 17: 'Malta', 18: 'The Netherlands', 19: 'Austria', 20: 'Poland', 21: 'Portugal', 22: 'Romania', 23: 'Slovenia', 24: 'Slovakia', 25: 'Spain', 26: 'Czech Republic', 27: 'Sweden'}
    country = driver.find_element_by_xpath("//div[@id ='divCond_12851595']//tr[@id='divCond_12851092']/td[2]").text
    executive = driver.find_element_by_xpath("//div[@id='divCond_12851595']//tr[@id='divCond_13003455']/td[2]").text

    if (executive == 'EB') or (executive == 'SEB') or (executive == 'VP'):
        is_Executive = True
    else:
        is_Executive = False

    if (country in countries.values() ):
        is_Country = True
    else:
        is_Country = False

    if (is_Executive == True) or (is_Country == True):
        exitControls = False
    else:
        exitControls = True
    
    #exitCotrols  False = no tiene exit controls   True = Si tiene
    if (exitControls == False):
        select_dropdown(driver, "el12853494", "No")
        if (is_Executive == True):
            select_dropdown(driver, "el13003821", "Executive Band")
        #agregar condicion IF else para AE
        else:
            select_dropdown(driver, "el13003821", "EU")
    else:
        select_dropdown(driver, "el12853494", "Yes")
        pickDate()
    
    return exitControls
    
def pickDate():
    todayM = datetime.datetime.today().strftime('%m')
    todayD = datetime.datetime.today().strftime('%d')
    todayY = datetime.datetime.today().strftime('%Y')
    todayM = int (todayM)
    todayM = todayM - 1
    todayD = int (todayD)
    if (todayD < 10):
        todayD = todayD % 10
    driver.find_element_by_xpath("//a[contains(@href, 'el12853497')]").click()
    driver.find_element_by_xpath("//select[@name = 'mSelect']//option[@value = '%s']" % todayM).click()
    value1 = driver.find_element_by_link_text("%s" % todayD).click()

def workflow(case):
    open_tab()
    driver.get("http://supportcentral.ge.com/processmaps/ProcessQFrmSet.asp")
    driver.switch_to_frame("mycasetop")
    srch = driver.find_element_by_xpath("//input[@id='TopBannerQuery']")
    srch.send_keys(case)
    driver.find_element_by_class_name("sprite-go_button_blue").click()

def close_tab():
    body = driver.find_element_by_tag_name("html")
    body.send_keys(Keys.CONTROL + 'w')

def open_tab():
    body = driver.find_element_by_tag_name("html")
    body.send_keys(Keys.CONTROL + 't')
    
def singFirst():
    driver.get("http://dgtools-prod01.dlp.corporate.ge.com/GE.DLP.Web.DLPInvestigation/Default.aspx")

def submit():
    #actualmente apuntado al boton de save
    driver.find_element_by_xpath("//a[contains(@href, 'fnSave')]").click()
    try:
        driver.switch_to.alert.accept()
    except:
        print "No alert"
        
def selectConsole(console, isDgInstalled):
    #DG Console
    driver.switch_to_frame("mycase")
    if(console == "EnProd" or console == "EnDev" or console == "EnQa"):
        driver.find_element_by_xpath("//div[@id = 'divCond_12853487']/table/tbody/tr[@id = 'divCond_13319446']/td[@bgcolor = '#ffffff']//input[@value = 'Energy Prod']").click()
    elif (console == "CorpProd" or console == "CorpDev" or console == "CorpQa"):
        driver.find_element_by_xpath("//div[@id = 'divCond_12853487']/table/tbody/tr[@id = 'divCond_13319446']/td[@bgcolor = '#ffffff']//input[@value = 'Corp Prod']").click()
    elif (console == "GRCProdBNG" or console == "GRCProdNSK" or console == "GRCProdSHA"):
        driver.find_element_by_xpath("//div[@id = 'divCond_12853487']/table/tbody/tr[@id = 'divCond_13319446']/td[@bgcolor = '#ffffff']//input[@value = 'GRC']").click()
    else:
        driver.find_element_by_xpath("//div[@id = 'divCond_12853487']/table/tbody/tr[@id = 'divCond_13319446']/td[@bgcolor = '#ffffff']//input[@value = 'Other']").click()

    #check is Dg installed field 
    if (isDgInstalled == True):
        driver.find_element_by_xpath("//div[@id = 'divCond_12853487']/table/tbody/tr[@id = 'divCond_12853499']/td[@bgcolor = '#ffffff']//input[@value = 'Yes']").click()
    else:
        driver.find_element_by_xpath("//div[@id = 'divCond_12853487']/table/tbody/tr[@id = 'divCond_12853499']/td[@bgcolor = '#ffffff']//input[@value = 'No']").click()

# This function will access the queue and get the Case Number and SSO of the cases that need to be assigned
def setUp():
    #Ruta al perfil de Firefox
    profile = webdriver.FirefoxProfile("C:\\Users\\alan.zacarias\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\k4sorz7l.alan")
    driver = webdriver.Firefox(firefox_profile=profile)
    singFirst()
    driver.get(queue) # Load page
    time.sleep(0.2) # Let the page load
    #ssoLogin()
    driver.implicitly_wait(3) # 3 seconds
    driver.switch_to_frame("mycase")
    select_dropdown(driver, "allComm", "322555") # Selects the community
    select_dropdown(driver, "selIdProcessAjax", "1820234") # Selects the process
    select_dropdown(driver, "selIdStepAjax", "1820246") #Selects the step
    driver.find_element_by_xpath("//a[contains(@href, 'fnSubmit')]").click() #clickbutton

    Cases = []
    SSOs = []
    table = driver.find_element_by_xpath("//table[@bgColor = '#dddddd']")
    rowCount = table.find_elements_by_xpath("//tbody/tr[@bgColor = '#ffffff']") #length of table
    totalNumber = len(rowCount)
    
    #Open File writing
    today = datetime.datetime.today().strftime('%m/%d/%Y')
    filename = "C:\\Users\\alan.zacarias\\Desktop\\AssigningLog.txt"
    target = open(filename, 'a')
    target.write("+++ %s +++" % today)
    target.write("\n")

    target.write("Total Cases to be assigned: %s" % totalNumber)
    target.write("\n")

    #this cycle gets all case numbers from the workflow
    if totalNumber != 0:
        numCase = driver.find_elements_by_xpath("//td[@class = 'reqId']")
        Cases = [td.text for td in numCase]
        numSSO = driver.find_elements_by_xpath("//tr[@bgColor = '#ffffff']/td[8]")
        SSOs = [td.text for td in numSSO]
    else:
        target.write("There's no cases on the queue")
        target.write("\n")
        target.close()
        sys.exitfunc()

    #this cycle goes through the whole list of cases
    count = 0
    for i in enumerate(SSOs):
        workflow(Cases[count])
        console, isDgInstalled = verify_DG(SSOs[count])
        close_tab()
        time.sleep(1)
        if console != 'Null':
            selectConsole(console, isDgInstalled)
            time.sleep(1)
            check_elements()
            target.write("SSO: %s Console: %s " % (SSOs[count], console))
            target.write("\n")
            submit()
            close_tab()
        else:
            target.write("SSO: %s Investigation Tool Error" % SSOs[count])
            target.write("\n")
        count = count + 1
        
    target.close()

setUp()
