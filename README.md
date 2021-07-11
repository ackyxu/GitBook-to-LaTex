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

Change the link in scraper.print_gitbook() in main.py to choose the textbook you want to retrieve an offline copy.
