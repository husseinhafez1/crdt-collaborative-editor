# CRDT Collaborative Text Editor

A real-time collaborative text editor built with Conflict-Free Replicated Data Types (CRDTs) in Python. This project demonstrates advanced distributed systems concepts and algorithmic complexity that are highly valued in FAANG interviews.

## 🎯 Why This Project Matters

- **Distributed Consistency**: Implements CRDTs to handle concurrent edits without conflicts
- **Real-time Collaboration**: Multiple users can edit simultaneously with automatic conflict resolution
- **Algorithm-Heavy**: Pure algorithmic implementation of CRDT logic, not just glued libraries
- **Industry Relevance**: Similar to Google Docs, VSCode Live Share, Notion, etc.

## 🏗️ Architecture

### Core Components

1. **CRDT Implementation** (`app/crdt.py`): Replicated Growable Array (RGA) for text sequences
2. **Document Management** (`app/document.py`): Document state and operation handling
3. **Session Management** (`app/session.py`): Client session and WebSocket handling
4. **API Layer** (`app/main.py`): FastAPI with REST and WebSocket endpoints

### CRDT Algorithm

The editor uses a **Replicated Growable Array (RGA)** CRDT:
- Each character has a unique identifier (site ID + logical timestamp)
- Characters are ordered in a tree structure
- Insert operations place characters between existing ones
- Delete operations mark characters as deleted (tombstone approach)
- All operations are commutative and associative

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Redis (optional, for multi-instance simulation)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd crdt-collaborative-editor

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Usage

1. **Start the server**: `uvicorn app.main:app --reload`
2. **Open multiple browser tabs** to `http://localhost:8000`
3. **Start typing** in different tabs to see real-time collaboration
4. **Use the REST API** to fetch document state: `GET /api/document`

## 📡 API Endpoints

### REST API
- `GET /api/document` - Get current document state
- `POST /api/document/reset` - Reset document to empty state

### WebSocket API
- `WS /ws/{client_id}` - Real-time collaboration endpoint
- Send operations: `{"type": "insert", "position": 0, "char": "a"}`
- Send operations: `{"type": "delete", "position": 0}`

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_crdt.py
```

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t crdt-editor .

# Run the container
docker run -p 8000:8000 crdt-editor
```

## 🔧 Configuration

### Environment Variables
- `REDIS_URL`: Redis connection string (optional)
- `LOG_LEVEL`: Logging level (default: INFO)

## 📊 Monitoring

The application includes Prometheus metrics:
- `crdt_operations_total`: Total number of CRDT operations
- `crdt_conflicts_resolved`: Number of conflicts resolved
- `active_sessions`: Number of active WebSocket sessions

Access metrics at: `http://localhost:8000/metrics`

## 🧠 CRDT Algorithm Details

### Character Identifiers
Each character has a unique ID: `(site_id, logical_timestamp, random_suffix)`

### Insert Operation
1. Generate unique character ID
2. Find insertion position in the tree
3. Insert character as child of the position's parent
4. Broadcast operation to all clients

### Delete Operation
1. Mark character as deleted (tombstone)
2. Character remains in tree but is not displayed
3. Broadcast deletion to all clients

### Conflict Resolution
- Operations are commutative and associative
- No manual conflict resolution needed
- System automatically converges to consistent state

## 🎯 Stretch Goals

- [ ] Redis integration for multi-instance deployment
- [ ] Text formatting support (bold, italic, etc.)
- [ ] CLI tool for testing collaboration
- [ ] Performance optimization for large documents
- [ ] Cursor position synchronization

## 📚 Learning Resources

- [CRDTs: The Hard Parts](https://martin.kleppmann.com/2020/07/06/crdt-hard-parts-hydra.html)
- [A comprehensive study of CRDTs](https://hal.inria.fr/hal-00932833/file/CRDTs_SSS-2011.pdf)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details. 