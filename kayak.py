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
    driver.implicitly_wait(10)
    driver.set_window_size(1319, 750)
    driver.get(url)
    driver.implicitly_wait(10)

    return driver


def fill_form(driver, city):
    '''Receives a search_argument to insert it in the search bar and
    then clicks the search button.'''

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
    data_name = driver.find_element_by_class_name(
        'bookingLink').get_attribute('data-name')

    for accomodation_title in driver.find_elements_by_class_name('keel-grid providersGrid no-overflow'):
        if 'KAYAK' in data_name:
            hotel_link = accomodation_title.find_element_by_class_name(
                'bookingLink')
            print(data_name)
            hotel_href = hotel_link.get_attribute('href')
            accommodations_urls.append(hotel_href)

    for url in accommodations_urls:
        url_data = scrape_accommodation_data(driver, url)
        print(url_data)
        accommodations_data.append(url_data)

    return accommodations_data


def scrape_accommodation_data(driver, accommodation_url):
    '''Visits an accommodation page and extracts the data.'''

    if driver == None:
        driver = prepare_driver(accommodation_url)

    driver.get(accommodation_url)
    time.sleep(3)

    accommodation_fields = dict()
    # Get the most popular facilities

    try:
        accommodation_fields['name'] = driver.find_element_by_class_name(
            'hotelName').text
    except Exception as e:
        accommodation_fields['name'] = 'empty'

    try:
        accommodation_fields['rooms'] = driver.find_element_by_class_name(
            'price').text
    except Exception as e:
        accommodation_fields['rooms'] = 'empty'

    return accommodation_fields


if __name__ == '__main__':
    city = "Monteria, Cordoba"
    try:
        driver = prepare_driver(url)
        fill_form(driver, city)
        accommodations_data = scrape_results(driver)
        accommodations_data = json.dumps(accommodations_data, indent=4)
        with open('kayak_monteria_test.json', 'w') as f:
            f.write(accommodations_data)
    finally:
        driver.quit()
