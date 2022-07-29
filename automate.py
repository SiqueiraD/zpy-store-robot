import os
import random
import base64
from socket import timeout
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


pathWebDriver = os.path.join(os.path.abspath(os.getcwd()),'chromedriver.exe')
pathDB = os.path.join(os.path.abspath(os.getcwd()),'dados.txt')
scriptC = """
const promisseCLicks = (res) => {
    var limit = parseInt(document.querySelector("#app > section > main > section > div.item_wrap.rule_wrap.fz14 > p:nth-child(2) > span > span").textContent);
    var orders = parseInt(document.querySelector("#app > section > main > section > div.item_wrap.achievements > div > div:nth-child(3) > div > h1").textContent);
    var qtd = limit - orders

    for(i=0;i<qtd;i++){
        setTimeout((t)=>{
                console.log('primeiro ' + t);
                document.querySelector("#app > section > main > section > div.btns.df.fz16.fw600 > span.bg-blue").click();
            setTimeout(()=>{
                console.log('segundo ' + t);
                document.querySelector("#app > section > main > section > div.check_order.fz12.van-popup.van-popup--center > div > div.contain > div > div.btns.df.df_sb.fz14.fw600 > span.btn.submit").click();
                setTimeout(()=>{if (t == (qtd-1))
                    res(parseFloat(document.querySelector("#app > section > main > section > div.item_wrap.achievements > div > div:nth-child(1) > div > h1").textContent))
                },1000)
            },(12000));
            
        },(10000 * i),i);

    }
}
const handlePromisseCLicks = () => new Promise(promisseCLicks)
return await handlePromisseCLicks()
"""


def logar(login,psw):
    driver.get('https://'+ str(base64.b64decode('b25idXkuCg=='), "utf-8") + 'store/#/login')
    driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/input').send_keys(login)
    driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[3]/input').send_keys(psw)
    driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/button').click()
    
def grabOrders():
    # Ordens Completas
    completed = int(driver.find_element(By.XPATH, '//*[@id="app"]/section/main/section/div[3]/div/div[3]/div/h1').text)
    # Limite Ordens
    limit = int(driver.find_element(By.XPATH, '//*[@id="app"]/section/main/section/div[4]/p[2]/span/span').text)
    try:
        timeoutT = (limit - completed) *  11
        if timeoutT > 0:
            driver.set_script_timeout(timeoutT)
            termo = driver.execute_script(scriptC)
            print('Valor Comissão hoje: ' + str(termo))
        else:
            if limit == 0:
                grabOrders()
            else:
                print('ja foi feito')
                print('valor de ontem: ' + driver.find_element(By.XPATH, '/html/body/div[1]/section/main/section/div[3]/div/div[5]/div/h1').text)
                print('valor de hoje: ' + driver.find_element(By.XPATH, '/html/body/div[1]/section/main/section/div[3]/div/div[1]/div/h1').text)
    except Exception as e:
        print('erro de execução do grab:')
        print (e)
        print (e.args)

fd = open(pathDB, 'r')
Lines = fd.readlines()

random.shuffle(Lines)

for line in Lines:
    print('Inicio de execução da conta: ' + line.split()[0])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    try:
        logar(line.split()[0],line.split()[1])
        sleep(2)
        # try:
        #     driver.find_element(By.XPATH, '//*[@id="app"]/section/main/div/div[6]/div[3]/i').click()
        # finally:
        driver.find_element(By.XPATH, '//*[@id="app"]/section/footer/div[3]/div').click()
        sleep(13)
        grabOrders()
    except Exception as e:
        msgFull = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div')
        if msgFull.is_displayed():
            print('Dear user, your order is full, please go to the next room. (Code:T0015)')
        else:
            print('erro geral:')
            print (e)
    finally:
        print('Fim de execução da conta: ' + line.split()[0])
        print('|===========================================================|')
        sleep(1)
        driver.quit()
input('Pressione enter para fechar (algumas vezes rs)...')
