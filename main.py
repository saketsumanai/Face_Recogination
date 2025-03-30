import logging
import sys
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from app import app
    logger.info("Successfully imported Flask application")
except Exception as e:
    logger.error(f"Failed to import Flask application: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    try:
        logger.info("Starting Flask server...")
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        logger.error(f"Error starting Flask server: {str(e)}")
        traceback.print_exc()
        sys.exit(1)