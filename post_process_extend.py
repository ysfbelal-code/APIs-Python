import requests
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from config import hf_api_key

def gen_image_from_text(prompt):
    #Generates image using Stable Diffusion API

    API_URL = 'https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0'
    headers = {'Authorization': f'Bearer {hf_api_key}'}
    payload = {'inputs': prompt}

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return Image
    else:
        raise Exception(f'Request failed with status code {response.status_code}: {response.text}')
    
def post_process_image(image, edition):
    DAYLIGHT = ['sunrise', 'noon', 'sunset', 'morning', 'daylight', 'day']
    NIGHT = ['midnight', 'evening', 'sunset', 'morning', 'night', 'nighttime']
    
    if edition.lower() in DAYLIGHT:
        print('Setting image effects to default.')
        enhancer = ImageEnhance.Brightness(image)
        bright_image = enhancer.enhance(1.3)
        enhancer = ImageEnhance.Contrast(bright_image)
        contrast_image = enhancer.enhance(1.1)
        soft_focus_image = contrast_image.filter(ImageFilter.GaussianBlur(radius=1))
    elif edition.lower() in NIGHT:
        print('Setting image effects to default.')
        enhancer = ImageEnhance.Brightness(image)
        bright_image = enhancer.enhance(0.9) #1.2 = 20% increase
        enhancer = ImageEnhance.Contrast(bright_image)
        contrast_image = enhancer.enhance(1.4)
        soft_focus_image = contrast_image.filter(ImageFilter.GaussianBlur(radius=0.5))
    else:
        print('Setting image effects to default.')
        enhancer = ImageEnhance.Brightness(image)
        bright_image = enhancer.enhance(1.2) #1.2 = 20% increase
        enhancer = ImageEnhance.Contrast(bright_image)
        contrast_image = enhancer.enhance(1.3)
        soft_focus_image = contrast_image.filter(ImageFilter.GaussianBlur(radius=2))

    return soft_focus_image

def main():
    print('Welcome to the Post-Processing Magic Workshop!')
    print('This program generates an image from text and applies post-processing effects.')
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter a description for your image (or 'exit' to quit): \n")
        if user_input.lower() == 'exit':
            print('Goodbye!')
            break
        try:
            print('\nGenerating image...')
            image = gen_image_from_text(user_input)
            edition=input('Would you like to add daylight/nighttime effects? ').lower()
            print('Applying post-processing effects...\n')
            processedImage = post_process_image(image, edition=edition)
            processedImage.show()

            save_option = input("Do you want to save the image? (yes/no)? ").strip().lower()
            if save_option == 'yes':
                file_name = input('What would you like to name the image file (without extension)? ')
                processedImage.save(f'{file_name}.png')
                print(f'Image saved as {file_name}.png')
            print('-' * 80 + '\n')
        except Exception as e:
            print(f'An error occured: {e}\n')
if __name__ == '__main__':
    main()