# 📝 CRDT Collaborative Editor Backend

A real-time collaborative text editor backend built with **FastAPI**, **CRDT (Replicated Growable Array)**, and **Redis Pub/Sub**.  
This system enables multiple users to concurrently edit a shared document with strong consistency, low latency, and distributed synchronization.

---

## 🚀 Features

- 🔄 Real-time collaboration via WebSockets  
- 🧠 CRDT-based document model (Replicated Growable Array - RGA)  
- 🌐 REST API for state access and reset  
- 🛰️ Redis Pub/Sub for distributed multi-instance coordination  
- 📊 Prometheus metrics for observability  
- ✅ Comprehensive tests for REST and WebSocket endpoints  

---

## ⚙️ Architecture Overview

- **CRDT Logic** — Handles insert/delete operations using RGA (tombstone-based).  
- **Document Management** — Tracks current state and active client sessions.  
- **Session Manager** — Manages WebSocket connections, routes operations.  
- **Redis Pub/Sub** — Broadcasts operations across multiple backend instances.  
- **FastAPI** — Provides REST and WebSocket interfaces.  


```
[Client] <-- WebSocket --> [FastAPI Backend] <-- Redis Pub/Sub --> [Other Backend Instances]
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/husseinhafez1/crdt-collaborative-editor.git
cd crdt-collaborative-editor
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Redis (for distributed mode)

```bash
redis-server
```

### 5. Run the Backend Server

```bash
uvicorn app.main:app --reload
```

----------

###  Run with Docker Compose (Backend + Redis)

```bash
docker-compose up --build
```

Access the backend at: [http://localhost:8000](http://localhost:8000/)

----------

##  API Usage

### REST Endpoints

-   `GET /api/document` — Fetch current document state
    
-   `POST /api/document/reset` — Reset document to initial state
    
-   `GET /metrics` — Prometheus-compatible metrics
    

### WebSocket Endpoint

-   `ws://<host>:<port>/ws/{client_id}` — Real-time collaboration
    
-   On connection: Client receives full document state
    
-   Clients send/receive CRDT operations (insert/delete)
    

#### Example Operation (Insert)

```json
{
  "type": "insert",
  "char_id": "1:1:abc123",
  "char": "A",
  "parent_id": "root",
  "site_id": 1,
  "logical_timestamp": 1
}

```

----------

##  Testing

Run all tests with:

```bash
pytest tests/
```

-   Tests cover:
    
    -   REST endpoints
        
    -   WebSocket operations
        
    -   Error handling & edge cases
        
-   Each test starts with a fresh document state for isolation.
    

----------

## Project Structure

```
app/
├── crdt.py           # CRDT logic (RGA)
├── document.py       # Document state management
├── session.py        # WebSocket session handling
├── redis_pubsub.py   # Redis Pub/Sub integration
├── utils.py          # Helpers (serialization, validation, etc.)
├── main.py           # FastAPI app with routes
├── metrics.py        # Prometheus integration (optional)
tests/
└── test_api.py       # Unit tests for API and WebSocket logic

Dockerfile            # Docker build
docker-compose.yml    # Orchestration for backend + Redis
requirements.txt      # Python dependencies
```
