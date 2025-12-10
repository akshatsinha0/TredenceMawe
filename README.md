# Agent Workflow Engine

A minimal graph-based workflow execution system built with FastAPI. This engine allows you to define sequences of processing steps (nodes), connect them via edges, maintain shared state, and execute workflows end-to-end via REST APIs.

## Features

- **Nodes**: Python functions that read and modify shared state
- **State**: Dictionary that flows from one node to another
- **Edges**: Define execution order between nodes
- **Branching**: Conditional routing based on state values
- **Looping**: Repeat nodes until conditions are met
- **Tool Registry**: Register reusable functions for nodes

## Project Structure

```
app/
├── api/
│   └── routes.py       # FastAPI endpoints
├── engine/
│   ├── exceptions.py   # Custom exception classes
│   ├── executor.py     # Workflow execution logic
│   ├── graph_manager.py # Graph creation and validation
│   └── state_manager.py # State management
├── models/
│   ├── api.py          # Request/response models
│   ├── execution.py    # Execution tracking models
│   └── graph.py        # Graph configuration models
├── storage/
│   └── backend.py      # Storage implementations
├── tools/
│   └── registry.py     # Tool registry
├── workflows/
│   └── code_review.py  # Sample workflow
└── main.py             # Application entry point
```

## Installation

```bash
# Clone the repository
git clone https://github.com/akshatsinha0/TredenceMawe.git
cd TredenceMawe

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /graph/create

Creates a new workflow graph.

**Request:**
```json
{
  "config": {
    "name": "my_workflow",
    "nodes": [
      {"name": "step1", "handler": "my_handler"}
    ],
    "edges": [
      {"source": "step1", "target": "step2"}
    ],
    "entry_node": "step1"
  }
}
```

**Response:**
```json
{
  "graph_id": "uuid-string"
}
```

### POST /graph/run

Executes a workflow graph.

**Request:**
```json
{
  "graph_id": "uuid-string",
  "initial_state": {"key": "value"}
}
```

**Response:**
```json
{
  "run_id": "uuid-string",
  "status": "completed",
  "final_state": {"key": "modified_value"},
  "execution_log": [...]
}
```

### GET /graph/state/{run_id}

Returns current state of a workflow run.

**Response:**
```json
{
  "run_id": "uuid-string",
  "status": "running",
  "current_state": {"key": "value"}
}
```

## Sample Workflow: Code Review

The included Code Review workflow demonstrates:

1. **Extract Functions**: Parses code to find function definitions
2. **Check Complexity**: Calculates complexity score
3. **Detect Issues**: Identifies code problems
4. **Suggest Improvements**: Generates recommendations
5. **Loop**: Repeats until quality_score >= threshold

### Example Usage

```python
import requests

# Create the workflow
workflow_config = {
    "config": {
        "name": "code_review",
        "nodes": [
            {"name": "extract", "handler": "extract_functions"},
            {"name": "complexity", "handler": "check_complexity"},
            {"name": "issues", "handler": "detect_issues"},
            {"name": "improve", "handler": "suggest_improvements"}
        ],
        "edges": [
            {"source": "extract", "target": "complexity"},
            {"source": "complexity", "target": "issues"},
            {"source": "issues", "target": "improve"}
        ],
        "entry_node": "extract"
    }
}

response = requests.post("http://localhost:8000/graph/create", json=workflow_config)
graph_id = response.json()["graph_id"]

# Run the workflow
run_request = {
    "graph_id": graph_id,
    "initial_state": {
        "code": "def hello():\n    print('Hello')\n"
    }
}

result = requests.post("http://localhost:8000/graph/run", json=run_request)
print(result.json())
```

## Workflow Engine Capabilities

| Feature | Supported |
|---------|-----------|
| Linear execution | ✓ |
| Conditional branching | ✓ |
| Looping with conditions | ✓ |
| Loop iteration limits | ✓ |
| State persistence | ✓ |
| Execution logging | ✓ |
| Tool registration | ✓ |
| Error handling | ✓ |

## Condition Operators

- `eq`: Equal to
- `ne`: Not equal to
- `gt`: Greater than
- `lt`: Less than
- `gte`: Greater than or equal
- `lte`: Less than or equal

## Future Improvements

- **Async Execution**: Support for async node handlers
- **WebSocket Streaming**: Real-time execution log streaming
- **Persistent Storage**: SQLite/PostgreSQL backend
- **Parallel Nodes**: Execute independent nodes concurrently
- **Subgraphs**: Nested workflow composition
- **Retry Logic**: Automatic retry on node failures
- **Timeout Handling**: Per-node execution timeouts

## License

MIT
