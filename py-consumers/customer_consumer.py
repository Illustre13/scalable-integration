"""
Customer event consumer.
Processes customer data events from the customer_data queue.
"""
import json
import logging
from base_consumer import BaseConsumer
from config import Config

logger = logging.getLogger(__name__)


class CustomerConsumer(BaseConsumer):
    """Consumer for customer data events"""
    
    def __init__(self, data_merger):
        self.data_merger = data_merger
        super().__init__(Config.CUSTOMER_QUEUE, self.process_customer_event)
    
    def process_customer_event(self, message: dict):
        """
        Process customer event message.
        
        Expected message format (CanonicalEvent from Java):
        {
            "source": "CRM",
            "timestamp": "2026-02-05T10:30:00Z",
            "payload": {
                "rawData": "{...customer JSON...}"
            }
        }
        """
        try:
            source = message.get('source') 
            timestamp = message.get('timestamp')
            payload = message.get('payload', {})
            raw_data = payload.get('rawData', '{}')
            
            # Parse the embedded JSON string
            customer_data = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
            
            logger.info(f"Processing customer event from {source} at {timestamp}")
            
            # Store customer data for merging
            self.data_merger.add_customer_data(customer_data)
            
            logger.info("Customer data stored for merging")
            
        except Exception as e:
            logger.error(f"Error processing customer event: {e}", exc_info=True)
            raise
