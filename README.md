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

Responsibilities:

* Ensure idempotent processing (no duplicate handling)
* Enrich orders with inventory data
* Transform and aggregate data
* Export results to analytics-ready formats (JSON / CSV)

---

## Key Engineering Concepts Demonstrated

* Event-driven architecture
* Polyglot microservices (Java + Python)
* Asynchronous messaging
* Fault tolerance and retries
* Idempotent data processing
* Schema normalization and evolution
* Containerized infrastructure with Docker

---

## Repository Structure

```
scalable-integration-assignment/
├── infra/            # Mock APIs, RabbitMQ, Docker Compose
├── java-producers/            # Spring Boot ingestion services
├── py-consumers/          # Python processing workers
├── .github/                   # CI/CD workflows
└── README.md                  # Project documentation
```

---
