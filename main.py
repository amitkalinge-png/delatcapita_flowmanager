# main.py
from fastapi import FastAPI, HTTPException
import uuid
import asyncio
import time

from models import FlowFile
from registry import FLOW_REGISTRY, JOB_STORE, TASK_REGISTRY
from flow_manager import FlowManager

app = FastAPI(title="Flow Manager Service")


@app.post("/flows/register", status_code=201)
async def register_flow(flow_file: FlowFile):
    fs = flow_file.flow
    if fs.id in FLOW_REGISTRY:
        raise HTTPException(status_code=400, detail="Flow ID already exists")
    FLOW_REGISTRY[fs.id] = fs
    return {"message": "flow registered", "flow_id": fs.id}


@app.post("/flows/{flow_id}/execute", status_code=202)
async def execute_flow(flow_id: str):
    flow_spec = FLOW_REGISTRY.get(flow_id)
    if not flow_spec:
        raise HTTPException(status_code=404, detail="Flow not found")

    job_id = str(uuid.uuid4())
    JOB_STORE[job_id] = {"status": "queued", "flow_id": flow_id}

    manager = FlowManager(flow_spec, TASK_REGISTRY)
    asyncio.create_task(_run(job_id, manager))

    return {"job_id": job_id, "status": "started"}


async def _run(job_id: str, manager: FlowManager):
    try:
        await manager.run_flow(job_id, JOB_STORE)
    except Exception as ex:
        JOB_STORE[job_id] = {
            "status": "failed",
            "message": f"error running job: {ex}",
            "finished_at": time.time(),
        }


@app.get("/jobs/{job_id}")
async def job_status(job_id: str):
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/flows")
async def list_flows():
    return {"flows": list(FLOW_REGISTRY.keys())}


@app.get("/")
def home():
    return {"message": "Flow Manager is running"}
