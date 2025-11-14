import requests
import random
import html

AMOUNT = 5
url = f'https://opentdb.com/api.php?amount={AMOUNT}&type=multiple'

def get_edu_questions():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['respond_code'] == 0 and data['results']:
            return data['results']
    return None

def main():
    questions = get_edu_questions()
    if not questions:
        print('Failed to fetch questions.')
        return
    
    score = 0
    print(f'Welcome to the Education Quiz\n')

    for i, q in enumerate(questions, 1):
        question = html.unescape(q['question'])
        correct = html.unescape(q['correct_answer'])
        incorrects = html.unescape(q['incorrect_answers'])

        options = incorrects + [correct]
        random.shuffle(options)

        print(f"Question {i}: {question}")
        for idx, option in enumerate(options, 1):
            print(f' {idx}. {option}')

        while True:
            try:
                choice = int(input("\nYour answer (1-4): "))
                if 1 <= choice <= 4:
                    break
            except ValueError:
                pass
            print('Invalid input! Please enter 1-4')

            if options[choice-1] == correct:
                print('Correct!')
                score = score + 1
            else:
                print(f'Wrong! Correct answer: {correct}\n')
    print(f"Final Score: {score}/{len(questions)}")
    print(f"Percentage: {score/len(questions)*100:.1f}%")

if __name__ == '__main__':
    main()        