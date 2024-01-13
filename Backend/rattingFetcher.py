import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def get_codechef_profile_image(username):
    url = f'https://www.codechef.com/users/{username}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        profile_image_element = soup.find('img', class_='profileImage')
        
        if profile_image_element:
            profile_image_url = profile_image_element['src']
            # Convert relative URL to absolute URL
            profile_image_url = urljoin(url, profile_image_url)
            return profile_image_url
        else:
            return "Profile image not found for this user"
    else:
        return "User profile not found or inaccessible"
def get_user_rating(username):
    url = f'https://www.codechef.com/users/{username}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rating_element = soup.find('div', class_='rating-number')
        if rating_element:
            return int(re.search(r'\d+', rating_element.text.strip()).group())
        else:
            return "Rating not found for this user"
    else:
        return "User profile not found or inaccessible"

def total_contest(username):
    url = f'https://www.codechef.com/users/{username}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        total = soup.find('div', class_='contest-participated-count')
        return int(re.search(r'\d+', total.text.strip()).group()) if total else "Total contest not found"
    else:
        return "User profile not found or inaccessible"

def extract_id(url_or_username):
    if "://" in url_or_username:
        # If the input is a URL
        parts = url_or_username.split('/')
        return parts[-1] if parts[-1] else parts[-2]
    else:
        # If the input is just a username
        return url_or_username

def get_star_rating(rating):
    if rating < 1400:
        return "⭐"
    elif rating < 1600:
        return "⭐⭐"
    elif rating < 1800:
        return "⭐⭐⭐"
    elif rating < 2000:
        return "⭐⭐⭐⭐"
    elif rating < 2200:
        return "⭐⭐⭐⭐⭐"
    elif rating < 2500:
        return "⭐⭐⭐⭐⭐⭐"
    else:
        return "⭐⭐⭐⭐⭐⭐⭐"

# Read input data from input Excel file
excel_file = './Backend/Sheet.xlsx' 
df = pd.read_excel(excel_file)
output_json = './Backend/data.json'
df.to_json(output_json, orient='records', indent=4)
# Process user data and fetch CodeChef ratings
output_data = []

for _, user in df.iterrows():
    username = ""
    if pd.notna(user['CodeChef ID']) and user['CodeChef ID']:
        username = extract_id(user['CodeChef ID'])
    else:
        continue
    rating = get_user_rating(username)
    rating = int(rating)
    
    star = get_star_rating(rating)
    contests = total_contest(username)
    
    year = int(re.search(r'\d+', user['Email']).group()[:4])
    
    output_user_data = {
        "name": user['Name (First & Last Name)'],
        "year": year,
        "id": username,
        "stars": star,
        "codechefRating": rating,
        "totalContest": contests,
        "img":get_codechef_profile_image(username)
    }
    output_data.append(output_user_data)
    print(f"{user['Name (First & Last Name)']} {rating}")

# Write output data to output JSON file
with open(output_json, 'w') as file:
    json.dump(output_data, file, indent=4)
