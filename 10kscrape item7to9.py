import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
# import string
import time
from multiprocessing import Pool
# import os
import itertools
import io

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

tickers = ['AAPL', 'GOOGL', 'AMZN', 'FB']

urls = [r'https://www.sec.gov/Archives/edgar/data/320193/00032019320000096/0000320193-20-000096.txt',
r'https://www.sec.gov/Archives/edgar/data/1652044/000165204421000010/0001652044-21-000010.txt',
r'https://www.sec.gov/Archives/edgar/data/1018724/000101872421000004/0001018724-21-000004.txt',
r'https://www.sec.gov/Archives/edgar/data/1326801/000132680121000014/0001326801-21-000014.txt'
]

# def get_files(url, ticker):
    # Grab the response
for (url, ticker) in zip(urls, tickers):
    try: 
        response = requests.get(url, header)

        # Parse the response (the XML flag works better than HTML for 10Ks)
        soup = BeautifulSoup(response.content, 'lxml')

        for filing_document in soup.find_all('document'): # The document tags contain the various components of the total 10K filing pack
            
            # The 'type' tag contains the document type
            document_type = filing_document.type.find(text=True, recursive=False).strip()
            
            if document_type == "10-K": # Once the 10K text body is found
                
                # Grab and store the 10K text body
                TenKtext = filing_document.find('text').extract().text
                
                # Set up the regex pattern
                matches = re.compile(r'(item\s(7[\.\s]|9[\.\s])|'
                                    'discussion\sand\sanalysis\sof\s(consolidated\sfinancial|financial)\scondition|'
                                    'changes\sin\sand\sdisagreements\swith\saccountants\son\saccounting\sand\sfinancial\sdisclosure)', re.IGNORECASE)
                                                    
                matches_array = pd.DataFrame([(match.group(), match.start()) for match in matches.finditer(TenKtext)])
                
                # Set columns in the dataframe
                matches_array.columns = ['SearchTerm', 'Start']
                
                # Get the number of rows in the dataframe
                Rows = matches_array['SearchTerm'].count()
                
                # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
                count = 0 # Counter to help with row location and iteration
                while count < (Rows-1): # Can only iterate to the second last row
                    matches_array.at[count,'Selection'] = (matches_array.iloc[count,0] + matches_array.iloc[count+1,0]).lower() # Convert to lower case
                    count += 1
                
                # Set up 'Item 7/8 Search Pattern' regex patterns
                matches_item7 = re.compile(r'(item\s7\.discussion\s[a-z]*)')
                matches_item8 = re.compile(r'(item\s9\.changes\sin\sand\sdisagreements\swith\saccountants\s[a-z]*)')
                    
                # Lists to store the locations of Item 7/8 Search Pattern matches
                Start_Loc = []
                End_Loc = []
                    
                # Find and store the locations of Item 7/8 Search Pattern matches
                count = 0 # Set up counter
                
                while count < (Rows-1): # Can only iterate to the second last row
                    
                    # Match Item 7 Search Pattern
                    if re.match(matches_item7, matches_array.at[count,'Selection']):
                        # Column 1 = 'Start' columnn in 'matches_array'
                        Start_Loc.append(matches_array.iloc[count,1]) # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)
                    
                    # Match Item 8 Search Pattern
                    if re.match(matches_item8, matches_array.at[count,'Selection']):
                        End_Loc.append(matches_array.iloc[count,1])
                    
                    count += 1

                # Extract section of text and store in 'TenKItem7'
                TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

                # Clean newly extracted text
                TenKItem7 = TenKItem7.strip()
                # Remove starting/ending white spaces
                TenKItem7 = TenKItem7.replace('\n', ' ') # Replace \n (new line) with space
                TenKItem7 = TenKItem7.replace('\r', '') # Replace \r (carriage returns-if you're on windows) with space
                TenKItem7 = TenKItem7.replace('&#8217', '')
                TenKItem7 = TenKItem7.replace('&#8212', '')
                TenKItem7 = TenKItem7.replace(' ', ' ') # Replace " " (a special character for space in HTML) with space
                TenKItem7 = TenKItem7.replace('U+00A0', ' ')
                TenKItem7 = TenKItem7.replace(' ', ' ') # Replace " " (a special character for space in HTML) with space
                while '  ' in TenKItem7:
                    TenKItem7 = TenKItem7.replace('  ', ' ') # Remove extra spaces
                    special_char = ['@', '_', '!', '#', '^', '&', '*', '(', ')', '<', '>', '?', '/', '|', '}', '{', '~', ':', ';', '[', ']']
                    for i in special_char:
                        file = TenKItem7.replace(i, '')
                        with io.open(r'C:\Users\chris\OneDrive\Desktop\10k_scrape_retry\{}.txt'.format(str(ticker)), 'w+', encoding='utf-8') as f:
                            f.write(str(file))
                            print('{}'.format(ticker))
                            time.sleep(3)                          
    except:
        print("exception occured mister!!! -->" '{}'.format(ticker))

# time.sleep(5)

# get_files(tickers, urls)

# p = Pool(4)
# p.map(get_files, tickers, urls)
# p.terminate()
# p.join()
