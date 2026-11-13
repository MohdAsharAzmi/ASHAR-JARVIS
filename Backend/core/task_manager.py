
import uuid
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from core.agents import agent_manager


# Background workers
executor = ThreadPoolExecutor(max_workers=4)

# Temporary task storage
tasks = {}
tasks_lock = Lock()


def run_background_task(task_id, agent_name, task):
    try:
        with tasks_lock:
            tasks[task_id]["status"] = "running"
            tasks[task_id]["started_at"] = (
                datetime.now(timezone.utc).isoformat()
            )

        result = agent_manager.run_agent(
            agent_name,
            task=task
        )

        with tasks_lock:
            tasks[task_id]["status"] = "completed"
            tasks[task_id]["result"] = result
            tasks[task_id]["completed_at"] = (
                datetime.now(timezone.utc).isoformat()
            )

    except Exception as error:
        with tasks_lock:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["error"] = str(error)


def submit_task(agent_name, task):
    if agent_manager.get_agent(agent_name) is None:
        raise ValueError("Agent not found: " + agent_name)

    task_id = str(uuid.uuid4())

    with tasks_lock:
        tasks[task_id] = {
            "task_id": task_id,
            "agent": agent_name,
            "task": task,
            "status": "pending",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "result": None,
            "error": None
        }

    executor.submit(
        run_background_task,
        task_id,
        agent_name,
        task
    )

    return get_task(task_id)


def get_task(task_id):
    with tasks_lock:
        task = tasks.get(task_id)

        if task is None:
            return None

        return dict(task)
      
