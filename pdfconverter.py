from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64

def toPDF(url: str, name:str):

    PATH_TO_DRIVER = "B:\chromedriver_win32\chromedriver.exe"
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options, executable_path=PATH_TO_DRIVER)
    driver.get(url)

    #below code from https://stackoverflow.com/questions/59893671/pdf-printing-from-selenium-with-chromedriver
    pdf = driver.execute_cdp_cmd("Page.printToPDF", {
        "printBackground": True
    })
    file_name = name + ".pdf"
    with open(file_name, "wb") as f:
        f.write(base64.b64decode(pdf['data']))




