import math
from time import sleep
import pandas as pd
import requests
import os

# Create the 'images' folder if it doesn't exist
if not os.path.exists('data/images'):
    os.makedirs('data/images')

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('data/data.csv')
MAX_ROWS = df.shape[0]

# Function to download and save an image
def download_image(url, filename):
    try:
        response = requests.get(url)
    except:
        return
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)


prev_put_string_len = 0
# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Extract necessary information
    title = row['title']
    published_year = row['published_year']
    thumbnail_url = row['thumbnail']

    # Generate the filename
    filename = f'{str(title)}_{published_year}.jpg'.lower()
    
    # Download and save the image
    download_image(thumbnail_url, 'data/images/'+filename)

    # Update the 'thumbnail' column with the new filename
    df.at[index, 'thumbnail'] = filename
    
    out_string = f"{index : >5} / {MAX_ROWS : <5} | {'=' * (math.floor((int(index) / MAX_ROWS) * 30)) : <30} | {filename}"
    
    print(f'{out_string}{" " * abs(prev_put_string_len - len(out_string))}', end='\r')
    prev_put_string_len = len(out_string)

# Save the updated DataFrame to the CSV file
df.to_csv('data/data.csv', index=False)
