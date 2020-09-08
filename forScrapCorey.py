import requests
import sqlite3
from bs4 import BeautifulSoup

def get_title(blog):
    return blog.find("h2").find("a").text
        
def get_link(blog):
    return blog.find("h2").find("a")["href"]

def get_date(blog):
    return blog.find("p").find("time").text

def get_description(blog):
    return blog.find("div").find("p").text
    
def start_db():
    global connection, c
    #1 create connection
    connection = sqlite3.connect("coreyblogs.db") 
    #2 create cursor
    c = connection.cursor()

def conncet_db():
    start_db()
    #3 create table
    c.execute("CREATE TABLE coreyblogs (title TEXT, link TEXT,date TEXT, desc TEXT)")
    close_db()

def close_db():
    #4 commit
    connection.commit()
    5#close
    connection.close()

def insert_db(all_blogs):
    start_db()
    c.executemany("INSERT INTO coreyblogs VALUES (?,?,?,?)", all_blogs)
    close_db()



def scrape_blogs(url):
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,"html.parser")
        blogs = soup.find_all("article")
        all_blogs = []
        for blog in blogs:
            blog_data = (get_title(blog),get_link(blog),get_date(blog),get_description(blog))
            all_blogs.append(blog_data)
        print("outsid of for loop")
        conncet_db()
        insert_db(all_blogs)

        if soup.select(".pagination-next"):
            url = soup.select(".pagination-next")[0].find("a")["href"]
            print(f"-----Next page url is: {url}")
        else:
            print("not there!!!")
            break

scrape_blogs("https://coreyms.com/page/1")