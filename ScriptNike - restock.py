# coding=utf-8
import os
import sys
import six
import pause
import argparse
import logging.config
from time import sleep
from selenium import webdriver
from dateutil import parser as date_parser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [PID %(process)d] [Thread %(thread)d] [%(levelname)s] [%(name)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
})

NIKE_HOME_URL = "https://www.nike.com.br/Snkrs"
CHECK_OUT_URL = "https://www.nike.com.br/Checkout"
LOGGER = logging.getLogger()





def run(driver):
    try:
        x = True
        LOGGER.info("Clicando")
        xpath1 = '//*[@id="confirmar-pagamento"]'
        xpath2 = '//*[@id="errorModal"]/div/div/div[3]/button'
        while x == True:
            wait_until_visible(driver=driver, xpath=xpath1)
            wait_until_clickable(driver=driver, xpath=xpath1)
            driver.find_element_by_xpath(xpath1).click()
            sleep(0.5)
            
            wait_until_visible(driver=driver, xpath=xpath2)
            print("Achei!")
            wait_until_clickable(driver=driver, xpath=xpath2)
            print("Clicavel")
            sleep(0.5)
            driver.find_element_by_xpath(xpath2).click()
            print("cliquei")
            sleep(1)
            
            
        #botão aguardar ban ip disable codigo: <button id="confirmar-pagamento" href="#" title="" class="button btn-confirmar" disabled="disabled">Aguarde...</button>
        #//*[@id="errorModal"]/div/div/div[3]/button (XPATH BOTAO ESTOQUE ESGOTADO)
        #/html/body/div[15]/div/div/div[3]/button (FULLXPATH)
    except TimeoutException:
        LOGGER.info("Erro no Clicker")
                
    

def wait_until_clickable(driver, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))


def wait_until_visible(driver, xpath=None, class_name=None, duration=20000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))       
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=False)
    parser.add_argument("--password", required=False)
    parser.add_argument("--url", required=False)
    parser.add_argument("--shoe-size", required=False)
    parser.add_argument("--login-time", default=None)
    parser.add_argument("--release-time", default=None)
    parser.add_argument("--screenshot-path", default=None)
    parser.add_argument("--html-path", default=None)
    parser.add_argument("--page-load-timeout", type=int, default=2)
    parser.add_argument("--driver-type", default="chrome", choices=("firefox", "chrome"))
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--select-payment", action="store_true")
    parser.add_argument("--purchase", action="store_true")
    parser.add_argument("--num-retries", type=int, default=1)
    parser.add_argument('--proxy-server=localhost:8118')
    args = parser.parse_args()

    driver = None
    try:

            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:2746")
            #Change chrome driver path accordingly
            chrome_driver = "./bin/chromedriver.exe"
            driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
            print (driver)
    
    except:
        print("erro geral mané")
        input()

    run(driver=driver)


