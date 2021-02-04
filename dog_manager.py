import requests
import os
import csv
import random

API_KEY = os.environ.get("API_KEY")
SEARCH_URL = "https://api.thedogapi.com/v1/images/search"
BREEDS_URL = "https://api.thedogapi.com/v1/breeds"
HEADER = {"x-api-key": API_KEY}

class Dog:

    def __init__(self, breed, img_url, weight, life_span, temperament):
        self.breed = breed
        self.img = img_url
        self.weight = weight
        self.life_span = life_span
        self.temperament = temperament


class DogManager:

    def __init__(self):
        self.all_breeds = []
        self.get_all_breeds()

    def get_all_breeds(self):
        try:
            with open("breeds/breeds.csv", "r") as file:
                breeds = csv.reader(file)
                self.all_breeds = list(breeds)[0]
        except FileNotFoundError:
            response = requests.get(url=BREEDS_URL, headers=HEADER)
            breed_list = [breed["name"] for breed in response.json()]
            self.all_breeds = breed_list
            with open("breeds/breeds.csv", "w") as file:
                writer = csv.writer(file, dialect="excel")
                writer.writerow(breed_list)

    def new_dog(self):
        finished = False

        while not finished:
            response = requests.get(url=SEARCH_URL, headers=HEADER)
            response = response.json()
            if len(response[0]["breeds"]) > 0:
                breed = response[0]["breeds"][0]["name"]
                img_url = response[0]["url"]
                weight = response[0]["breeds"][0]["weight"]["metric"]
                life_span = response[0]["breeds"][0]["life_span"]
                temperament = response[0]["breeds"][0]["temperament"]
                finished = True
        return Dog(breed=breed, img_url=img_url, weight=weight, life_span=life_span, temperament=temperament)

    def random_breeds(self, number, current_breed):
        breeds_to_return = []
        if len(self.all_breeds) > 0:
            for i in range(number):
                random_breed = random.choice(self.all_breeds)
                if random_breed == current_breed:
                    random_breed = random.choice(self.all_breeds)
                breeds_to_return.append(random_breed)
        else:
            temp_breeds = ['Affenpinscher', 'Afghan Hound', 'African Hunting Dog', 'Airedale Terrier',
                           'Akbash Dog', 'Akita', 'Alapaha Blue Blood Bulldog', 'Alaskan Husky', 'Alaskan Malamute']
            if number <= len(temp_breeds):
                breeds_to_return = random.sample(temp_breeds, number)
            else:
                breeds_to_return = temp_breeds
        breeds_to_return.append(current_breed)
        random.shuffle(breeds_to_return)
        return breeds_to_return
