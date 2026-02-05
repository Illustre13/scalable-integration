# Scalable Systems Integration Project

## Overview

This project is a **real-world capstone simulation** of a scalable systems integration architecture using **heterogeneous technologies** (Java + Python) and **event-driven design**. It demonstrates how independent systems can be decoupled, integrated, and scaled reliably using a message broker as a buffer layer.

The system mimics an enterprise scenario where data from external services (CRM and Inventory systems) must be ingested, processed, enriched, and forwarded to downstream analytics without tight coupling or single points of failure.

---

## What I will be building

An **end-to-end data integration pipeline** consisting of:

1. **Mock External APIs** – Simulated third‑party systems
2. **Java-based Ingestion Services** – Data producers
3. **RabbitMQ Message Broker** – Buffer and decoupling layer
4. **Python-based Processing Services** – Data consumers and transformers

Each component is independently deployable and communicates through well-defined contracts.

---

## High-Level Architecture

```
[ CRM API ]        [ Inventory API ]
     |                    |
     v                    v
[ Java Producers (Spring Boot) ]
               |
               v
        [ RabbitMQ Broker ]
               |
               v
     [ Python Consumers / Workers ]
               |
               v
        [ Analytics / Export Layer ]
```

---

## System Components

### 1. Mock Source APIs (Infrastructure Layer)

These simulate external systems that the organization does not control.

* **CRM API**: Provides customer and order data
* **Inventory API**: Provides product and stock information

They are implemented using **FastAPI** and expose Swagger documentation for contract clarity.

---

### 2. Ingestion Layer – Java (Spring Boot)

These services act as **producers** in the system.

Responsibilities:

* Poll external APIs on a schedule
* Handle failures using circuit breakers and retries
* Normalize data into a canonical JSON event format
* Publish events to RabbitMQ

This layer demonstrates resilience and fault isolation.

---

### 3. Buffer Layer – RabbitMQ

RabbitMQ acts as the **shock absorber** between systems.

Responsibilities:

* Decouple producers from consumers
* Absorb traffic spikes
* Guarantee message delivery
* Support retries and dead-letter queues

This enables each side of the system to scale and fail independently.

---

### 4. Processing Layer – Python Consumers

Python services act as **workers** that consume messages from RabbitMQ.

**Implementation**: `py-consumers/`

Responsibilities:

* Consume events from `customer_data` and `inventory_data` queues
* Ensure idempotent processing (no duplicate handling using MD5 hashing)
* Merge customer and inventory data from multiple sources
* Forward enriched data to analytics systems with retry logic
* Handle concurrent processing with thread-safe operations

**Features**:
- Asynchronous message consumption using `pika`
- Thread-safe data merging with locking mechanisms
- Exponential backoff retry strategy for external API calls
- Graceful shutdown handling (SIGINT/SIGTERM)
- Comprehensive error handling and logging

---

### Message Flow

```
RabbitMQ Queues
    ├── customer_data   → CustomerConsumer
    └── inventory_data  → InventoryConsumer
                              ↓
                        DataMerger (idempotent)
                              ↓
                        AnalyticsForwarder
                              ↓
                        Analytics System
```

### Message Format Example

``` json
{
  "source": "CRM",
  "timestamp": "2026-02-05T10:30:00Z",
  "payload": {
    "rawData": "{...}"
  }
}

```

---

### 5. Repository Structure

```
scalable-integration-assignment/
├── infra/                     # Mock APIs, RabbitMQ, Docker Compose
├── java-producers/            # Spring Boot ingestion services
├── py-consumers/              # Python processing workers
├── .github/                   # CI/CD workflows
└── README.md                  # Project documentation
```

---

## 6. Project Setup Guide

### Prerequisites

Before starting, ensure you have the following installed:

- **Docker Desktop** (for RabbitMQ and WireMock)
- **Java 21+** and **Maven 3.8+**
- **Python 3.8+** and **pip**
- **Git** (for version control)

---

### Step 1: Infrastructure Setup (Docker Containers)

The infrastructure layer runs RabbitMQ (message broker) and WireMock (mock APIs) in Docker containers.

#### 1.1 Start Docker Infrastructure

```bash
cd infra
docker compose up -d
```

This starts:
- **RabbitMQ** on ports `5672` (AMQP) and `15672` (Management UI)
- **WireMock** on port `8393` (Mock CRM & Inventory APIs)

#### 1.2 Verify Infrastructure

**RabbitMQ Management UI:**
- URL: http://localhost:15672
- Username: `your-username` 
- Password: `your-password`
- Check: Queues tab should show `customer_data` and `inventory_data` queues (created automatically)

**WireMock Mock APIs:**
```bash
# Test CRM API
curl http://localhost:8393/customers

# Test Inventory API
curl http://localhost:8393/products

# View OpenAPI documentation
curl http://localhost:8393/openapi.yaml
```

#### 1.3 Stop Infrastructure (when done)

```bash
cd infra
docker compose down
```

---

### Step 2: Java Producers Setup (Spring Boot)

The Java producers poll external APIs and publish events to RabbitMQ.

#### 2.1 Build the Project

```bash
cd java-producers
mvn clean install
```

Expected output:
```
[INFO] BUILD SUCCESS
[INFO] Total time: 15.2 s
```

#### 2.2 Configure Application

The configuration is already set in `src/main/resources/application.yaml`:

```yaml
spring:
  application:
    name: java-producers
  rabbitmq:
    host: localhost
    port: 5672
    username: your-username
    password: your-password

producer:
  crm:
    base-url: http://localhost:8393
  inventory:
    base-url: http://localhost:8393
```

