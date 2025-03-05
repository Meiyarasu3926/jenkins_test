import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging
import sys
import signal
import time

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

def signal_handler(signum, frame):
    """
    Handle signals to prevent unexpected shutdown
    """
    logger.info(f"Received signal {signum}. Continuing to run.")

def run_server(host="0.0.0.0", port=8000):
    """
    Run the server with signal handling and persistent mode
    """
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info(f"Starting FastAPI application on port {port}")
    
    # Start the server
    uvicorn.run(
        "main:app", 
        host=host, 
        port=port, 
        log_level="info",
        reload=False  # Explicitly disable reload
    )

if __name__ == "__main__":
    # Allow optional port specification
    import sys
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid port number: {sys.argv[1]}. Using default 8000.")

    # Run the server indefinitely
    while True:
        try:
            run_server(port=port)
            # If server stops, wait and restart
            logger.warning("Server stopped. Restarting in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(5)
