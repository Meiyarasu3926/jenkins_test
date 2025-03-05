from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI App</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { color: #4CAF50; }
            button { padding: 10px 20px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Welcome to FastAPI App</h1>
        <p>This is a simple FastAPI web application.</p>
        <button onclick="alert('FastAPI is awesome!')">Click Me</button>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