#### 2.3 Run the Producers

```bash
cd java-producers
mvn spring-boot:run
```

**Expected output:**
```
Started JavaProducersApplication in 3.456 seconds
Scheduled customer producer running...
Scheduled inventory producer running...
```

The producers will:
- Poll CRM API every 60 seconds
- Poll Inventory API every 60 seconds
- Publish `CanonicalEvent` messages to RabbitMQ queues

#### 2.4 Verify Messages in RabbitMQ

1. Open RabbitMQ Management UI: http://localhost:15672
2. Go to **Queues** tab
3. Click on `customer_data` queue → should see messages ready/total
4. Click on `inventory_data` queue → should see messages ready/total

---

### Step 3: Python Consumers Setup

The Python consumers process messages from RabbitMQ, merge data, and forward to analytics.

#### 3.1 Setup Virtual Environment

```bash
cd py-consumers

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

#### 3.2 Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**Installed packages:**
- `pika` - RabbitMQ Python client
- `requests` - HTTP client for analytics API
- `python-dotenv` - Environment configuration
- `Flask` - Mock analytics server (dev only)

#### 3.3 Configure Environment

The `.env` file is already configured with default values:

```env
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=your-username
RABBITMQ_PASSWORD=your-password

CUSTOMER_QUEUE=customer_data
INVENTORY_QUEUE=inventory_data

ANALYTICS_BASE_URL=http://localhost:5000
```

#### 3.4 Start Mock Analytics Server (Terminal 1)

```bash
cd py-consumers
python mock_analytics_server.py
```

**Expected output:**
```
Starting Mock Analytics Server
Listening on http://localhost:5000
```

This server receives merged data via REST POST at `/analytics/data`.

#### 3.5 Start Python Consumers (Terminal 2)

```bash
cd py-consumers
python main.py
```

**Expected output:**
```
Starting Python Consumer Application
RabbitMQ Host: localhost:5672
All consumers started successfully
Consuming from queues:
  - customer_data
  - inventory_data
Press CTRL+C to stop
Connected to RabbitMQ queue: customer_data
Connected to RabbitMQ queue: inventory_data
```

The consumers will:
- Connect to both RabbitMQ queues
- Process messages asynchronously (2 threads)
- Merge customer + inventory data
- Forward to analytics system with retry logic
- Handle idempotency with MD5 hashing

---

### Step 4: Verify End-to-End Data Flow

#### 4.1 Check Consumer Logs

You should see logs like:
```
INFO - Received message from customer_data
INFO - Processing customer event from CRM
INFO - Added customer data to cache
INFO - Received message from inventory_data
INFO - Processing inventory event from INVENTORY
INFO - Successfully merged and forwarded data
INFO - Successfully sent data to analytics system
```

#### 4.2 Query Analytics Data

```bash
# Get all merged data
curl http://localhost:5000/analytics/data

# Pretty print with jq (if installed)
curl http://localhost:5000/analytics/data | jq
```

**Expected response:**
```json
{
  "count": 2,
  "data": [
    {
      "received_at": "2026-02-05T15:30:00",
      "data": {
        "merged_at": "2026-02-05T15:30:00.123Z",
        "customer": {
          "source": "CRM",
          "customers": [...]
        },
        "inventory": {
          "source": "InventorySystem",
          "products": [...]
        },
        "metadata": {
          "customer_source": "CRM",
          "inventory_source": "InventorySystem"
        }
      }
    }
  ]
}
```

#### 4.3 Monitor RabbitMQ Queues

- Visit http://localhost:15672/#/queues
- Check message rates (messages/sec)
- Verify both queues are being consumed

---

### Complete Running System

You should have **4 terminals** running:

| Terminal | Component | Command | Port |
|----------|-----------|---------|------|
| 1 | Docker Infrastructure | `cd infra && docker compose up` | 5672, 8393, 15672 |
| 2 | Java Producers | `cd java-producers && mvn spring-boot:run` | 8080 |
| 3 | Mock Analytics Server | `cd py-consumers && python mock_analytics_server.py` | 5000 |
| 4 | Python Consumers | `cd py-consumers && python main.py` | - |

---

### Troubleshooting

#### Problem: Docker containers won't start

```bash
# Check if ports are already in use
netstat -ano | findstr :5672
netstat -ano | findstr :8393

# Stop existing containers
docker compose down

# Remove volumes and restart
docker compose down -v
docker compose up -d
```

#### Problem: RabbitMQ connection refused

```bash
# Wait for RabbitMQ to fully start (30 seconds)
docker logs rabbitmq

# Check RabbitMQ is healthy
docker ps | grep rabbitmq
```

#### Problem: Java build fails

```bash
# Clean Maven cache
cd java-producers
mvn clean

# Rebuild
mvn clean install -U
```

#### Problem: Python import errors

```bash
# Ensure virtual environment is activated
cd py-consumers
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Problem: Messages not flowing

```bash
# Purge queues and restart
cd py-consumers
python purge_queues.py

# Restart Java producers
cd java-producers
mvn spring-boot:run
```

---

### Stopping the System

Stop services in reverse order:

```bash
# 1. Stop Python consumers (Ctrl+C in terminal)
# 2. Stop Mock analytics server (Ctrl+C in terminal)
# 3. Stop Java producers (Ctrl+C in terminal)

# 4. Stop Docker infrastructure
cd infra
docker compose down
```

---

### Next Steps

- **Monitoring**: Add Prometheus metrics for message rates
- **Persistence**: Replace in-memory caching with Redis
- **Scaling**: Run multiple consumer instances
- **Production**: Deploy to Kubernetes with Helm charts

