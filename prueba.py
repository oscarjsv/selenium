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


def prepare_driver(url):
    '''Returns a chrome Webdriver.'''
    driver = webdriver.Chrome()
    driver.get(url)
    driver.set_window_size(1319, 750)
    driver.implicitly_wait(10)
    return webdriver

def fill_form(driver, city):
    
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
    # We look for the search button and click it

    driver.find_element_by_class_name('c1AQ-header')
    button1 = driver.find_element_by_class_name('c1AQ-header')
    button1.click()
    driver.implicitly_wait(10)

    driver.find_element_by_class_name('c1AQ-submit')
    button = driver.find_element_by_class_name('c1AQ-submit')
    button.click()
    driver.implicitly_wait(15)



def scrape_results(driver):
    '''Returns the data from n_results amount of results.'''

    accommodations_urls = []
    accommodations_data = []

    original_window = driver.current_window_handle
    assert len(driver.window_handles) == 1
    count = 0

    for element in driver.find_elements_by_class_name('allowWrap'):
        element = driver.find_element_by_class_name('allowWrap')
        element.click()
        count += 1
        time.sleep(5)

        # Recorrelas hasta encontrar el controlador de la nueva ventana
        handles = driver.window_handles
        size = len(handles)
        for x in range(size):
            if handles[x] != original_window:
                driver.switch_to.window(handles[x])
                urls = driver.current_url
                accommodations_urls.append(urls)
                print(accommodations_urls, count)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

    # Cambia el controlador a la ventana o pestaña original

if __name__ == '__main__':
    city = "Monteria, colombia"
    try:
        driver = prepare_driver(url)
        fill_form(driver, city)
        accommodations_data = scrape_results(driver)
    finally:
        driver.quit()