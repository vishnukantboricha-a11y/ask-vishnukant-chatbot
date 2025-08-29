from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # set this in your environment

app = FastAPI()

class ChatIn(BaseModel):
    text: str
    session_id: str | None = None

@app.post("/chat")
async def chat(payload: ChatIn):
    user_text = payload.text
    if openai.api_key is None:
        return {"reply": "OpenAI API key not set on server. Set OPENAI_API_KEY env var."}

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"You are 'Ask Vishnukant', a helpful sales trainer and assistant. Answer concisely in Hindi + simple English when asked."},
            {"role":"user","content": user_text}
        ],
        max_tokens=300
    )
    text = resp['choices'][0]['message']['content']
    return {"reply": text}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
