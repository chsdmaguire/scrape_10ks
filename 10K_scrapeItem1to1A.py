import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define URL for the specific 10K filing
URL_text = r'https://www.sec.gov/Archives/edgar/data/1318605/000156459020004475/0001564590-20-004475.txt' # Tesla 10K Dec 2019

# Grab the response
response = requests.get(URL_text)

# Parse the response (the XML flag works better than HTML for 10Ks)
soup = BeautifulSoup(response.content, 'lxml')

for filing_document in soup.find_all('document'): # The document tags contain the various components of the total 10K filing pack
    
    # The 'type' tag contains the document type
    document_type = filing_document.type.find(text=True, recursive=False).strip()
    
    if document_type == "10-K": # Once the 10K text body is found
        
        # Grab and store the 10K text body
        TenKtext = filing_document.find('text').extract().text
        
        # Set up the regex pattern
        matches = re.compile(r'(item\s(1[\.\s]|2[\.\s])|'
        'business|'
        'properties)', re.IGNORECASE)
                                             
        matches_array = pd.DataFrame([(match.group(), match.start()) for match in matches.finditer(TenKtext)])
        
        # Set columns in the dataframe
        matches_array.columns = ['SearchTerm', 'Start']
        
        # # Get the number of rows in the dataframe
        Rows = matches_array['SearchTerm'].count()
  
        # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
        count = 0 # Counter to help with row location and iteration
        while count < (Rows-1): # Can only iterate to the second last row
            matches_array.at[count,'Selection'] = (matches_array.iloc[count,0] + matches_array.iloc[count+1,0]).lower() # Convert to lower case
            count += 1

        # Set up 'Item 7/8 Search Pattern' regex patterns
        matches_item7 = re.compile(r'(item\s1\.business)')
        matches_item8 = re.compile(r'(item\s2\.properties)')
            
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

   

        # # Extract section of text and store in 'TenKItem7'
        TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]
        
        # Clean newly extracted text
        TenKItem7 = TenKItem7.strip() # Remove starting/ending white spaces
        TenKItem7 = TenKItem7.replace('\n', ' ') # Replace \n (new line) with space
        TenKItem7 = TenKItem7.replace('\r', '')
        TenKItem7 = TenKItem7.replace("'", "") # Replace \r (carriage returns-if you're on windows) with space
        TenKItem7 = TenKItem7.replace(' ', ' ') # Replace " " (a special character for space in HTML) with space
        TenKItem7 = TenKItem7.replace(' ', ' ') # Replace " " (a special character for space in HTML) with space
        while '  ' in TenKItem7:
            TenKItem7 = TenKItem7.replace('  ', ' ') # Remove extra spaces

        # Print first 500 characters of newly extracted text
        print(TenKItem7[:500])
