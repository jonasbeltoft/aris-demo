import math
import base64
import pandas as pd
import requests
import os
import re

# Create the 'images' folder if it doesn't exist
if not os.path.exists('backend/data/images'):
    os.makedirs('backend/data/images')

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('backend/data/data.csv')
MAX_ROWS = df.shape[0]

regex = re.compile('[^0-9a-zA-Z ]+')
prev_put_string_len = 0

files = []

# Iterate through each row in the DataFrame and prepare urls
for index, row in df.iterrows():
    # Extract necessary information
    title = row['title']
    published_year = row['published_year']
    thumbnail_url = row['thumbnail']

    # Clean the title to only consist of alphanumerics
    title = regex.sub('', title).replace(' ', '_')
    # Generate the filename
    filename = f'{str(title)}_{published_year}.jpg'.lower()
    
    # Download and save the image in the DataFrame as a blob of bytes
    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            df.at[index, 'thumbnail'] = base64.b64encode(response.content)
        else:
            df.at[index, 'thumbnail'] = '' 
    except:
        df.at[index, 'thumbnail'] = ''

    # Print progress to console
    if int(index) % 20 == 0:
        out_string = f"{index : >5} / {MAX_ROWS : <5} | {'=' * (math.floor((int(index) / MAX_ROWS) * 30)) : <30} | {filename}"
        print(f'{out_string}{" " * abs(prev_put_string_len - len(out_string))}', end='\r')
        prev_put_string_len = len(out_string)

# for i, file in enumerate(files):
#     with open('backend/data/images/'+file[0], 'wb') as f:
#         f.write(file[1])
        
#     # Print progress to console
#     if i % 20 == 0:
#         out_string = f"{index : >5} / {len(files) : <5} | {'=' * (math.floor((int(index) / len(files)) * 30)) : <30} | {file[0]}"
#         print(f'{out_string}{" " * abs(prev_put_string_len - len(out_string))}', end='\r')
#         prev_put_string_len = len(out_string)

# Save the updated DataFrame to the CSV file
df.to_csv('backend/data/data.csv', index=False)
