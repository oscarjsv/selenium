from selenium import webdriver
import json
import time
from typing import cast
import selenium
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://www.colombia.com/turismo/prestadores-de-servicios-turisticos/c1/establecimiento-de-alojamiento-y-hospedaje'


def prepare_driver(url):
    '''Returns a chrome Webdriver.'''
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.ID, 'txtNombre')))
    return driver


def return_rooms(driver, city):
    '''Receives a search_argument to insert it in the search bar and
    then clicks the search button.'''

    search_field = driver.find_element_by_id('txtNombre')
    search_field.send_keys(city + ' Monteria')
    # We look for the search button and click it
    driver.find_element_by_id('btnBuscar')\
        .click()

    driver.implicitly_wait(5)
    driver.find_element_by_xpath("/html/body/div[8]/div[1]/div[1]/form/div/div[4]/div[2]/div[1]/div/div[5]/a").click()
    rooms = driver.find_element_by_xpath('/html/body/div[8]/div/div[1]/form/div/div[4]/table/tbody/tr[9]/td[2]').text

    return rooms

    

if __name__ == '__main__':
    city = "Hotel San Jeronimo"
    try:
        driver = prepare_driver(url)
        return_rooms(driver, city)
    finally:
        driver.quit()
