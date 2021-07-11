import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64
import htmltolatex
import os

def print_gitbook(base_url:str, method: str, bookname: str):

    page = requests.get(base_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    chapters = soup.find_all("li", class_="chapter")

    dir_path = create_file_folder(bookname)

    chp_name = []
    chp_html = []

    for tag in chapters:

        try:
            int(tag['data-level'])

            h_tag = tag.find_next()
            chp_name.append(h_tag.text)
            chp_html.append(h_tag['href'])
        except:
             pass




    size = len(chp_html)


    file_names = []
    for i in range(size):

        url = base_url + chp_html[i]
        name = clean_file_name(chp_name[i])
        file_names.append(name)

        if(method == "pdf"):
            to_pdf(url, name, dir_path)
        else:
            to_latex(base_url, url, name, dir_path)
            create_main_page(file_names, dir_path)


def to_pdf(url: str, name:str, dir:str):

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

    path = os.path.join(dir, file_name)
    with open(path, "wb") as f:
        f.write(base64.b64decode(pdf['data']))

def to_latex(base_url:str, url: str, name:str, dir: str):

    latex = htmltolatex.scrap_chapter(base_url,url, dir)

    file_name = name + ".tex"

    path = os.path.join(dir, file_name)

    with open(path, 'w', encoding="utf-8") as f:
        f.write(latex)



def clean_file_name(name: str):
    table =["<", ">", ":", '"', "/", "\\", "|", "?", "*"]

    for letter in table:
        name = name.replace(letter, " ")

    name = name.replace(" ", "_")

    return name



def create_file_folder(bookname: str):
    path= bookname
    img_dir = bookname + "\\img"
    try:
        os.makedirs(path)
        os.makedirs(img_dir)
    except:
        print()

    return path

def create_main_page(file_names, dir_path:str):
    latex = ""

    latex += "\\documentclass[letterpaper]{report}\n"
    latex += "\\usepackage{graphicx} \n"
    latex += "\\usepackage{float}\n"
    latex += "\\usepackage{svg} \n"
    latex += "\\usepackage{tabularx} \n"
    latex += "\\usepackage{hyperref} \n"
    latex += "\\UseRawInputEncoding\n"
    latex += "\\usepackage{color}\n"
    latex += "\\usepackage{xcolor, soul, float} \n"
    latex += "\\usepackage[letterpaper, total={7in, 10in}]{geometry}\n"
    latex += "\\sethlcolor{lightgray}\n"

    #colour guide from https://tex.stackexchange.com/questions/176966/put-a-grey-background-behind-code-extracts-in-a-latex-document-like-this-site-d


    #listing config from https://stackoverflow.com/questions/3175105/inserting-code-in-this-latex-document-with-indentation
    latex += "\\usepackage{listings}\n\\usepackage{color}\n"
    latex += "\\definecolor{dkgreen}{rgb}{0,0.6,0}\n\\definecolor{gray}{rgb}{0.5,0.5,0.5}\n\\definecolor{mauve}{rgb}{0.58,0,0.82} \n"
    latex += "\\lstset{\nframe=tb,\nlanguage=R,\naboveskip=3mm, \nbelowskip=3mm, \nshowstringspaces=false,\ncolumns=flexible,basicstyle={\\small\\ttfamily},\nnumbers=none,\nnumberstyle=\\tiny\\color{gray},\nkeywordstyle=\color{blue},\ncommentstyle=\color{dkgreen},\nstringstyle=\color{mauve},\nbreaklines=true,\nbreakatwhitespace=true,\ntabsize=3\n}\n"
    latex += "\n\\begin{document} \n \\setcounter{secnumdepth}{0} \n \\tableofcontents\n\n"

    intag = "\\input{\\"

    for i in range(len(file_names)):
        name = file_names[i]
        latex += intag + name + ".tex}\n\n"


    latex += "\\end{document} \n"

    path = os.path.join(dir_path, "main.tex")

    with open(path, 'w', encoding="utf-8") as f:
        f.write(latex)


