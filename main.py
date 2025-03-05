import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging
import sys
import argparse
import time
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

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
    logger.info("Health check performed")
    return {"status": "healthy"}

def keep_alive():
    """
    Function to keep the application running by preventing immediate shutdown
    """
    try:
        while True:
            time.sleep(3600)  # Sleep for an hour
    except Exception as e:
        logger.error(f"Keep-alive thread encountered an error: {e}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run FastAPI application")
    parser.add_argument('port', type=int, nargs='?', default=8000, 
                        help='Port to run the application on (default: 8000)')
    
    args = parser.parse_args()
    
    logger.info(f"Starting FastAPI application on port {args.port}")
    
    # Start a keep-alive thread
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # Run the server
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=args.port, 
        log_level="info",
        reload=False  # Disable auto-reload
    )
