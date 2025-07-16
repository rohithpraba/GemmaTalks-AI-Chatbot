import gradio as gr
import requests
import json 

OLLAMA_URL = "http://localhost:11434/api/chat"

def query_ollama_stream(messages, state):
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    
    messages.append({"role": "assistant", "content": ""})

    try:
        with requests.post(
            OLLAMA_URL,
            json={
                "model": "gemma3",
                "messages": messages[:-1],  
                "stream": True
            },
            stream=True
        ) as response:
            if response.status_code != 200:
                raise ValueError(f"Ollama Error: {response.status_code}")
            
            full_reply_content = ""
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    try:
                        json_data = json.loads(chunk)
                        content = json_data.get("message", {}).get("content", "")
                        full_reply_content += content
                        messages[-1]["content"] = full_reply_content
                        yield messages
                    except json.JSONDecodeError:
                        continue 
            
    except Exception as e:
        messages[-1]["content"] = f"Error: {str(e)}"
        yield messages
    
gr.ChatInterface(
    fn=query_ollama_stream,
    type="messages",
    title="GemmaTalks",
    theme="soft"
).launch(
    pwa=True,
    share=True,
    # favicon_path = r"E:\GemmaTalks\gradio-seeklogo.png"
)