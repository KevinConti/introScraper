__author__ = 'Kevin'

from bs4 import BeautifulSoup
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import tkinter as tk


BASE_URL = 'http://www.mrmoneymustache.com/blog/'

"""
Accepts: The blog page of MMM's blog (as defined by BASE_URL)
Returns: list of tuples where tuple[0] = title and tuple[1] = url
Possible errors: If the blog's HTML changes. This is the most likely error.
"""
def get_all_articles(section_url):
    html = urllib2.urlopen(section_url).read()
    soup = BeautifulSoup(html, 'lxml')
    all_content = soup.find('section', 'content_area')

    articles = []
    for headline in soup.find_all('h2', 'headline'):
        title = headline.string
        url = headline.a['href']
        title_url = title, url
        articles.append(title_url)
    return articles

"""
Checks to see if there is a new article.
Accepts: list of articles as generated by get_all_articles method (list of tuples where tuple[0] = title and tuple[1] = url)
Returns: Boolean
"""
def is_new_article(articles):
    recentArticle = open('recentArticle', 'r+')
    saved_title = recentArticle.readline()
    first_article = articles[0]
    new_title = first_article[0]
    if saved_title == new_title:
        is_new = False
    else:
        is_new = True
        recentArticle.write(new_title)
    recentArticle.close()
    return is_new

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text="Quit", command = self.quit)
        self.quitButton.grid()
        self.runButton = tk.Button(self, text="Run", command = self.run_program)
        self.runButton.grid()

    def run_program(self):
        articles = get_all_articles(BASE_URL)
        is_new = is_new_article(articles)
        print(is_new)

app = Application()
app.master.title = "Sample App"
app.mainloop()


