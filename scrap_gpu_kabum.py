from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import math
from time import sleep
import pandas as pd

url = "https://www.kabum.com.br/hardware/placa-de-video-vga"

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

try:
    quantidade = int(driver.find_element(By.ID, "listingCount").text.strip().split('p')[0])
    ultima_pagina = math.ceil(int(quantidade) / 20)

    dict_gpu = {"nome": [], "valor": []}
        
    for i in range(1, ultima_pagina+1):
        try:     
            sleep(4)
            url_pag = (f"https://www.kabum.com.br/hardware/placa-de-video-vga?page_number={i}&page_size=20&facet_filters=&sort=most_searched")
            all_gpus = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "productCard")))
    
            for all_gpu in all_gpus:
                try:
                    nome = all_gpu.find_element(By.CLASS_NAME, "nameCard").text.strip()
                    valor = all_gpu.find_element(By.CLASS_NAME, "priceCard").text.strip().replace('----', 'N/A')

                    dict_gpu["nome"].append(nome)
                    dict_gpu["valor"].append(valor)
                        
                    print(nome, valor)
                    
                except StaleElementReferenceException:
                    nome = all_gpu.find_element(By.CLASS_NAME, "nameCard").text.strip()
                    valor = all_gpu.find_element(By.CLASS_NAME, "priceCard").text.strip()

                    dict_gpu["nome"].append(nome)
                    dict_gpu["valor"].append(valor)
                        
                    print(nome, valor)

            print(f"\n{url_pag}\n")
                
            clica_bt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next")))
            sleep(1)
            clica_bt.click()
            sleep(1)

        except Exception as er:
            print(f"ERROR:     {er}")
            
except Exception as er:
    print(f"ERROR:     {er}")

finally:
    driver.quit()

df = pd.DataFrame(dict_gpu)
df.to_csv('C:/Users/xLBKx/Desktop/python_scraping/tabela_gpu2.csv', encoding='utf-8', sep=';')