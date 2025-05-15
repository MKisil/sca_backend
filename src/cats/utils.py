import requests


def validate_cat_breed(breed: str) -> bool:
    url = "https://api.thecatapi.com/v1/breeds"
    response = requests.get(url)

    breed = breed.lower()

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from TheCatAPI. Status: {response.status_code}")

    data = response.json()
    if breed in tuple(cat.get("id") for cat in data):
        return True
    return False