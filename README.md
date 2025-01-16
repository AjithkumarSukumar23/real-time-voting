# Realtime Election Voting System

## Overview
This project implements a **Realtime Election Voting System** that processes and visualizes real-time voting data using modern streaming and data processing frameworks. Built with **Python**, **Kafka**, **Spark Streaming**, **PostgreSQL**, and **Streamlit**, the system leverages **Docker Compose** for easy deployment. The pipeline is designed for scalability, real-time updates, and interactive visualization.

---

## Project Workflow

### **1. Data Initialization: `main.py`**
- **Database Setup:**  
  Creates PostgreSQL tables: `candidates`, `voters`, and `votes`.
- **Kafka Topic Initialization:**  
  Creates Kafka topics (`votes_topic` and `voters_topic`) and populates the `votes` table into Kafka.
- **Vote Stream Management:**  
  Consumes votes from the Kafka topic and produces enriched data to the `voters_topic`.

---

### **2. Voting Data Generation: `voting.py`**
- **Consumption and Production:**  
  - Consumes data from the `voters_topic` Kafka topic.
  - Generates real-time voting data.
  - Produces the data to the `votes_topic`.

---

### **3. Data Processing: `spark-streaming.py`**
- **Stream Enrichment:**  
  Consumes votes from the `votes_topic` Kafka topic and enriches the data with PostgreSQL.
- **Aggregation:**  
  Aggregates voting data and produces results to specific Kafka topics for real-time insights.

---

### **4. Real-Time Dashboard: `streamlit-app.py`**
- **Data Visualization:**  
  Displays real-time voting data from Kafka topics and PostgreSQL.
- **Interactive Dashboards:**  
  Provides live insights into:
  - Candidates and parties.
  - Voter information.
  - Aggregated voting results.

---

## System Components

| **Component**       | **Description**                                                                                  |
|----------------------|--------------------------------------------------------------------------------------------------|
| `main.py`           | Initializes PostgreSQL, Kafka topics, and manages initial vote streams.                         |
| `voting.py`         | Generates and manages real-time voting data.                                                     |
| `spark-streaming.py`| Enriches and aggregates voting data using Kafka and PostgreSQL.                                  |
| `streamlit-app.py`  | Interactive Streamlit dashboard to visualize real-time voting data.                              |

---

## Prerequisites
- **Python** (3.9 or above)
- **Docker** installed on your machine
- **Docker Compose** installed on your machine

---
