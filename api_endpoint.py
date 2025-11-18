import requests
import sys

def get_random_fact():

    category = input("Pick the subject of your fact (Animals, History, Science, Technology, Sports). They MUST be written exactly as they are: ")

    url = f"https://apirobots.pro/apis/facts-api/v1/facts/categories/{category}/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Did you know? {data['text']}")
    else:
        print(f'Failed to fetch fact: Error {response.status_code}')

while True:
    user_input = input("Press Enter to get a new fact, or press 'q' to exit. ")
    if user_input == 'q':
        print('Goodbye!')
        sys.exit()

    get_random_fact()