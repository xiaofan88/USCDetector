import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import json
import secrets
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import WriteData

url = 'https://etherscan.io/accounts/label/old-contract'
login = 'https://etherscan.io/login'

def init(folder, file_name):

    options = uc.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.set_capability("detach", True)

    options.add_argument("--window-size=1920,1050")

    chrome_path = r'D:\Code\USCDetector\etherscan_crawler\chromedriver.exe'

    driver = uc.Chrome(options=options, driver_executable_path=chrome_path)

    driver.get(login)

    time.sleep(60)


    driver.get(url)
    time.sleep(10)

    table = driver.find_element(by=By.ID, value='table-subcatid-0_wrapper')

    show_rows = table.find_element(by=By.NAME, value='table-subcatid-0_length')
    row_select = Select(show_rows)
    time.sleep(1)
    row_select.select_by_value('100')
    time.sleep(5)

    flag = True

    round_times = 0
    while(flag):

        round_times += 1
        print(round_times)

        table = driver.find_element(by=By.ID, value='table-subcatid-0_wrapper')

        tr_list = table.find_element(by=By.TAG_NAME, value='tbody').find_elements(by=By.TAG_NAME, value='tr')

        for tr in tr_list:

            jsonData = json.loads(json.dumps({}))

            td_list = tr.find_elements(by=By.TAG_NAME, value='td')

            address = td_list[0].find_element(by=By.CLASS_NAME, value='js-clipboard').get_attribute('data-clipboard-text')
            
            name_tag = tr.find_element(by=By.CLASS_NAME, value='sorting_1').text
            balance = td_list[2].text
            txn_count = td_list[3].text

            jsonData["address"] = address
            jsonData["name_tag"] = name_tag
            jsonData["balance"] = balance
            jsonData["txn_count"] = txn_count

            WriteData.writeIn(json.dumps(jsonData), f'{folder}/{file_name}')


        time.sleep(2)

        next_btn = table.find_element(by=By.ID, value='table-subcatid-0_next')
        cls_value = next_btn.get_attribute('class')

        if 'disabled' in cls_value:
            flag = False
        else:
            driver.execute_script('arguments[0].click();', next_btn)
            time.sleep(5)



    driver.quit()


folder = "D:/Code/USCDetector"
file_name = "Old-Contracts"

init(folder, file_name)

