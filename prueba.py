from copy import error
import json
from logging import exception
import time
from typing import Text, cast
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
    time.sleep(20)

    driver.find_element_by_class_name('showAll')
    show_all = driver.find_element_by_class_name('showAll')
    show_all.click()
    driver.implicitly_wait(15)

    next_click = driver.find_element_by_class_name(
            'ButtonPaginator').get_attribute("class")
    while True:
        next_click = driver.find_element_by_class_name(
            'ButtonPaginator').get_attribute("class")

        more_button = driver.find_element_by_class_name(
            'moreButton')

        if 'Common-Results-Paginator ButtonPaginator' == next_click:
            break

        try:
            more_button.click()
        except Exception:
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
            

        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)


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
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

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
    time.sleep(2)

    accommodation_fields = dict()

    try:
        accommodation_fields['name'] = driver.find_element_by_class_name(
            'name').text   
    except Exception as e:
        try :
            accommodation_fields['name'] = driver.find_element_by_class_name(
                'c3xth-hotelName').text
        except Exception as e:
            accommodation_fields['name'] = 'empty'

    try:
        accommodation_fields['price'] = driver.find_element_by_class_name(
            'bigPrice').text   
        print("hello", driver.find_element_by_class_name(
            'bigPrice').text)
    except Exception as e:
        try :
            accommodation_fields['price'] = driver.find_element_by_class_name(
                'c3xth-price').text
            print(driver.find_element_by_class_name(
                'c3xth-price').text, 'hello2')
        except Exception as e:
            accommodation_fields['price'] = 'empty'
    

    # c3xth-hotelName
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
        print(accommodations_data, 'esta monda')
        accommodations_data = json.dumps(accommodations_data, indent=4)
        with open('kayak_scraping.json', 'w', encoding='utf8') as f:
            f.write(accommodations_data)
    finally:
        driver.quit()
