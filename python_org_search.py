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

url = 'https://www.booking.com'


def prepare_driver(url):
    '''Returns a chrome Webdriver.'''
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.ID, 'ss')))
    return driver


def fill_form(driver, city):
    '''Receives a search_argument to insert it in the search bar and
    then clicks the search button.'''

    search_field = driver.find_element_by_id('ss')
    search_field.send_keys(city)
    # We look for the search button and click it
    driver.find_element_by_class_name('sb-searchbox__button')\
        .click()

    wait = WebDriverWait(driver, timeout=1).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'sr-hotel__title')))


def scrape_results(driver):
    '''Returns the data from n_results amount of results.'''
    accommodations_urls = []
    accommodations_data = []
    active = False

    next_click = driver.find_element_by_class_name(
        'bui-pagination__next-arrow').get_attribute("class")
    next_button = driver.find_element_by_class_name(
        'paging-next').get_attribute("href")

    if 'bui-pagination__item--disabled' in next_click:
        active = True
    while True:

        for accomodation_title in driver.find_elements_by_class_name('sr-hotel__title'):
            try:
                hotel_link = accomodation_title.find_element_by_class_name(
                    'hotel_name_link')
                hotel_href = hotel_link.get_attribute('href')
                accommodations_urls.append(hotel_href)
            except Exception as e:
                print(e)
                continue

        for url in accommodations_urls:
            print(type(url), url)
            url_data = scrape_accommodation_data(driver, url)
            # print(url_data)
            accommodations_data.append(url_data)

        if active:
            break

        if 'bui-pagination__item--disabled' in next_click:
            break

        driver.get(next_button)

        wait = WebDriverWait(driver, timeout=3).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, 'sr-hotel__title')))

        driver.find_element_by_class_name('bui-pagination__next-arrow').click()
        accommodations_urls = []
        wait = WebDriverWait(driver, timeout=3).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, 'sr-hotel__title')))

        next_click = driver.find_element_by_class_name(
            'bui-pagination__next-arrow').get_attribute("class")
        print(type(next_click), next_click)
        try:
            next_button = driver.find_element_by_class_name(
                'paging-next').get_attribute("href")
        except Exception as e:
            next_button = 'sirve perro'
            pass

        print(next_button, 'next botton pagina')
    return accommodations_data


def scrape_accommodation_data(driver, accommodation_url):
    '''Visits an accommodation page and extracts the data.'''

    if driver == None:
        driver = prepare_driver(accommodation_url)

    driver.get(accommodation_url)
    time.sleep(5)

    accommodation_fields = dict()

    # Get the accommodation score
    # try:
    #     name_container = driver.find_element_by_class_name(
    #         'bui-review-score--end')
    #     name_child = name_container.find_element_by_class_name(
    #         'bui-review-score__badge')
    #     name_text = name_child.text
    #     accommodation_fields['score'] = name_text
    # except NoSuchElementException:
    #     accommodation_fields['score'] = 'empty'

    # Get the accommodation name
    try:
        accommodation_fields['name'] = driver.find_element_by_id('hp_hotel_name')\
            .text.strip('Hotel')
    except NoSuchElementException:
        accommodation_fields['name'] = 'empty'

    # Get the accommodation location
    # try:
    #     accommodation_fields['location'] = driver.find_element_by_id('showMap2')\
    #         .find_element_by_class_name('hp_address_subtitle').text
    # except NoSuchElementException:
    #     accommodation_fields['location'] = 'empty'

    # Get the most popular facilities

    # try:
    #     accommodation_fields['popular_facilities'] = list()
    #     facilities = driver.find_element_by_class_name(
    #         'hp_desc_important_facilities')

    #     for facility in facilities.find_elements_by_class_name('important_facility'):
    #         accommodation_fields['popular_facilities'].append(facility.text)
    # except NoSuchElementException:
    #     accommodation_fields['popular_facilities'] = []

    return accommodation_fields


if __name__ == '__main__':
    city = "Monteria, colombia"
    try:
        driver = prepare_driver(url)
        fill_form(driver, city)
        accommodations_data = scrape_results(driver)
        accommodations_data = json.dumps(accommodations_data, indent=4)
        with open('monteria_booking.json', 'w', encoding='utf8') as f:
            f.write(accommodations_data)
    finally:
        driver.quit()
