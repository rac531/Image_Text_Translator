from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from translate import Translator

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)
CORS(app)

global cv_client

load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')

# Authenticate Azure AI Vision client
cv_client = ImageAnalysisClient(
    endpoint=ai_endpoint,
    credential=AzureKeyCredential(ai_key)
)

@app.route('/api/translate', methods=['POST'])
def translate():
    if 'file' not in request.files:
         return jsonify({'error': 'No image'}), 400
    
    file = request.files['file']
    if file.filename == '':
         return jsonify({'error': 'No selected file'}), 400
    
    language = request.form.get('language')
    if language == '':
        return jsonify({'error': 'No selected language'}), 400

    try:
        #language <- language recieved from the frontend
        fullText = getText(file)
        translatedText = translateText(fullText, language)

        #return the translatedText
        return jsonify({'text': translatedText}), 200
                
    except Exception as ex:
        print(ex)



def getText(image_file):

    image_data = image_file.read()

    # use the cv client to obtain text
    extracted_text = cv_client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ]
    )

    # Append the text into a single string
    fullText = ''
    for line in extracted_text.read.blocks[0].lines:
        fullText += line.text
        fullText += '\n'

    print(fullText)

    # Return the text detected in the image
    return fullText



def translateText(text, targetLanguage):
    # Set a translator for the specified language
    translator = Translator(to_lang=targetLanguage)
    
    # Return the translated text
    return translator.translate(text)
    

if __name__ == "__main__":
    app.run(debug=True)
