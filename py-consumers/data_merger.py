"""
Data merger service.
Combines customer and inventory data and forwards to analytics system.
"""
import logging
import threading
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)


class DataMerger:
    """
    Merges customer and inventory data from different sources.
    Thread-safe for concurrent consumer operations.
    """
    
    def __init__(self, analytics_forwarder):
        self.analytics_forwarder = analytics_forwarder
        self.customer_data_cache = {}
        self.inventory_data_cache = {}
        self.lock = threading.Lock()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def add_customer_data(self, data: Dict[str, Any]):
        """
        Add customer data to the cache and attempt merge.
        
        Args:
            data: Customer data from CRM system
        """
        with self.lock:
            timestamp = datetime.now().isoformat()
            self.customer_data_cache[timestamp] = data
            self.logger.info(f"Added customer data to cache. Cache size: {len(self.customer_data_cache)}")
            
            # Attempt to merge if we have both datasets
            self._try_merge()
    
    def add_inventory_data(self, data: Dict[str, Any]):
        """
        Add inventory data to the cache and attempt merge.
        
        Args:
            data: Inventory data from Inventory system
        """
        with self.lock:
            timestamp = datetime.now().isoformat()
            self.inventory_data_cache[timestamp] = data
            self.logger.info(f"Added inventory data to cache. Cache size: {len(self.inventory_data_cache)}")
            
            # Attempt to merge if we have both datasets
            self._try_merge()
    
    def _try_merge(self):
        """
        Attempt to merge customer and inventory data when both are available.
        This is a simple strategy - in production, you might want more sophisticated
        matching logic based on timestamps, IDs, or other criteria.
        """
        if not self.customer_data_cache or not self.inventory_data_cache:
            self.logger.debug("Waiting for both customer and inventory data before merging")
            return
        
        try:
            # Get the most recent data from each cache
            # In production, you might want more sophisticated matching
            latest_customer_key = max(self.customer_data_cache.keys())
            latest_inventory_key = max(self.inventory_data_cache.keys())
            
            customer_data = self.customer_data_cache[latest_customer_key]
            inventory_data = self.inventory_data_cache[latest_inventory_key]
            
            # Create merged payload
            merged_data = self._merge_data(customer_data, inventory_data)
            
            # Forward to analytics system
            self.analytics_forwarder.send(merged_data)
            
            # Clean up processed data
            del self.customer_data_cache[latest_customer_key]
            del self.inventory_data_cache[latest_inventory_key]
            
            self.logger.info("Successfully merged and forwarded data")
            
        except Exception as e:
            self.logger.error(f"Error merging data: {e}", exc_info=True)
            raise
    
    def _merge_data(self, customer_data: Dict, inventory_data: Dict) -> Dict:
        """
        Merge customer and inventory data into a unified structure.
        
        Args:
            customer_data: Data from CRM system
            inventory_data: Data from Inventory system
            
        Returns:
            Merged data structure ready for analytics
        """
        merged = {
            "merged_at": datetime.now().isoformat(),
            "customer": customer_data,
            "inventory": inventory_data,
            "metadata": {
                "customer_source": customer_data.get("source", "CRM"),
                "inventory_source": inventory_data.get("source", "InventorySystem"),
                "customer_generated_at": customer_data.get("generated_at"),
                "inventory_generated_at": inventory_data.get("generated_at")
            }
        }
        
        self.logger.debug(f"Merged data structure created")
        return merged
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get current cache statistics.
        
        Returns:
            Dictionary with cache sizes
        """
        with self.lock:
            return {
                "customer_cache_size": len(self.customer_data_cache),
                "inventory_cache_size": len(self.inventory_data_cache)
            }
