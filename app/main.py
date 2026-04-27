from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.chatbot import get_ai_response

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("app/static/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        html_content = "<h1>Welcome to E-commerce Chatbot</h1>"
    return HTMLResponse(content=html_content)

@app.get("/checkout", response_class=HTMLResponse)
def checkout():
    try:
        with open("app/static/checkout.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        html_content = "<h1>Checkout Page Not Found</h1>"
    return HTMLResponse(content=html_content)

@app.get("/chat/{message}")
def api_chat(message: str):
    return get_ai_response(message)
