from re import split
import requests
from bs4 import BeautifulSoup
import string
import re
import io
import time
from urllib.error import HTTPError
from multiprocessing import Pool
import pandas as pd

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

# url code involves searching ticker + a special keyword.. chosen words are: stock, operations, company, performance
# prediction, forecast, supplychain, analysis
urls = [r'https://www.google.com/search?q=flws+stock&tbm=nws&ei=k8wRYbS7CcP3-gTf-46ABg',
]

iterator1 = iter(urls)

index = 0

news_sources = []

missed_articles = []

def get_articles(index, url, item):
    while index < len(urls):
        try:
            for url in iterator1:
                response = requests.get(url, header)

                file = response.text

                soup = BeautifulSoup(file, 'html.parser')
                

                for item in soup.find_all('a'):
                    file = item.get('href')
                    if 'policies' not in file and 'support' not in file and  'accounts' not in file and 'url' in file:
                        found_links = file.split("/url?q=")[1]
                        new_links = found_links.split("&sa")[0]
                        title = new_links.split(".com")[1]
                        title = title.replace("/", "")
                        title = title.replace(".html", "")
                        title = title.replace("-", "_")
                        title = title.replace(".", "")
                        print(title)
                        print(new_links)
                        news_sources.append(new_links)
                        time.sleep(5)
            
                        for item in news_sources:
                            if 'nasdaq' not in item:
                                page = requests.get(item)
                                print(page.status_code)
                                # time.sleep(3)
                                soup1 = BeautifulSoup(page.content, 'html.parser')
                                soup2 = soup1.find('body')
                                print('text secured')
                                time.sleep(5)

                                with io.open(r'C:\Users\chris\OneDrive\Desktop\articles\{}.txt'.format(title), 'w+', encoding='utf-8') as f:
                                    for body in soup2.find_all('p'):
                                        article = body.get_text()
                                        article = article.strip()
                                        article = article.replace('\n', ' ')
                                        article = article.replace('\r', '')
                                        f.write(str(article))
                            
                    index += 1    
        except:
            pass
            print('something happened!')
            missed_articles.append(new_links)

    df = pd.DataFrame(missed_articles)
    df.to_csv('missed_articles.csv')

            
        

get_articles(index, iterator1, news_sources)

p = Pool(4)
p.map(get_articles, index, urls, news_sources)
p.terminate()
p.join()
