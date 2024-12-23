from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from translate import Translator

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def main():

    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Authenticate Azure AI Vision client
        cv_client = ImageAnalysisClient(
        endpoint=ai_endpoint,
        credential=AzureKeyCredential(ai_key)
        )

        # Menu for text reading functions       // change and delete
        print('\n1: Use Read API for image (Lincoln.jpg)\n2: Read handwriting (Note.jpg)\nAny other key to quit\n')
        command = input('Enter a number:')
        if command == '1':
            image_file = os.path.join('images','Lincoln.jpg')
            fullText = GetTextRead(image_file)
            print(fullText)
            translatedText = translateText(fullText, 'es')
            print(translatedText)
        elif command =='2':
            image_file = os.path.join('images','Note.jpg')
            fullText = GetTextRead(image_file)
            print(fullText)
            translatedText = translateText(fullText, 'es')
            print(translatedText)
                

    except Exception as ex:
        print(ex)

def GetTextRead(image_file):
    print('\n')

    # Open image file
    with open(image_file, "rb") as f:
            image_data = f.read()

    # Use Analyze image function to read text in image
    result = cv_client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ]
    )

    # add a condition for when there is no text

    # Append the text into a single string
    fullText = ''
    for line in result.read.blocks[0].lines:
        fullText += line.text
        fullText += '\n'

    # Return the text detected in the image
    return fullText


def translateText(text, targetLanguage):
    # Set a translator for the specified language
    translator = Translator(to_lang=targetLanguage)
    
    # Return the translated text
    return translator.translate(text)
    



if __name__ == "__main__":
    main()