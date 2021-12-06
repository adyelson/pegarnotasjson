import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import getpass

login = input("Login: ")
senha = getpass.getpass("Senha: ")
option = Options()
option.headless = True
driver = webdriver.Chrome()#options=option
notas = {}
url="https://minha.unisul.br/psp/pa91prd/EMPLOYEE/CS90PRD/c/U_SISTEMAS_UNISUL.U_MTR_CURSO.GBL"

semestres = {
    '1sem':{'field':'0'},
    '2sem':{'field':'1'},
    '3sem':{'field':'2'},
    '4sem':{'field':'3'},
    'eletiva':{'field':'4'},
    'GAC':{'field':'6'},
}

def pegarnotas(linha):
    time.sleep(2)
    field = semestres[linha]['field']
    driver.find_element(By.XPATH,f"//*[@id='U_MTR_MENU_D_MENULABEL${field}']").click()
    time.sleep(2)   
    element = driver.find_element(By.XPATH,"//*[@id='U_MTR_DSC11_V$scroll$0']/tbody/tr[2]/td/table")
    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')
    
    df_full = pd.read_html(str(table))[0].head(20)
    df = df_full[['UA/Disciplina','Nota','Situação']]
    df.columns = ['Disci','Nota','Sit']
    df = df.fillna("-")
    
    return df.to_dict('records')

driver.get(url)

driver.implicitly_wait(10)
driver.find_element(By.XPATH,"//*[@id='userid']").send_keys(login)
driver.find_element(By.XPATH,"//*[@id='pwd']").send_keys(senha)
driver.find_element(By.XPATH,"//*[@id='login']").submit()

iframe = driver.find_element(By.ID,"ptifrmtgtframe")
driver.switch_to.frame(iframe)

driver.find_element(By.XPATH,"//*[@id='U_MTR_MENU_D_MENULABEL$1']").click()
driver.find_element(By.XPATH,"//*[@id='U_CRS_AND10_V_U_BTN001$0']").click()
driver.implicitly_wait(10)

#loop para buscar todas notas definidas, faz as chamadas da função pegarnotas
for k in semestres:
    notas[k]=pegarnotas(k)
    
driver.quit()

js = json.dumps(notas)
fp= open('Notas.json','w')
fp.write(js)
fp.close




