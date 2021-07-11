from bs4 import BeautifulSoup
from collections import deque
from pathlib import Path
from urllib.request import urlretrieve
import os
import requests
import bs4
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

def htmltolatex(tags: deque):

    latex = ""






    while(len(tags) != 0):

        tag = tags.popleft()



        if tag.has_attr('class') and tag["class"][0] == "math display":
            latex += convert_to_math_display(tag)
            continue


        if tag.has_attr('class') and (tag['class'][0] == 'title' or tag['class'][0] == "date" or tag['class'][0] == 'author'):
            continue

        if (tag.name == "h1"):
            latex += "\\chapter{" + add_escape(tag.text) + "} \n"

        elif (tag.name == "h2"):
            latex += "\\section{" + add_escape(tag.text) + "} \n"

        elif (tag.name == "h3"):
            latex += "\\subsection{" + add_escape(tag.text) + "} \n"

        elif tag.name == "img":

            img_path = tag['src']
            filename, file_extension = os.path.splitext(img_path)
            if file_extension == ".svg":
                latex += "\\begin{figure}[H]\n\\centering\n\\includegraphics[width=\\textwidth,height=\\textheight,keepaspectratio]{" + filename + ".png" + "}\n\\end{figure}"
                latex += "\n"

            else:
                latex += "\\begin{figure}[H]\n\\centering\n\\includegraphics[width=\\textwidth,height=\\textheight,keepaspectratio]{" + tag['src'] + "}\n\\end{figure}"
                latex += "\n"

        elif(tag.name == "p" or tag.name == "pre"):
            latex += parsestrings(tag)

        elif(tag.name == "ul"):
            latex += "\\begin{itemize} \n"
            latex += parseullist(tag)
            latex += "\\end{itemize} \n"

        elif(tag.name == "ol"):
            latex += "\\begin{enumerate} \n"
            latex += parseullist(tag)
            latex += "\\end{enumerate} \n"

        elif tag.name == "a":
            latex += "\\href{" + tag['href'] + "}{" + add_escape(tag.text) + "}"

        elif tag.name == "table":
            col_count = len(tag.find("tr").findAll("th"))

            latex += "\\begin{tabularx}{\\textwidth}{X*{" + str(col_count) + "}{>{\\raggedright\\arraybackslash}X}}\n \\hline \n"
            latex += make_table_header(tag.find("thead").find("tr").findAll("th"))

            rows = tag.find("tbody").findAll("tr")

            for row in rows:
                latex += make_table_row(row.findAll("td"))

            latex += "\\end{tabularx} \n"






    return latex



#still need to add code blocks
def parsestrings(bs4_strings)->str:

    text = ""
    size = len(bs4_strings)


    for string in bs4_strings:

        # try:
        #     string.name
        # except:
        #     try:
        #         return string.text
        #     except:
        #         continue



        #
        # try:

        if (string.name == "span") :
            class_list = string['class']
            if class_list[0] == "math":
                if class_list[1] == "display":
                    text += add_escape_math(string.text) + "\n"
                if class_list[1] == "inline":
                    text += add_escape_math(string.text)
            continue


        # except:
        #     pass

        if string.name == "ul":
            text += "\n\\begin{itemize} \n"
            text += parseullist(string)
            text += "\\end{itemize}"
            text += "\n"

        elif string.name == "ol":
            text += "\\begin{enumerate} \n"
            text += parseullist(string)
            text += "\\end{enumerate}"
            text += "\n"




        elif string.name == "img":
            img_path = string['src']
            filename, file_extension = os.path.splitext(img_path)



            if file_extension == ".svg":
                text += "\\begin{figure}[H]\n\\centering\n\\includegraphics[width=\\textwidth,height=\\textheight,keepaspectratio]{" + filename + ".png" + "}\n\\end{figure}"
                text += "\n"

            else:
                text += "\\begin{figure}[H]\n\\centering\n\\includegraphics[width=\\textwidth,height=\\textheight,keepaspectratio]{" + string['src'] + "}\n\\end{figure}"
                text += "\n"

        elif string.name == "a":
            text += "\\href{" + string['href'] + "}{" + add_escape(string.text) + "}"
            if size == 1:
                text += "\n"

        elif string.name == "em":
            text += "\\emph{" + add_escape(string.text) + "}"

            if size == 1:
                text += "\n"

        elif string.name == "code":

            if bs4_strings.name == "pre":
                text += "\\begin{lstlisting}[float,floatplacement=H]\n"
                text += string.text
                text += "\n"
                text += "\\end{lstlisting}\n"


            else:
                text +="\\hl{" + add_escape(string.text) + "}"


        elif string.name == "strong":
            text += "\\textbf{" + add_escape(string.text) + "}"


        else:
            try:
                text += add_escape(string.string) + " "
                if size == 1:
                    text += "\n"
            except:
                text += add_escape(string.text) + " "
                if size == 1:
                    text += "\n"

    if bs4_strings.name == "pre" or  bs4_strings.name == "p":
        text += "\n"
    return text


def parseullist(tags):

    latex = ""

    for tag in tags:
        if tag.name == "li":
            latex += "\\item "
            latex += parsestrings(tag)

    return latex


def parseollist(tags):

    latex = ""

    for tag in tags:
        if tag.name == "li":
            latex += "\\item "
            latex += parsestrings(tag)

    return latex

def make_table_header(header):
    row = ""
    for col in header:
        row += "\\textbf{" + add_escape(col.text) + "} & "

    row = row[:-2]

    row += " \\\ \n"

    return row

def make_table_row(column):
    row = ""

    for col in column:
        row += add_escape(col.text) + " & "

    row = row[:-2]

    row += "\\\ \n"

    return row

def add_escape(text: str) -> str:
    table = ['\\',"&" ,"%" ,"$" ,"#" ,"_" ,"{" ,"}" ,"~" ,"^" ]
    escape = "\\"
    for letter in table:
        text = text.replace(letter, (escape + letter))

    return text

def add_escape_math(text: str) -> str:
    # text = text.replace("\\", "\\\\")
    # text = text.replace("\\[", "")
    text = text.replace("\\text", "\\mathrm")



    return text

def scrap_chapter(base_url:str, url: str, cwd: str):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find(class_="page-inner")
    img = soup.findAll("img")
    download_img(img, base_url, cwd)
    q = deque()

    queue = build_queue(body, q)

    return htmltolatex(queue)

def build_queue(body, queue: deque)->deque:
    items = {"img","ul","ol","p", "pre", "table", "h1","h2","h3"}
    for s in body:

        if s.name in items:
            queue.append(s)
        elif isinstance(s, bs4.NavigableString):
            continue
        else:
            build_queue(s.children, queue)

    return queue


def download_img(tags, base_url, dir):

    for tag in tags:
        file = Path(dir + "\\" + tag['src'])
        os.makedirs(os.path.dirname(file), exist_ok=True)
        if file.is_file():
            pass
        else:
            img_url = base_url +"/" + tag['src']
            try:
                urlretrieve(img_url, file)
            except:
                pass
        filename, file_extension = os.path.splitext(file)

        if file_extension == ".svg":
            convert_svg(file)


def convert_svg(path: str):

    filename, file_extension = os.path.splitext(path)
    drawing = svg2rlg(path)
    renderPDF.drawToFile(drawing, filename + ".pdf")
    renderPM.drawToFile(drawing, filename + ".png", fmt="PNG")

def convert_to_math_display(bs4_strings)->str:

    latex = "$"

    for string in bs4_strings:
        latex += string.text

    latex += "$\n"

    return latex









