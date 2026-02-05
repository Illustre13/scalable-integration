"""
Configuration management for the consumer application.
Loads environment variables and provides typed access to configuration.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # RabbitMQ Settings
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
    RABBITMQ_USERNAME = os.getenv('RABBITMQ_USERNAME', '')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', '')
    
    # Queue Names (matching Java producer configuration)
    CUSTOMER_QUEUE = os.getenv('CUSTOMER_QUEUE', 'customer_data')
    INVENTORY_QUEUE = os.getenv('INVENTORY_QUEUE', 'inventory_data')
    
    # Analytics System
    ANALYTICS_BASE_URL = os.getenv('ANALYTICS_BASE_URL', 'http://localhost:5000')
    
    # Consumer Settings
    PREFETCH_COUNT = int(os.getenv('PREFETCH_COUNT', 1))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 2))  # seconds
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = [
            'RABBITMQ_HOST',
            'RABBITMQ_USERNAME',
            'RABBITMQ_PASSWORD',
        ]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")
