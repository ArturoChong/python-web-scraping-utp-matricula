from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys, time

def get_credentials():
    credentials = {'user': '', 'password':''}
    if len(sys.argv) == 3:
        credentials['user'] = str(sys.argv[1])
        credentials['password'] = str(sys.argv[2])
        return credentials
    else:
        return {}

def print_credentials(credentials):
    print(f'User: {credentials["user"]} \nPassword: {credentials["password"]} \n\n')

def attempt_login(url, credentials):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)

    cedula = driver.find_element_by_id('txtCedula')
    password = driver.find_element_by_id('txtClave')
    input_button = driver.find_element_by_id('imgbEnviar')

    cedula.send_keys(credentials['user'])
    password.send_keys(credentials['password'])
    input_button.click()
    
    student_link = driver.find_element_by_xpath('//a[contains(@href, "javascript:perfil")]')
    student_link.click()

    time.wait(10)

    driver.close()

credentials = get_credentials()

if credentials:
    url = 'http://matricula.utp.ac.pa/acceso.aspx'
    attempt_login(url, credentials)
    print("Beginning automated scraping with credentials:")
    print_credentials(credentials)
else:
    print("Credentials are incomplete")
    print("Format is: python3 scrap.py username password")
