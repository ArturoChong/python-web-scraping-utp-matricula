from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
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

def attempt_login(url, credentials):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('./chromedriver', options=options)
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
    driver.get('http://matricula.utp.ac.pa/estudia/consu_horarioest.asp')

    schedule = obtain_schedule(driver)

    print_data(user_data, schedule)

    driver.close()
    return True

def obtain_schedule(driver):
    header_webdriver = driver.find_elements_by_xpath('//td[contains(@bgcolor, "#FFE2FF")]')
    row_webdriver = driver.find_elements_by_xpath('//font[contains(@size, "1")]')
    headers = [ item.text for item in header_webdriver ]
    rows = [ item.text for item in row_webdriver ]
    schedule = [rows[x:x+8] for x in range(0, len(rows), 8)]
    schedule.insert(0, headers)
    return schedule

def obtain_user_data(driver):
    fields = ['lblnombre', 'lblCedula', 'lblCarrera', 'lblPlan', 'lblAnoEstudio', 'lblIndice', 'lblEstatus', 'lblEmail', 'lblContrasena', 'lblSede', 'lblCitaMatricula']
    user_data = {
        "name": '',
        "cedula": '',
        "career": '',
        "plan": '',
        "year": '',
        "index": '',
        "is_active": '',
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

def print_data(user_data, schedule):
    print(f'\nPrinting user data for {user_data["name"]}: \n')
    data = [list(item) for item in user_data.items()]

    user_table = Texttable()
    user_table.add_rows(data)
    print(user_table.draw())

    print(f'\nPrinting schedule data for {user_data["name"]}: \n')
    schedule_table = Texttable()
    schedule_table.add_rows(schedule)
    print(schedule_table.draw())
    return True

credentials = get_credentials()

if credentials:
    url = 'http://matricula.utp.ac.pa/acceso.aspx'
    print(f"Beginning automated scraping of {url}:")
    attempt_login(url, credentials)
else:
    print("Credentials are incomplete")
    print("Format is: python3 scrap.py username password")
