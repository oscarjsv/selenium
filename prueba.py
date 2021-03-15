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
    return driver

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
    element = driver.find_element_by_class_name('allowWrap')
    for element in driver.find_elements_by_class_name('allowWrap'):
        element.click()
        count += 1

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
    
    for url in accommodations_urls:
        url_data = scrape_accommodation_data(driver, url)
        print(url_data)
        accommodations_data.append(url_data)

def scrape_accommodation_data(driver, accommodation_url):
    '''Visits an accommodation page and extracts the data.'''

    if driver == None:
        driver = prepare_driver(accommodation_url)

    driver.get(accommodation_url)
    time.sleep(3)

    accommodation_fields = dict()
    # Get the most popular facilities

    try:
        accommodation_fields['name'] = driver.find_element_by_xpath(
            '//*[@id="M57K"]/div/h1').text
    except Exception as e:
        accommodation_fields['name'] = 'empty'
    
    # try:
    #     accommodation_fields['rooms'] = driver.find_element_by_xpath(
    #         '//*[@id="at-a-glance"]/div/div/div[1]/div/ul[1]/li[1]').text
    # except Exception as e:
    #     accommodation_fields['rooms'] = 'empty'

    return accommodation_fields

if __name__ == '__main__':
    city = "Monteria, colombia"
    try:
        driver = prepare_driver(url)
        fill_form(driver, city)
        accommodations_data = scrape_results(driver)
    finally:
        driver.quit()