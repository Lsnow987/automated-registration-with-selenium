from typing import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
from selenium.webdriver.support.ui import Select

semester_of_registration = input("semester you want to register for as it is listed in the drop down menu on banner: ")
list_of_crns = input("list of crns separated by spaces: ")
list_of_crns = list_of_crns.split(" ") 

try:
    with open('login_info.pkl', 'rb') as file:
        username = pickle.load(file)
        password = pickle.load(file)
except:
    username = input("username: ")
    password = input("password: ")
    save = input("do you want to store your login info (y/n)? ")
    if save == "y":
        with open('login_info.pkl', 'wb') as file:
            pickle.dump(username, file)
            pickle.dump(password, file)
 
url = "https://banner.oci.yu.edu/ssomanager/c/SSB?pkg=twbkwbis.P_GenMenu?name=bmenu.P_MainMnu"
# replace with your own path or use ChromeDriverManager().install() instead of PATH later
# PATH = "C:/Program Files (x86)/chromedriver.exe"


def advance(driver, by, val, isButton):
    counter = 0
    while True:
        try:
            element = driver.find_element(by=by, value=val)
            if isButton == 1: # 1 means it is a button
                element.click()
            elif isButton == 0: # 0 means we want to send a username
                element.send_keys(username)
            elif isButton == 2: # 2 means we want to send a password
                element.send_keys(password)
            elif isButton == 3: # 3 means we want to find the element but not do anything with it
                return element
            elif isButton >= 4:
                element.send_keys(list_of_crns[isButton-4])
            break # we either found the element or we are done
        except:
            counter+=1
            if counter == 300 and isButton >= 4:
                raise Exception("could not find the element")
            pass

def open_link(url):
    # could use PATH variable if you have it installed already
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.maximize_window()
    advance(driver, By.NAME, "loginfmt",0)
    advance(driver, By.ID, "idSIButton9",1)
    advance(driver, By.NAME, "passwd",2)
    time.sleep(1)
    advance(driver, By.ID, "idSIButton9",1)
    time.sleep(1)
    advance(driver, By.ID, "idSIButton9",1)
    advance(driver, By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a",1)
    advance(driver, By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[5]/td[2]/a",1)
    advance(driver, By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[5]/td[2]/a",1)
    select = Select(advance(driver, By.NAME, 'term_in',3))
    select.select_by_visible_text(semester_of_registration)
    advance(driver, By.XPATH, "/html/body/div[3]/form/input",1)

    for i in range(len(list_of_crns)):
        x = i+1
        while True:
            try:
                advance(driver, By.XPATH, f'//*[@id="crn_id{x}"]',4+i)
                break
            except:
                driver.refresh()

    advance(driver, By.XPATH, "/html/body/div[3]/form/input[19]",1)
    time.sleep(300)
    driver.quit()

open_link(url)