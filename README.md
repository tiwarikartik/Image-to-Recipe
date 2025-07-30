# 🍲 Image to Recipe Generator

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-orange?style=for-the-badge)](https://www.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge&logo=google)](https://ai.google/gemini/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An intelligent web application that transforms a picture of your kitchen ingredients into a complete, ready-to-cook recipe. Don't know what to make for dinner? Just snap a photo, and let AI be your chef!

## ✨ Features

- **Ingredient Detection**: Upload an image, and the app uses the **Google Gemini 2.5 Flash** model to identify all edible ingredients.
- **AI-Powered Recipe Generation**: Based on the detected ingredients, the app uses **LangChain** and **Gemini Pro** to generate a structured recipe in JSON format.
- **Interactive & Organized UI**: A clean, user-friendly interface built with **Streamlit**, featuring:
  - A responsive sidebar for image uploads.
  - At-a-glance recipe metrics (difficulty, time, category).
  - Collapsible expanders for ingredients, tools, instructions, and macros.

[![Watch the Video](https://img.youtube.com/vi/fVqFvSXqjlc/maxresdefault.jpg)](https://www.youtube.com/watch?v=fVqFvSXqjlc)

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM Orchestration**: [LangChain](https://www.langchain.com/)
- **AI Models**: [Google Gemini Pro](https://ai.google/gemini/) for vision and text generation
- **Environment Management**: [python-dotenv](https://pypi.org/project/python-dotenv/)

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.9 or higher
- A Google API Key with the Gemini API enabled. You can get one from [Google AI Studio](https://makersuite.google.com/).

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/image-to-recipe-generator.git
    cd image-to-recipe-generator
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    Create a `requirements.txt` file with the following content:
    ```txt
    streamlit
    langchain
    langchain-google-genai
    python-dotenv
    ```
    Then, install the packages:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the root of your project and add your Google API key:
    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
    ```

### Running the Application

Launch the Streamlit app with the following command:

```sh
streamlit run app.py
