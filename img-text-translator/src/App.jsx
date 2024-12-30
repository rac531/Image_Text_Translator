import React, { useState } from "react";
import axios from 'axios';
import './App.css'

function App() {
    const [image, setImage] = useState(null);
    const [text, setText] = useState('');
    const [language, setLanguage] = useState('');
    
    // handle the user uploaded image
    const imageUpload = (e) => {
      console.log(e.target.files);
      setImage(e.target.files[0]);
    }

    // handle the user uploaded language
    const handleLang = (e) => {
      setLanguage(e.target.value);
    }

    // send the image and language to the backend and retrieve the translated text
    const handleTranslate = async() => {
        // construct form
        const formData = new FormData();
        formData.append('file', image);
        formData.append('language', language);

        try {
            // send to the backend
            const response = await axios.post('http://127.0.0.1:5000/api/translate', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
        });

        // retrieve the data recieved from the backend
        setText(response.data.text);
        
      }
        catch (err){
            console.error('Error uploading image', err);
        }
        
    };

    return (
      <div>
      <h1>Upload Image for Translation</h1>
      <div>
        <input type="file" name="file" onChange={imageUpload}/>
      </div>
      <div>
        <label for="languages">Select Language:</label>
        <select value={language} onChange={handleLang}>
          <option value="en">English</option>
          <option value="es">Spanish</option>
          <option value="fr">French</option>
          <option value="de">German</option>
          <option value="it">Italian</option>
          <option value="ko">Korean</option>
          <option value="pt">Portuguese</option>
        </select>
      </div>
      <div>
      <button onClick={handleTranslate}>Translate</button>
      </div>
      {text && (
        <div>
          <h3>Translated Text:</h3>
          <p>{text}</p>
        </div>
      )}
    </div>
      );
}

export default App
