# flow_manager.py
import time
from typing import Dict, Any
from models import TaskResult
from flow_manager import FlowManager
from models import FlowSpec


class FlowManager:
    def __init__(self, flow_spec: FlowSpec, task_registry: Dict[str, Any]):
        self.flow_spec = flow_spec
        self.task_registry = task_registry

        self.conditions_by_source = {}
        for cond in flow_spec.conditions:
            self.conditions_by_source.setdefault(cond.source_task, []).append(cond)

    async def run_flow(self, job_id: str, job_store: Dict[str, Any]):
        context = {"job_id": job_id, "task_results": {}}
        job_store[job_id] = {
            "status": "running",
            "started_at": time.time(),
            "task_order": [],
            "results": {},
        }

        current = self.flow_spec.start_task

        while True:
            if current == "end":
                job_store[job_id]["status"] = "success"
                job_store[job_id]["finished_at"] = time.time()
                return job_store[job_id]

            task = self.task_registry.get(current)
            if not task:
                job_store[job_id]["status"] = "failed"
                job_store[job_id]["message"] = f"Task {current} not found"
                return job_store[job_id]

            job_store[job_id]["task_order"].append(current)

            result: TaskResult = await task.run(context)

            context["task_results"][current] = result.dict()
            job_store[job_id]["results"][current] = result.dict()

            conditions = self.conditions_by_source.get(current, [])
            next_task = None

            for cond in conditions:
                if result.status == cond.outcome:
                    next_task = cond.target_task_success
                    break

            if not next_task:
                next_task = conditions[0].target_task_failure if conditions else "end"

            if result.status == "failure" and next_task == "end":
                job_store[job_id]["status"] = "failed"
                job_store[job_id]["finished_at"] = time.time()
                job_store[job_id]["message"] = f"Flow stopped due to failure in {current}"
                return job_store[job_id]

            current = next_task
