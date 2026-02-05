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

See [py-consumers/SETUP.md](py-consumers/SETUP.md) for detailed setup instructions.

---

### Key Engineering Concepts Demonstrated

* Event-driven architecture
* Polyglot microservices (Java + Python)
* Asynchronous messaging
* Fault tolerance and retries
* Idempotent data processing
* Schema normalization and evolution
* Containerized infrastructure with Docker

---

### Repository Structure

```
scalable-integration-assignment/
├── infra/            # Mock APIs, RabbitMQ, Docker Compose
├── java-producers/            # Spring Boot ingestion services
├── py-consumers/          # Python processing workers
├── .github/                   # CI/CD workflows
└── README.md                  # Project documentation
```

### Python Consumers - Event Processing Layer

This module consumes messages from RabbitMQ queues, merges data from multiple sources, and forwards enriched data to downstream analytics systems.

### Features

- **Asynchronous message consumption** from RabbitMQ
- **Idempotency** handling to prevent duplicate processing
- **Data merging** from customer and inventory events
- **Retry logic** for external API calls
- **Concurrent processing** of multiple queues

### Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run consumers**:
   ```bash
   python main.py
   ```

### Architecture

```
RabbitMQ Queues
    ├── customer_data   → CustomerConsumer
    └── inventory_data  → InventoryConsumer
                              ↓
                        DataMerger (with idempotency)
                              ↓
                        AnalyticsForwarder
                              ↓
                        Analytics System
```

### Message Format

Messages follow the `CanonicalEvent` structure from Java producers:

```json
{
  "source": "CRM",
  "timestamp": "2026-02-05T10:30:00Z",
  "payload": {
    "rawData": "{...}"
  }
}
```

---
