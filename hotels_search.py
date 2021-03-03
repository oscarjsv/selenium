from selenium import webdriver
import json
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


url = 'https://www.hotels.com'


def prepare_driver(url):
    '''Returns a chrome Webdriver.'''
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'h-full')))
    return driver


def fill_form(driver, city):
    '''Receives a search_argument to insert it in the search bar and
    then clicks the search button.'''

    search_field = driver.find_element_by_name('q-destination')
    search_field.send_keys(city)
    # We look for the search button and click it
    randomClick = driver.find_elements_by_xpath('//h1')
    submitButton = driver.find_element_by_xpath('//button[@type="submit"]')

    if randomClick:
        randomClick[0].click()

    submitButton.click()

    wait = WebDriverWait(driver, timeout=2).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'h-full')))


def scrape_results(driver):
    '''Returns the data from n_results amount of results.'''


    accommodations_urls = []
    accommodations_data = []
    
    for accomodation_title in driver.find_elements_by_class_name('p-name'):
        try:
            hotel_link = accomodation_title.find_element_by_class_name(
                'property-name-link')
            hotel_href = hotel_link.get_attribute('href')
            accommodations_urls.append(hotel_href)
        except Exception as e:
            print(e)
            continue

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
    time.sleep(1)

    accommodation_fields = dict()
    # Get the most popular facilities
    
    try:
        accommodation_fields['name'] = driver.find_element_by_xpath('.//h3/a')
    except NoSuchElementException:
        accommodation_fields['name'] = 'empty'
    
    return accommodation_fields


if __name__ == '__main__':
    city = "barranquilla, colombia"
    try:
        driver = prepare_driver(url)
        fill_form(driver, city)
        accommodations_data = scrape_results(driver)
        accommodations_data = json.dumps(accommodations_data, indent=4)
        with open('hotels.json', 'w') as f:
            f.write(accommodations_data)
    finally:
        driver.quit()
