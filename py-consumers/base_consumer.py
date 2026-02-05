"""
Base consumer class for RabbitMQ message processing.
Provides common functionality for all consumers.
"""
import pika
import json
import logging
import hashlib
from typing import Callable
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseConsumer:
    """Base class for RabbitMQ consumers"""
    
    def __init__(self, queue_name: str, callback: Callable):
        self.queue_name = queue_name
        self.callback = callback
        self.logger = logging.getLogger(self.__class__.__name__)
        self.processed_hashes = set()  # In-memory idempotency store
        
        # RabbitMQ connection setup
        self.credentials = pika.PlainCredentials(
            Config.RABBITMQ_USERNAME,
            Config.RABBITMQ_PASSWORD
        )
        self.parameters = pika.ConnectionParameters(
            host=Config.RABBITMQ_HOST,
            port=Config.RABBITMQ_PORT,
            credentials=self.credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        
    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()
            
            # Declare queue (idempotent operation)
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            
            # QoS settings - process one message at a time
            self.channel.basic_qos(prefetch_count=Config.PREFETCH_COUNT)
            
            self.logger.info(f"Connected to RabbitMQ queue: {self.queue_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to RabbitMQ: {e}")
            return False
    
    def is_duplicate(self, message: dict) -> bool:
        """
        Check if message has already been processed.
        Uses MD5 hash for idempotency.
        
        Note: In production, use Redis or a database for persistent storage.
        """
        message_hash = hashlib.md5(
            json.dumps(message, sort_keys=True).encode()
        ).hexdigest()
        
        if message_hash in self.processed_hashes:
            return True
        
        self.processed_hashes.add(message_hash)
        return False
    
    def process_message(self, ch, method, properties, body):
        """
        Main message processing callback.
        Handles deserialization, idempotency, and error handling.
        """
        try:
            # Deserialize message
            message = json.loads(body)
            
            self.logger.info(f"Received message from {self.queue_name}")
            self.logger.debug(f"Message content: {message}")
            
            # Check for duplicates
            if self.is_duplicate(message):
                self.logger.warning(f"Skipping duplicate message")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            # Process message using provided callback
            self.callback(message)
            
            # Acknowledge successful processing
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.logger.info(f"Successfully processed message from {self.queue_name}")
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in message: {e}")
            # Reject and don't requeue malformed messages
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}", exc_info=True)
            # Don't acknowledge - message will be requeued
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def start_consuming(self):
        """Start consuming messages from the queue"""
        if not hasattr(self, 'channel'):
            if not self.connect():
                raise ConnectionError("Failed to connect to RabbitMQ")
        
        self.logger.info(f"Starting to consume from {self.queue_name}")
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.process_message
        )
        
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.logger.info("Consumer stopped by user")
            self.stop()
        except Exception as e:
            self.logger.error(f"Error in consumer: {e}")
            self.stop()
            raise
    
    def stop(self):
        """Stop consuming and close connection"""
        try:
            if hasattr(self, 'channel') and self.channel.is_open:
                self.channel.stop_consuming()
                self.channel.close()
            if hasattr(self, 'connection') and self.connection.is_open:
                self.connection.close()
            self.logger.info("Consumer stopped gracefully")
        except Exception as e:
            self.logger.error(f"Error stopping consumer: {e}")
