"""
Main application entry point.
Runs customer and inventory consumers concurrently.
"""
import logging
import threading
import signal
import sys
from customer_consumer import CustomerConsumer
from inventory_consumer import InventoryConsumer
from data_merger import DataMerger
from analytics_forwarder import AnalyticsForwarder
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('consumer.log')
    ]
)

logger = logging.getLogger(__name__)


class ConsumerApplication:
    """
    Main application that orchestrates all consumers.
    """
    
    def __init__(self):
        self.running = False
        self.consumers = []
        
        # Initialize services
        self.analytics_forwarder = AnalyticsForwarder()
        self.data_merger = DataMerger(self.analytics_forwarder)
        
        # Initialize consumers
        self.customer_consumer = CustomerConsumer(self.data_merger)
        self.inventory_consumer = InventoryConsumer(self.data_merger)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
    
    def start(self):
        """Start all consumers in separate threads"""
        try:
            # Validate configuration
            Config.validate()
            logger.info("Configuration validated successfully")
            
            # Check analytics system health
            if not self.analytics_forwarder.health_check():
                logger.warning("Analytics system health check failed - continuing anyway")
            
            self.running = True
            
            # Create threads for each consumer
            customer_thread = threading.Thread(
                target=self._run_consumer,
                args=(self.customer_consumer, "CustomerConsumer"),
                daemon=True
            )
            
            inventory_thread = threading.Thread(
                target=self._run_consumer,
                args=(self.inventory_consumer, "InventoryConsumer"),
                daemon=True
            )
            
            # Start threads
            logger.info("Starting consumers...")
            customer_thread.start()
            inventory_thread.start()
            
            # Keep main thread alive
            logger.info("=" * 60)
            logger.info("All consumers started successfully")
            logger.info(f"Consuming from queues:")
            logger.info(f"  - {Config.CUSTOMER_QUEUE}")
            logger.info(f"  - {Config.INVENTORY_QUEUE}")
            logger.info("Press CTRL+C to stop")
            logger.info("=" * 60)
            
            # Wait for threads
            customer_thread.join()
            inventory_thread.join()
            
        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")
            self.stop()
        except Exception as e:
            logger.error(f"Error starting application: {e}", exc_info=True)
            self.stop()
            sys.exit(1)
    
    def _run_consumer(self, consumer, name):
        """
        Run a consumer with error handling.
        
        Args:
            consumer: Consumer instance to run
            name: Name for logging
        """
        try:
            logger.info(f"{name} thread started")
            consumer.start_consuming()
        except Exception as e:
            logger.error(f"Error in {name}: {e}", exc_info=True)
            self.stop()
    
    def stop(self):
        """Stop all consumers gracefully"""
        if not self.running:
            return
        
        logger.info("Stopping consumers...")
        self.running = False
        
        try:
            self.customer_consumer.stop()
            self.inventory_consumer.stop()
            
            # Log final statistics
            stats = self.data_merger.get_cache_stats()
            logger.info(f"Final cache statistics: {stats}")
            
            logger.info("Application stopped gracefully")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


def main():
    """Main entry point"""
    logger.info("Starting Python Consumer Application")
    logger.info(f"RabbitMQ Host: {Config.RABBITMQ_HOST}:{Config.RABBITMQ_PORT}")
    logger.info(f"Analytics URL: {Config.ANALYTICS_BASE_URL}")
    
    app = ConsumerApplication()
    app.start()


if __name__ == "__main__":
    main()
