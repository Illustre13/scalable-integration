"""
Analytics forwarder service.
Sends merged data to the analytics system with retry logic.
"""
import logging
import requests
import time
from typing import Dict, Any
from config import Config

logger = logging.getLogger(__name__)


class AnalyticsForwarder:
    """
    Forwards enriched data to the analytics system.
    Includes retry logic and error handling.
    """
    
    def __init__(self):
        self.base_url = Config.ANALYTICS_BASE_URL
        self.max_retries = Config.MAX_RETRIES
        self.retry_delay = Config.RETRY_DELAY
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Python-Consumer/1.0'
        })
    
    def send(self, data: Dict[str, Any]) -> bool:
        """
        Send data to analytics system with retry logic.
        
        Args:
            data: Merged data to send
            
        Returns:
            True if successful, False otherwise
        """
        endpoint = f"{self.base_url}/analytics/data"
        
        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(f"Sending data to analytics system (attempt {attempt}/{self.max_retries})")
                
                response = self.session.post(
                    endpoint,
                    json=data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.logger.info(f"Successfully sent data to analytics system")
                    return True
                elif response.status_code == 201:
                    self.logger.info(f"Data created in analytics system")
                    return True
                elif response.status_code >= 400 and response.status_code < 500:
                    # Client error - don't retry
                    self.logger.error(
                        f"Client error sending to analytics: {response.status_code} - {response.text}"
                    )
                    return False
                else:
                    # Server error - retry
                    self.logger.warning(
                        f"Server error from analytics system: {response.status_code} - {response.text}"
                    )
                    
            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout sending to analytics system (attempt {attempt})")
                
            except requests.exceptions.ConnectionError as e:
                self.logger.warning(f"Connection error to analytics system: {e}")
                
            except Exception as e:
                self.logger.error(f"Unexpected error sending to analytics: {e}", exc_info=True)
            
            # Wait before retry (exponential backoff)
            if attempt < self.max_retries:
                delay = self.retry_delay * (2 ** (attempt - 1))
                self.logger.info(f"Waiting {delay}s before retry...")
                time.sleep(delay)
        
        self.logger.error(f"Failed to send data after {self.max_retries} attempts")
        return False
    
    def health_check(self) -> bool:
        """
        Check if analytics system is reachable.
        
        Returns:
            True if system is healthy, False otherwise
        """
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
