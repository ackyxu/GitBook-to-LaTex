# GitBook-to-LaTex
Converts the HTML code of a GitBook to a LaTex file


## Purpose of the program?

When I was taking DSCI 100 at UBC, we had access to a free online-textbook written by the Course Creators (thank you!).  
The best part of the course was: all examtions are open-book!  
But since it was during the online-course period (2020), it also means that all exmination are done at home and online.

So why did I want to be able to have a offline copy of the textbook?

1. I was worried about the reliability of the hosting server of the textbook, as 100+ students are trying to access it during the examations
2. I hate reading on my computer, and I especially hate reading textbooks on a web browsers
3. I ran out of ideas for projects to work on

Hence, after 2 semesters that I completed the course, I realize I need the textbook again for my other projects, and so these code was birthed.

## How to use

This program was tested on [Data Science: A First Introduction](https://ubc-dsci.github.io/introduction-to-datascience/).  I asked the instructor for my course for permission to get an offline copy of the textbook, and he was okay with it at the time.  If you are using this code for yourself for this course, make sure to check with your instructor to see if they are okay with it.

As you can tell from the title, the textbook was created using [GitBook](https://www.gitbook.com/).  Because GitBook makes sure that there are some consistent structure to the HTML code, it made it easier to map the HTML tags to LaTex syntax.

There are 4 files Python files in this repository:

1. main.py (your entry to the rest of the code)
2. htmltolatex.py
3. pdfconverter.py
4. scraper.py

There are two varibles for scraper.print_gitbook(), which you need to change in main.py for your build:

1. the link to the textbook you want to retrieve an offline copy.  Point it to the first chapter of the book
2.  either "pdf" if you want a copy of the textbook as if you are printing a pdf file off a webpage, or any string for the program to run in LaTex mode
3.  The name of the directory you wish to store the files in.  It will create a new directory if it does not exsists.

The books will be stored in the root directory of your build, under the directory that you specified in print_gitbook().

This program will retrieve all chapters of the book.

## Packages Used

This program uses the following packages:
- BeautifulSoup 4.9
- Selnium
- Requests
- os
- pathlib
- collections
- svg.lib
- reportlab.graphics

## LaTex Mode

The code maps certain HTML tags in the HTML code to a equalivalent LaTex code.  This is done in htmltolatex.py.
When everything is done, it will create a main.tex file that will create a table of content and combine the chapters together.

You can use this with your LaTex engine to output in a format you desire.  I personally use it to create a PDF file.


## PDF Mode

I am not creative with naming my functions (haha).

What this mode do is that it will retrieve the HTML request in a headless instance of Google Chrome, and print a PDF copy of the page it requested.

This is exactly the same as if you would go to a webpage, right-click and select print, then choose to print as PDF.




