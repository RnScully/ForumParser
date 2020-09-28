#Readme: this will take a text file with the Events.cfg events score in it and turn that into a nicer thing. 
#it eats a file called events.txt and outputs a file called events_output. Simple. 
#Also its terrible and needs a bit more work. 
#like, this is just not a finished thing. for example, further work includes it just GOING TO THE FORUM and collecting the information
import selenium
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import time

def get_name_and_score(string):
    equal = string.index('=')
    text = string[equal+2:]
    space = text.index(' ')
    score = int(text[space:].strip('\n'))
    name = text[:space].strip(',') #if anyone has put a comma at the end of their name, this will mess them up. 
    return name, score

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

def get_body(url):
    '''
    function which goes to the page and gets the body of the page
    returns
    Text(list) List of all text in the body, formatted kind of nicely. 
    '''
    #go to events_tracker page and download its info
    driver.get(url)
    data = driver.find_element_by_class_name('body')
    #clean up the data
    text = data.get_attribute('outerHTML').split('<br>')
    text.pop()#get rid of header and footer nonsense info
    text.pop(0)
    return text

def seperate_events(lines):
    '''
    a function that takes a list of lines of the events page and seperates them into induvidual events

    Parameters
    lines(list): a list of strings from the discovery events_tracker
    Returns
    events(list): a list of lists of strigs, each sub-list being an induvidual event.  
    '''
    #cargoculting the hard way from geeks for geeks. Thanks geeks!
    # initializing split index list  
    block_indexes = []
    for idx, line in enumerate(lines):
        if line == '[EventData]\n':
            block_indexes.append(idx)
    block_indexes.pop(0) # RESOLVEDED?? get rid of the list made that will be "the guys up to the first entry"...because there are no guys before the first entry. No more empty list at front! 
    # using list comprehension + zip() to perform custom list split 
    return [lines[i : j] for i, j in zip([0] + block_indexes, block_indexes + [None])] 

def write_scores(sorted_scores):
    output_document = open("events_output.txt", "w")
    for line in sorted_scores:
        output_document.write(line+'\n')
    output_document.close()
    
def save_to_txt(textlist, path):
    output_document = open(path, "w")
    for line in text:
        output_document.write(line)
    output_document.close()
        
def sort_scores(events):
    '''
    a function which takes a list of lists of event player score strings and ranks each inner list by best performer, and generates a list of totals for the events
    Parameters:
    events(list)
    Returns
    sorted_scores(list of lists) each event sorted in descending order with a total at the top
    totals(dict) totals for each event
    '''
    sorted_scores =[]
    totals = dict()
    for groups in events:
        scores =[]
        title = groups[1][5:].strip('\n')
        sorted_scores.append(title)
        for players in groups[2:]:
            scores.append(get_name_and_score(players))
        descending = sorted(scores, key=lambda player: player[1], reverse = True)
        total = sum([players[1] for players in scores])
        totals[title] = total
        sorted_scores.append('Total: {:,}'.format(total))
        formatted = []
        for i in descending:
            x = [i[0], "{:,}".format(i[1])]

            formatted.append(' '.join(x))  
        sorted_scores+=formatted
        sorted_scores.append('')
    return sorted_scores, totals
    
if __name__=="__main__":
    
    
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
    path = 'events.txt'
    
    with open(path, 'r') as file:
        lines = file.readlines()
    

    
    events = seperate_events(lines)
    sorted_scores, totals = sort_scores(events)
    write_scores(sorted_scores)
    

    