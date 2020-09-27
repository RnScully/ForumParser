import selenium
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import time

def read_config(config):
    '''
    function which reads the config file. 
    ++++++
    Parameters
    config(string): Path of config file
    ++++++
    Returns
    read_from(str): url to read from 
    write_to(str): url to write to
    user(str):username for login
    password(str):password for login
    '''
    with open(config, 'r') as file:
        lines = file.readlines()
        
    read_from = lines[2].strip('\n')[13:]
    write_to = lines[3].strip('\n')[14:]
    user = lines[4].strip('\n')[9:]
    password = lines[5].strip('\n')[9:]
    
    return read_from, write_to, user, password

def login(password, login):
    '''
    logs into the forums. 
    '''
    driver.get('https://discoverygc.com/forums/index.php')
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

def get_body(url_of_page):
    '''
    function which goes to the page and gets the body of the page
    returns
    Text(list) List of all text in the body, formatted kind of nicely. 
    '''
    #go to events_tracker page and download its info
    driver.get(url_of_page)
    data = driver.find_element_by_class_name('body')
    #clean up the data
    text = data.get_attribute('outerHTML').split('<br>')
    text.pop()#get rid of header and footer nonsense info
    text.pop(0)
    return text

def save_to_txt(textlist, path):
    output_document = open("events.txt", "w")
    for line in text:
        output_document.write(line)
    output_document.close()




if __name__ == "__main__":
    
    #read arguments
    config = 'config.txt'
    
    #start up selenium
    option = webdriver.FirefoxOptions()
    option.add_argument('-headless')
    print("Hello, I'm just getting everything together")
    driver =  webdriver.Firefox(options=option)
    actions = ActionChains(driver)

    read_from, write_to, user, password = read_config(config)
    print("logging in!")
    login(password, user)
    text = get_body(read_from)
    text.insert(0, '[EventData]\n') #fixes lack of leading eventData block that is breaking the formatter robot. 
    save_to_txt(text, "events.txt")
    print("text saved")