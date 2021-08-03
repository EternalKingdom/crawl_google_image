import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time, os

SCROLL_PAUSE_SEC = 1

def scroll_down():
    global driver
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            time.sleep(SCROLL_PAUSE_SEC)
            new_height = driver.execute_script("return document.body.scrollHeight")

            try:
                driver.find_element_by_class_name("mye4qd").click()
            except:

               if new_height == last_height:
                   break

        last_height = new_height

keyword = input('Put your Search Keyword : ')

url = 'https://www.google.com/search?q={}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjgwPKzqtXuAhWW62EKHRjtBvcQ_AUoAXoECBEQAw&biw=768&bih=712'.format(keyword)

os.makedirs("imgs/{}".format(keyword), exist_ok=True)

driver = webdriver.Chrome()
driver.get(url)

time.sleep(1)

scroll_down()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
images = soup.find_all('img', attrs={'class': 'rg_i Q4LuWd'})

print('number of img tags: ', len(images))

for step, i in enumerate(images):
    try:
        imgUrl = i["src"]
    except:
        imgUrl = i["data-src"]

    with urllib.request.urlopen(imgUrl) as f:
        try:
            with open('./imgs/{}/{}_{}.jpg'.format(keyword, keyword, step+1), 'wb') as h:
                img = f.read()
                h.write(img)
        except:
            pass
        print('({}/{})'.format(step+1, len(images)))