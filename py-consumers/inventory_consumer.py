"""
Inventory event consumer.
Processes inventory data events from the inventory_data queue.
"""
import json
import logging
from base_consumer import BaseConsumer
from config import Config

logger = logging.getLogger(__name__)


class InventoryConsumer(BaseConsumer):
    """Consumer for inventory data events"""
    
    def __init__(self, data_merger):
        self.data_merger = data_merger
        super().__init__(Config.INVENTORY_QUEUE, self.process_inventory_event)
    
    def process_inventory_event(self, message: dict):
        """
        Process inventory event message.
        
        Expected message format (CanonicalEvent from Java):
        {
            "source": "INVENTORY",
            "timestamp": "2026-02-05T10:30:00Z",
            "payload": {
                "rawData": "{...inventory JSON...}"
            }
        }
        """
        try:
            source = message.get('source')
            timestamp = message.get('timestamp')
            payload = message.get('payload', {})
            raw_data = payload.get('rawData', '{}')
            
            # Parse the embedded JSON string
            inventory_data = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
            
            logger.info(f"Processing inventory event from {source} at {timestamp}")
            
            # Store inventory data for merging
            self.data_merger.add_inventory_data(inventory_data)
            
            logger.info("Inventory data stored for merging")
            
        except Exception as e:
            logger.error(f"Error processing inventory event: {e}", exc_info=True)
            raise
