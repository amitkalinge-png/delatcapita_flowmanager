# Flow Manager Service

A lightweight, extensible **Flow Orchestration Engine** built using **FastAPI**, designed to execute a sequence of tasks based on conditions defined in a JSON flow file.

The service supports:
- Dynamic flow registration
- Sequential task execution
- Conditional branching based on task outcomes
- In-memory job tracking
- Custom task implementations

---

## 🚀 Features

### ✔ Register a Flow  
Upload a JSON definition containing:
- `start_task`
- `tasks` (each with name + description)
- `conditions` that define flow routing

### ✔ Run a Flow  
Execute a registered flow asynchronously.  
Each task result is recorded in job history.


### ✔ Task Registry  
Tasks are modular and extendable:

# To run the code
Install dependencies
    - pip install fastapi uvicorn pydantic
Run the server
    - uvicorn main:app --reload --port 8000

# API Usage
1. Register a flow
curl -X POST "http://localhost:8000/flows/register" \
    -H "Content-Type: application/json" \
    -d @flow.json

2. Execute the flow
curl -X POST "http://localhost:8000/flows/flow123/execute"


3. Check job status
curl http://localhost:8000/jobs/<job_id>

