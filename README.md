<h1 align="center"> Krishi Connect </h1> <br>
<p align="center">
    <img src="static/Images/final white logo.png" width="280">
  </a>
</p>

<p align="center">
एक कदम सफल कृषि की ओर 
</p>


## Contents

- [About the Project](#about-the-project)
- [Mini Project Upgrade](#mini-project-upgrade)
- [System Architecture](#system-architecture)
- [Top Features](#top-features)
- [How It Is Different](#how-it-is-different)
- [Demo Flow](#demo-flow)
- [Run Locally](#run-locally)
- [UI/UX Design](#uiux-design)
- [Built With](#built-with)
- [Contributors](#contributors)

## About The Project

India is predominantly an agricultural country. Farming is a major occupation in India and one of the biggest 
challenges which comes when a huge workforce is occupied is that it becomes very difficult to provide 
personal attention to every farmer. To help the farmers improve in agricultural sector, we propose a web-based application "कृषि Connect". 
Through the web-app we provide online tele-consultation services as well as offline alternatives for consultation to farmers. They can get support in various agricultural activities, by the help of consultants as well as connect with their peers through the web app. 

## Mini Project Upgrade

This branch upgrades Krishi Connect into a more meaningful farmer assistance mini project. It combines a Django web application, a FastAPI chatbot service, a small agriculture RAG knowledge base, live weather data, and preloaded crop disease samples.

The farmer can:

- Ask crop and disease questions in the Farmer Assistant.
- Get weather-aware advice before spraying or irrigating.
- Analyze preloaded disease samples for rice blast, tomato early blight, and potato late blight.
- Upload a crop image and provide crop, city, and symptom details for guidance.
- View cure steps, prevention steps, confidence, and follow-up chat suggestions.

## System Architecture

```text
Farmer Browser
     |
     | Django pages: assistant, weather, upload, result
     v
Django Web App  ------------------>  Open-Meteo Weather API
     |
     | Chat request
     v
FastAPI Chat Service
     |
     | Retrieval
     v
Local Farmer Knowledge Base
     |
     v
Dynamic crop cure, prevention, and weather-aware answer
```

Main modules:

- `chat_api/`: FastAPI chatbot API with `/chat` and `/health`.
- `chatBackend/farmer_knowledge.py`: crop disease knowledge base.
- `chatBackend/rag_service.py`: retrieval and answer composition.
- `weatherapp/services.py`: live weather forecast integration.
- `imgupload/views.py`: upload and sample diagnosis flow.
- `templates/assistant.html`: farmer chatbot interface.

## Top Features

1. Simple UI- KrishiConnect is aimed to assist the entire farmer population of India through a very easy to understand and convenient layout.


2. Plant Identification-The system identifies the plant from the image and analyzes its health. Response includes : Plant's name and details, Possible disease & their description, Remedies/cures for the disease.


3. Voice Asssistant- In case a farmer has difficulty using the website they can use the voice assistant to navigate the website. They just need to say the the name of the page where they want to go and our voice assistant will take the farmer there.


4. Multilingual- Website is available in English, Hindi and other regional languages. The users can easily switch the language of the entire website using the options in the homepage.

5. Farmer RAG Assistant- Farmers can chat with a local retrieval-based assistant for crop disease cure, irrigation, spraying, and weather-aware precautions. It works without an LLM API key by retrieving from the bundled agriculture knowledge base.

6. Weather API- Weather pages and assistant answers use the Open-Meteo API for live city forecast, humidity, wind, rain chance, and farm advice. No API key is required for this default integration.

7. Preloaded Crop Disease Samples- The project includes rice blast, tomato early blight, and potato late blight sample images. Open Plant Identification and use the sample buttons to see diagnosis, cure, and follow-up chat.

## How It Is Different

- It is not only a static agriculture website; it combines chat, weather, disease guidance, and retrieval-based answers.
- The chatbot runs as a separate FastAPI service, so it can later be reused by a mobile app or external client.
- Weather is used inside farming advice, for example to warn farmers before spraying when rain or wind risk is high.
- The project works without a paid LLM key because it has a local RAG fallback.
- If an LLM endpoint is configured later, the same FastAPI service can generate more natural answers using retrieved crop context.

## Demo Flow

Use this sequence while presenting:

1. Open `http://127.0.0.1:8000`.
2. Go to the Farmer Assistant: `http://127.0.0.1:8000/assistant`.
3. Ask: `My tomato leaves have brown circles. What should I do and can I spray if rain comes?`
4. Show that the answer includes likely disease, symptoms, cure, spray caution, and weather note.
5. Open Plant Identification: `http://127.0.0.1:8000/imgupload`.
6. Click a preloaded sample such as Rice Blast.
7. Show the result page with disease confidence, cure, prevention, and "Chat about cure".
8. Open Weather Forecast: `http://127.0.0.1:8000/weather`.
9. Enter a city and show live forecast plus farm advice.

Short presentation line:

> Krishi Connect helps farmers make faster crop-care decisions by combining a FastAPI chatbot, local RAG crop knowledge, live weather data, and crop disease diagnosis guidance in one simple web app.

## Run Locally

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Start Django and the FastAPI chatbot together:

```bash
./run_project.sh
```

Useful pages:

- Farmer Assistant: http://127.0.0.1:8000/assistant
- Plant upload and samples: http://127.0.0.1:8000/imgupload
- Weather forecast: http://127.0.0.1:8000/weather
- FastAPI chatbot docs: http://127.0.0.1:8001/docs

Optional API keys:

- `PLANTNET_API_KEY` can override the bundled PlantNet key for plant identification.
- Weather uses Open-Meteo by default, so no weather API key is needed.

## UI/UX Design

<img src="UI Design/Layoutpage.png" width="800"> 

## Built With

  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green" height="30px">&nbsp;

  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" height="30px">&nbsp;

  <img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white" height="30px">&nbsp;
  
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" height="30px">&nbsp;
  
  <img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E" height="30px">&nbsp;
  
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" height="30px">&nbsp;



## Contributors

Ashwini Kumar Singh <br>
Satyam Gupta <br>
Adarsh Verma <br>
Prakash Kumar <br>
Abhay Prasad <br>
