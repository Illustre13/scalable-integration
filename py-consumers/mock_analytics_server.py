"""
Mock Analytics Server for testing.
This is a simple Flask server that receives and logs merged data.
In production, this would be your actual analytics system.
"""
from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In-memory storage for demonstration
received_data = []


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/analytics/data', methods=['POST'])
def receive_data():
    """
    Receive merged data from consumers.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Store received data
        entry = {
            'received_at': datetime.now().isoformat(),
            'data': data
        }
        received_data.append(entry)
        
        # Log received data
        logger.info(f"Received merged data:")
        logger.info(f"  - Merged at: {data.get('merged_at')}")
        logger.info(f"  - Customer source: {data.get('metadata', {}).get('customer_source')}")
        logger.info(f"  - Inventory source: {data.get('metadata', {}).get('inventory_source')}")
        logger.info(f"  - Total records received: {len(received_data)}")
        
        return jsonify({
            'status': 'success',
            'message': 'Data received successfully',
            'record_count': len(received_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing data: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/analytics/data', methods=['GET'])
def get_data():
    """
    Retrieve all received data (for testing/verification).
    """
    return jsonify({
        'count': len(received_data),
        'data': received_data
    }), 200


@app.route('/analytics/data/clear', methods=['POST'])
def clear_data():
    """
    Clear all stored data (for testing).
    """
    received_data.clear()
    logger.info("All data cleared")
    return jsonify({'status': 'cleared'}), 200


if __name__ == '__main__':
    logger.info("Starting Mock Analytics Server")
    logger.info("Listening on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
