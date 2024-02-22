from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from time import sleep
import pandas as pd

url = "https://www.magazineluiza.com.br/busca/smartphone/"


service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

try:
    sleep(4)
    dict_book = {"name":[], "price":[]}  
    i = 0
    click_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cgbHmR")))
    last_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sc-kFWlue")))

    while True:
        try:
            sleep(4)
            i += 1
            url_pag = (f"https://www.magazineluiza.com.br/busca/smartphone/?page={i}")
            products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ciMFyT")))

            for product in products:
                name = product.find_element(By.CLASS_NAME, "fbccdO").text.strip()
                price = product.find_element(By.CLASS_NAME, "dOwMgM").text.strip()

                dict_book["name"].append(name)
                dict_book["price"].append(price)
                
                print(name, price)

            print(f"\n{url_pag}\n")

            sleep(2)
            click_button.click()
            sleep(1)

            if "disabled" in last_button.get_attribute("sc-kFWlue"):
                print(f"Page {i} is the last!!!")
                break

        except Exception as er:
            print(f"ERROR:      {er}")

except TimeoutException:
    print(f"No more pages!!!!")

except Exception as er:
    print(f"ERROR:     {er}")

finally:
    driver.quit()

# df = pd.DataFrame(dict_book)
# df.to_csv('C:/Users/xLBKx/Desktop/python_scraping/magalu_celular.csv', encoding='utf-8', sep=';')
