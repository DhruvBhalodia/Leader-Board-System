import requests
from bs4 import BeautifulSoup

def get_user_rating(username):
    url = f'https://www.imdb.com/user/{username}/ratings'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        rating_element = soup.find('span', {'class': 'ipl-rating-star__rating'})

        if rating_element:
            return float(rating_element.text)
        else:
            return f"No rating found for user {username}"

    else:
        return f"Failed to fetch data for user {username}. Status code: {response.status_code}"

# Example usage
username_to_check = "example_user"
user_rating = get_user_rating(username_to_check)

print(f"The rating for {username_to_check} is: {user_rating}")
