"""
Quick script to purge RabbitMQ queues.
Run this to clear old binary-serialized messages.
"""
import pika
import sys

def purge_queues():
    """Purge customer_data and inventory_data queues"""
    try:
        # Connection parameters
        credentials = pika.PlainCredentials('illustre', 'ithQW12ink!@')
        parameters = pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
        
        # Connect to RabbitMQ
        print("Connecting to RabbitMQ...")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        # Purge queues
        print("Purging customer_data queue...")
        result1 = channel.queue_purge('customer_data')
        print(f"  ✓ Purged {result1.method.message_count} messages from customer_data")
        
        print("Purging inventory_data queue...")
        result2 = channel.queue_purge('inventory_data')
        print(f"  ✓ Purged {result2.method.message_count} messages from inventory_data")
        
        # Close connection
        connection.close()
        
        print("\n✅ Queues purged successfully!")
        print("\nNext steps:")
        print("1. Restart Java producers: cd java-producers && mvn spring-boot:run")
        print("2. Restart Python consumers: cd py-consumers && python main.py")
        
        return True
        
    except pika.exceptions.AMQPConnectionError as e:
        print(f"\n❌ Failed to connect to RabbitMQ: {e}")
        print("\nMake sure RabbitMQ is running:")
        print("  cd infra && docker compose up")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("RabbitMQ Queue Purge Utility")
    print("=" * 60)
    print()
    
    success = purge_queues()
    sys.exit(0 if success else 1)
