import os
import glob
import pandas as pd
import re
import nltk
import inflect
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from multiprocessing import Pool
import io
from bs4 import BeautifulSoup


all_filenames = [i for i in glob.glob(r'C:\Users\chris\OneDrive\Desktop\cleaned_transcripts\*')]

p = inflect.engine()
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))
tokenizer = nltk.RegexpTokenizer(r'\w+')

def clean_10ks(txt):
    for txt in all_filenames:
        data = []
        fname = open(txt, encoding='mbcs').read()
        soup = BeautifulSoup(fname, 'html.parser')
        doc = soup.extract().text
        print(os.path.basename(txt))
        new_frame = re.sub('[^a-zA-Z0-9\n\.]', ' ', doc)
        doc = new_frame.lower()
        doc = doc.replace(' 7. ', '')
        doc = ' '.join(doc.split())
        doc = doc.replace('item', '')
        data.append(doc)
        df = pd.DataFrame(data)
        if '.txt' not in os.path.basename(txt): 
            df.to_csv(r'C:\Users\chris\OneDrive\Desktop\{}.txt'.format(os.path.basename(txt)), index=False, header=False)
        else:
            df.to_csv(r'C:\Users\chris\OneDrive\Desktop\{}'.format(os.path.basename(txt)), index=False, header=False)

clean_10ks(all_filenames)

p = Pool(8)
p.map(clean_10ks, all_filenames)
p.terminate()
p.join()
