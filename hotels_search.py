from selenium import webdriver
import json
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


url = 'https://co.hoteles.com/?pos=HCOM_LATAM&locale=es_CO'


def prepare_driver(url):
    '''Returns a chrome Webdriver.'''
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    
    driver.get(url)
    driver.implicitly_wait(10)

    return driver


def fill_form(driver, city):
    '''Receives a search_argument to insert it in the search bar and
    then clicks the search button.'''
    
    try:
        driver.find_element_by_name('q-destination')
        search_field = driver.find_element_by_name('q-destination')
        search_field.send_keys(city)
    except Exception as e:
        print('no sirve')
       
        search_field = driver.find_element_by_xpath('//*[@id="modal-panel-srs-0"]/header/div/form/fieldset/div/input')
        print(search_field)
        search_field.send_keys(city)

    
    driver.implicitly_wait(10)
    # We look for the search button and click it
    randomClick = driver.find_element_by_xpath('//h1')
    submitButton = driver.find_element_by_xpath('//button[@type="submit"]')

    if randomClick:
        randomClick.click()

    submitButton.click()



 

def scrape_results(driver):
    '''Returns the data from n_results amount of results.'''
    accommodations_urls = []
    accommodations_data = []
    scroll_pause_time = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height  
    
    for accomodation_title in driver.find_elements_by_class_name('p-name'):
        hotel_link = accomodation_title.find_element_by_class_name(
            'property-name-link')
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
    time.sleep(12)

    accommodation_fields = dict()
    # Get the most popular facilities

    try:
        accommodation_fields['name'] = driver.find_element_by_xpath(
            '//*[@id="property-header"]/div/div[1]/h1').text
    except Exception as e:
        accommodation_fields['name'] = 'empty'
    
    try:
        accommodation_fields['rooms'] = driver.find_element_by_xpath(
            '//*[@id="at-a-glance"]/div/div/div[1]/div/ul[1]/li[1]').text
    except Exception as e:
        accommodation_fields['rooms'] = 'empty'

    return accommodation_fields



if __name__ == '__main__':
    city = "miami"
    try:
        driver = prepare_driver(url)
        fill_form(driver, city)
        accommodations_data = scrape_results(driver)
        accommodations_data = json.dumps(accommodations_data, indent=4)
        with open('hotels_monteria_test.json', 'w') as f:
            f.write(accommodations_data)
    finally:
        driver.quit()
