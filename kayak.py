import json
import time
from typing import cast
import selenium
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://www.kayak.com.co/hotels'
city = "Monteria, Cordoba"

'''Set all params and libraries for scraping process'''

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.set_window_size(1319, 750)
driver.get(url)
driver.implicitly_wait(10)

driver.find_element_by_class_name('lNCO-inner')
search_field = driver.find_element_by_class_name('lNCO-inner')
search_field.click()
driver.implicitly_wait(10)

driver.find_element_by_class_name('k_my-input')
imput = driver.find_element_by_class_name('k_my-input')
imput.send_keys(city)
driver.implicitly_wait(10)

driver.find_element_by_class_name('JyN0-name')
imput = driver.find_element_by_class_name('JyN0-name')
imput.click()
driver.implicitly_wait(10)

'''Look for search button and click it'''

driver.find_element_by_class_name('c1AQ-header')
button1 = driver.find_element_by_class_name('c1AQ-header')
button1.click()
driver.implicitly_wait(10)

driver.find_element_by_class_name('c1AQ-submit')
button = driver.find_element_by_class_name('c1AQ-submit')
button.click()
driver.implicitly_wait(15)



assert len(driver.window_handles) == 1

'''Sets all elements and starts scraping loop'''

element = driver.find_element_by_class_name('allowWrap')
for element in driver.find_elements_by_class_name('allowWrap'):
    element.click()
    time.sleep(5)

    handles = driver.window_handles
    size = len(driver.window_handles)
    for x in range(size):
        if handles[x] != driver.current_window_handle:
            driver.switch_to.window(handles[x])
            print(driver.current_url)
        
        

#Cambia el controlador a la ventana o pestaña original
