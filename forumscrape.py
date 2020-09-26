import selenium
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import time

def read_password(config):
    with open(config, 'r') as file:
        lines = file.readlines()
    password = lines[1].strip('\n')
    user = lines[0].strip('\n')
    return user, password

def login(front_page, config):
    '''
    Use read_password to grab username and password, and log into the forums. 
    '''
    user, password = read_password(config)
    
    driver.get(front_page)
    login = driver.find_element_by_class_name("login")
    login.click()
    time.sleep(1)
    username_box = driver.find_element_by_id("quick_login_username")
    username_box.send_keys(user)
    pass_box = driver.find_element_by_id("quick_login_password")
    pass_box.send_keys(password)
    time.sleep(1)
    button = driver.find_element_by_xpath('//*[@id="quick_login"]/form/table/tbody/tr[5]/td/div/input')
    button.click()
    time.sleep(1)
    return


front_page = 'https://discoverygc.com/forums/index.php'
config = 'config.txt'
events_tracker = 'https://discoverygc.com/forums/dev_config_view.php?action=viewfile&file=events_tracker.cfg'

#start up selenium
option = webdriver.FirefoxOptions()
#option.add_argument('-headless')
print("Hello, I'm just getting everything together")
driver =  webdriver.Firefox(options=option)
actions = ActionChains(driver)


login(front_page, config)

#go to events_tracker page and download its info
driver.get(events_tracker)
data = driver.find_element_by_class_name('body')
#clean up the data
text = data.get_attribute('outerHTML').split('<br>')
text.pop()#get rid of header and footer nonsense info
text.pop(0)

htmltext.split('<br>')
