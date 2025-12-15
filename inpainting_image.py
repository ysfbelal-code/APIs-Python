import requests
from PIL import Image
from io import BytesIO
from config import hf_api_key

def generate_inpainting_image(prompt, image_path, mask_path):
    api_url = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-inpainting'
    headers = {'Authorization': f'Bearer {hf_api_key}'}

    with open(image_path, 'rb') as img_file:
        image_data = img_file.read()
    with open(mask_path, 'rb') as mask_file:
        mask_data = mask_file.read()

        payload = {'inputs': prompt}
        files = {
            'image': ('Base.svg', image_data, 'Image/svg'), 
            'mask': ('Mask.svg', mask_data, 'Image/svg')
        }
        response = requests.post(api_url, headers=headers, data=payload, files=files)
        if response.status_code == 200:
            inpainted_image = Image.open(BytesIO(response.content))
            return inpainted_image
        else:
            raise Exception(f'Request failed with status code {response.status_code}: {response.text}')
        
def main():
    print("Welcome to the Inpainted and Restoration Program! This activity allows you to restore or transform parts of an existing image. Provide a base image, a mask image indicating the areas to modify, and a text prompt describing the desired change. Type 'exit' at any prompt to quit. \n")

    while True:
        prompt = input("Enter a description for the inpainting (or 'exit' to quit):\n")
        if prompt.lower() == 'exit':
            print('Goodbye!')
            break
        image_path = input('Enter the path to the base image (e.g., base_image.svg):\n')
        if image_path.lower() == 'exit':
            break
        mask_path = input('Enter the path to the mask image (e.g., mask_image.svg):\n')
        if mask_path.lower() == 'exit':
            break

        try:
            print("\nProcessing inpainting...")
            result_image = generate_inpainting_image(prompt, image_path, mask_path)
            result_image.show()
            save_option = input("Do you want to save the inpainted image? (yes/no)").strip().lower()
            if save_option == 'yes':
                file_name = input("Enter a namefor the image file (without extension): ").strip()
                result_image.save(f'{file_name}.svg')
                print(f"Image saved as {file_name}.svg\n")
            print('-' * 80 + '\n')
        except Exception as e:
            print(f'An error occured: {e}')

if __name__ == '__main__':
    main()