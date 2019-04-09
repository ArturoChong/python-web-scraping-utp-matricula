from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from texttable import Texttable
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

    user_data = obtain_user_data(driver)
    print_user_data(user_data)

    time.sleep(10)

    driver.close()
    return True

def obtain_user_data(driver):
    fields = ['lblnombre', 'lblCedula', 'lblCarrera', 'lblPlan', 'lblAnoEstudio', 'lblIndice', 'lblEstatus', 'lblEmail', 'lblContrasena', 'lblSede', 'lblCitaMatricula']
    user_data = {
        "name": '',
        "cedula": '',
        "career": '',
        "plan": '',
        "year": '',
        "index": '',
        "status": '',
        "email": '',
        "first-password": '',
        "location": '',
        "enrollment-date": ''
    }
    if len(fields) == len(user_data.keys()):
        for index, key in enumerate(user_data.keys()):
            user_data[key] = driver.find_element_by_id(fields[index]).text
        return user_data
    else:
        print("Check code, there might be missing fields!")
        return {}

def print_user_data(user_data):
    print(f'\nPrinting user data for {user_data["name"]}: \n')
    data = [list(item) for item in user_data.items()]
    table = Texttable()
    table.add_rows(data)
    print(table.draw())
    return True

credentials = get_credentials()

if credentials:
    url = 'http://matricula.utp.ac.pa/acceso.aspx'
    print("Beginning automated scraping with credentials:")
    print_credentials(credentials)
    attempt_login(url, credentials)
else:
    print("Credentials are incomplete")
    print("Format is: python3 scrap.py username password")
