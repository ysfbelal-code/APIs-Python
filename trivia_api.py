import requests
def get_random_fact():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Full JSON Response: {response.json()}")

        trivia_data = response.json()
        return f"{trivia_data['question']} - {trivia_data['correct_answer']}"
    else:
        return "Failed to retrieve fact."

def main():
    print("Welcome to the Random Fact Generator!")

    while True:
        user_input = input("Press Enter to get a new fact, or type 'q' / 'exit' to quit.").strip().lower()

        if user_input in ('q', 'exit'):
            print('Goodbye!')
            break
        fact = get_random_fact()
        print(fact)

if __name__=='__main__':
    main()