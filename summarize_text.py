import requests
from config import hf_api_key
from colorama import Fore, Style, init

init(autoreset=True)

DEFAULT_MODEL = 'google/pegasus-xsum'

def build_api_url(model_name):
    return f'https://api-inference.huggingdace.co/models/{model_name}'

def query(payload, model_name=DEFAULT_MODEL):
    api_url = build_api_url(model_name)
    headers = {'Authorization': f"Bearer {hf_api_key}"}
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

def summarize_text(text, min_length, max_length, model_name=DEFAULT_MODEL):
    payload = {
        'inputs': text,
        'parameters': {'min_length': min_length, 'max_length': max_length}
    }
    print(Fore.BLUE + Style.BRIGHT + f'\n???? Performing AI summarization using model: {model_name}')

    result = query(payload, model_name=model_name)

    if isinstance(result, list) and result and 'summary text' in result[0]:
        return result[0]['summary text']
    else:
        print(Fore.RED + 'Error in summarization response.', result)
        return None

if __name__ == '__main__':
    print(Fore.YELLOW + Style.BRIGHT + "???? Hi there! What's your name?")
    user_name = input("Your name: ").strip()
    if not user_name:
        user_name = 'Guest'
    print(Fore.GREEN + f"Welcome, {user_name}! Let's give your text some AI magic.")

    print(Fore.YELLOW + Style.BRIGHT + "\nPlease enter the text you want to summarize: ")
    user_text = input("> ").strip()

    print(Fore.YELLOW + Style.BRIGHT + "\nEnter the model name you want to use (facebook/bart-large-cnn): ")
    model_choice = input("Model name (leave blank for default): ").strip()
    if not model_choice:
        model_choice = DEFAULT_MODEL

        print(Fore.YELLOW + '\nChoose your summarization style: ')
        print("1. Standard Summary (Quick & Concise)")
        print("2. Enhanced Summary (More Detailed & Refined)")
        style_choice = input('Enter 1 or 2: ').strip()

        if style_choice == '2':
            min_length = 80
            max_length = 200
            print(Fore.BLUE + 'Enhancing summarization process... ????')
        else:
            min_length = 50
            max_length = 150
            print(Fore.BLUE + 'Using standard summarization settings... ????')
        
        summary = summarize_text(user_text, min_length, max_length, model_name=model_choice)

        if summary:
            print(Fore.GREEN + Style.BRIGHT + f"\n???? AI Summarizer Output for {user_name}")
            print(Fore.GREEN + summary)
        else:
            print(Fore.RED + 'Failed to generate summary.')