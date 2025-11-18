# registry.py
from tasks.fetch_data import FetchDataTask
from tasks.process_data import ProcessDataTask
from tasks.store_data import StoreDataTask

FLOW_REGISTRY = {}
JOB_STORE = {}

TASK_REGISTRY = {
    "task1": FetchDataTask("task1", "Fetch data"),
    "task2": ProcessDataTask("task2", "Process data"),
    "task3": StoreDataTask("task3", "Store data"),
}
