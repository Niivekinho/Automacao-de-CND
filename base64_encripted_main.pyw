import base64
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui as py
import time
import json

def encode(data):
    try:
        # Standard Base64 Encoding
        encodedBytes = base64.b64encode(data.encode("utf-8"))
        return str(encodedBytes, "utf-8")
    except:
        return ""
    
def decode(data):
    try:
        message_bytes = base64.b64decode(data)
        return message_bytes.decode('utf-8')
    except:
        return ""

your_code = encode("""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui as py
import time
import json
import sys

options = webdriver.ChromeOptions()
userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
options.add_argument(f'user-agent={userAgent}')
options.add_argument("--headless=new")
options.add_argument("--windowed")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--log-level=3') 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 500)

def login():
    email = py.prompt('Qual email deseja usar para acessar o SIEG IRIS?')
    if email == None:
        sys.exit()
    senha = py.password('Senha da conta SIEG IRIS', mask='*')
    if senha == None:
        sys.exit()

    return email, senha

def acessar_IRIS():
    #tenta acessar com  as informações do json, se não for, cria um novo arquivo
    try:
        with open(f"C:/loginIRIS.json", "r") as f:
            email, senha = list(json.load(f).items())[0]
            driver.find_element(By.NAME, 'txtEmail').send_keys(f'{email}')
            driver.find_element(By.NAME, 'txtPassword').send_keys(f'{senha}')
            driver.find_element(By.NAME, 'btnSubmit').click()
            time.sleep(2)

    except FileNotFoundError:
        email, senha = login()
        driver.find_element(By.NAME, 'txtEmail').send_keys(f'{email}')
        driver.find_element(By.NAME, 'txtPassword').send_keys(f'{senha}')
        driver.find_element(By.NAME, 'btnSubmit').click()
        time.sleep(2)

    #Caso apareça na tela "email ou senha errado", ele tenta novamente
    if driver.find_elements(By.XPATH, '//*[@id="form1"]/div[3]/div[1]/div/div[3]'):
        return False
    else:
        #cria um arquivo json no C: com as informações do primeiro login, se entrar
        usr = {email : senha}
        with open(f"C:/loginIRIS.json", "w+") as f:
            json.dump(usr, f)
        return True

if __name__ == '__main__': 
    driver.get("https://hub.sieg.com/IriS/#/Certidoes")
    CNPJ_empresa = py.prompt('Qual empresa deseja baixar os CNDs?(CNPJ apenas números)')
    if CNPJ_empresa == None:
        sys.exit()

    while acessar_IRIS() == False:
        py.alert('Erro! A senha ou e-mail fornecido não é válido. Por favor tente novamente.')
        driver.find_element(By.NAME, 'txtEmail').click()
        driver.find_element(By.NAME, 'txtEmail').clear()#limpa input de email
        driver.find_element(By.NAME, 'txtPassword').click()
        driver.find_element(By.NAME, 'txtPassword').clear()#limpa input de senha

    #buscar empresa e baixar CNDs
    driver.get("https://hub.sieg.com/IriS/#/Certidoes")#abrir IRIS de certidões
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'select2-selection__placeholder'))).click()#abrir busca
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/span/span/span[1]/input"))).send_keys(CNPJ_empresa + Keys.ENTER)#busca
    driver.find_element(By.ID, 'btnDownloadCertidaoLot').click()#faz o download
    time.sleep(25)
    driver.quit()
    py.alert('Download concluído! Confira sua pasta de Downloads. Caso não apareça, tente novamente')


""")
                             
exec(decode(your_code))