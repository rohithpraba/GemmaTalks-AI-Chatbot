# GemmaTalks 💬🧠
A fully offline, real-time AI chatbot built using **Gradio**, **Ollama**, and the **Gemma 3** language model.

## 🚀 Project Overview

**GemmaTalks** is a lightweight, privacy-focused chatbot that runs entirely on your local machine.  
It uses Ollama to serve the **Gemma 3** large language model and Gradio to provide a clean web-based chat interface with **streamed responses**, mimicking modern AI chatbots – without ever sending your data to the cloud.

---

## 🧠 Features

✅ Runs 100% locally – no internet or API keys needed  
✅ Real-time streaming responses for smoother interaction  
✅ Clean UI built with Gradio's `ChatInterface`  
✅ PWA-enabled – install it like an app  
✅ Easy to extend with other models or RAG pipelines

---

## 🧪 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/rohithpraba/GemmaTalks-AI-Chatbot.git
cd GemmaTalks-AI-Chatbot
```

### 2. Install dependencies
```bash
pip install gradio requests
```

### 3. Start Ollama and pull the Gemma model
Make sure Ollama is installed and running:
```bash
ollama run gemma:3b
```
The app will open in your browser. You can chat with the model in real-time!

### 📂 Project Structure
```bash
.
├── app1.py              
├── README.md
```

### 🧭 Future Improvements
 File upload + local document search (RAG)

 Chat history storage

 Custom prompt templates

 Switch between different models (Gemma, LLaMA, Mistral, etc.)

 ### 🙌 Acknowledgements
 Ollama – for simplifying local LLM inference

Gradio – for making UI development super fast

Gemma 3 – open-source LLM by Google


