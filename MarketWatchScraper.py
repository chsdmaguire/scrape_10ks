import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import io
import time



my_dict = {
'GOOGL': r'https://q10k.com/GOOGL/21q2',
'GOOGL': r'https://q10k.com/GOOGL/21q1',
'GOOGL': r'https://q10k.com/GOOGL/20q4',
'GOOGL': r'https://q10k.com/GOOGL/20q3',
'GOOGL': r'https://q10k.com/GOOGL/20q2',
'GOOGL': r'https://q10k.com/GOOGL/20q1'}

for key, value in my_dict.items():
    response = requests.get(value)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.split()
    TenKItem7 = re.sub(r'<.?*>', '', data)
    TenKItem7 = ' '.join(TenKItem7)
    TenKItem7 = TenKItem7.replace('\n', ' ')
    TenKItem7 = TenKItem7.replace('\r', '') 
    TenKItem7 = TenKItem7.replace('&#8217', '')
    TenKItem7 = TenKItem7.replace('&#8212', '')
    TenKItem7 = TenKItem7.replace(' ', ' ') 
    TenKItem7 = TenKItem7.replace('U+00A0', ' ')
    TenKItem7 = TenKItem7.replace(' ', ' ')
    while '  ' in TenKItem7:
        TenKItem7 = TenKItem7.replace('  ', ' ') 
        special_char = ['@', '_', '!', '#', '^', '&', '*', '(', ')', '<', '>', '?', '/', '|', '}', '{', '~', ':', ';', '[', ']']
        for i in special_char:
            file = TenKItem7.replace(i, '')
        with io.open(r'C:\Users\chris\OneDrive\Desktop\{}{}.txt'.format(key, value[-4:]), 'a', encoding='utf-8') as f:
            f.write(str(file))
            print('got file!-> {}'.format(key))
            time.sleep(3)
