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


size = input ("Escolha o seu size (34 - 43): ")
print ("Tamanho escolhido: {}".format(size))


def run(driver):
    try:
        LOGGER.info("Esperando size aparecer...")
        xpath = '//label[@for="tamanho__id{}"]'.format(size)
        wait_until_visible(driver=driver, xpath=xpath)
        try:
            LOGGER.info("Selecionando Size")
            xpath = '//label[@for="tamanho__id{}"]'.format(size)
            wait_until_clickable(driver=driver, xpath=xpath)
            driver.find_element_by_xpath(xpath).click()
            try:
                LOGGER.info("Adicionando ao carrinho")
                xpath = '/html/body/main/div/div[1]/div[3]/div/div[2]/div[4]/div/div[2]/button[1]'
                wait_until_clickable(driver=driver, xpath=xpath)
                driver.find_element_by_xpath(xpath).click()
                sleep(0.1)
                WebDriverWait(driver, 100000).until(EC.url_to_be("https://www.nike.com.br/Carrinho"))
                print("add ao carrinho")
                driver.switch_to.window(driver.window_handles[1])
                try:
                    LOGGER.info("Escolhendo o cartão")
                    sleep(0.5)
                    escolha_cartao = driver.find_element_by_css_selector('.arrow')
                    escolha_cartao.click()
                    try:
                        LOGGER.info("Selecionar MasterCard")
                        escolha_primeiro_cartao = driver.find_element_by_class_name('select-cta-option-text')
                        sleep(0.15)
                        escolha_primeiro_cartao.click()
                        try:
                            LOGGER.info("Clicando em finalizar compra")
                            driver.find_element_by_xpath('//*[@id="confirmar-pagamento"]').click()
                            print("Clicado com sucesso!")
                            while True:
                                try:
                                    LOGGER.info("Inicio do spam")
                                    sleep(2)
                                    xpath1 = '/html/body/div[13]/div/div/div[1]/button/span'
                                    wait_until_clickable(driver=driver, xpath=xpath1)
                                    driver.find_element_by_xpath(xpath1).click()
                                    sleep(2)
                                    try:
                                        xpath2 = '//*[@id="confirmar-pagamento"]'
                                        wait_until_clickable(driver=driver, xpath=xpath2)
                                        driver.find_element_by_xpath(xpath2).click()
                                    except TimeoutException:
                                        LOGGER.info("Erro ao conf pgto LOOP")
                                except TimeoutException:
                                    LOGGER.info("Erro ao fechar box LOOP")                     
                        except TimeoutException:
                            LOGGER.info("Erro ao confirmar pagamento")
                    except TimeoutException:
                        LOGGER.info("Erro ao selecionar Mastercard")
                except TimeoutException:
                    LOGGER.info("Erro ao escolher cartão")  
            except TimeoutException:
                LOGGER.info("Erro ao adiconar ao carrinho")
        except TimeoutException:
            LOGGER.exception("Falha ao selecionar o tamanho do tenis")
    except TimeoutException:
        LOGGER.info("Erro ao carregar grade de sizes. Não está visivel")
                
    

def wait_until_clickable(driver, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))


def wait_until_visible(driver, xpath=None, class_name=None, duration=10000, frequency=0.01):
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
    args = parser.parse_args()

    driver = None
    try:
        if args.driver_type == "chrome":
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:2746")
            #Change chrome driver path accordingly
            chrome_driver = "./bin/chromedriver.exe"
            driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
            print (driver)
        elif args.driver_type == "firefox":
            firefox_options = Options()
            firefox_options.add_experimental_option("debuggerAddress", "127.0.0.1:2746")
            #Change firefox driver path accordingly
            firefox_driver = "./bin/geckodriver_linux"
            driver = webdriver.Firefox(firefox_driver, firefox_options=firefox_options)
            print (driver)
    except:
        print("erro geral mané")

    run(driver=driver)


