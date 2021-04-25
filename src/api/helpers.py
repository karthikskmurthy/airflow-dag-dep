import json
import yaml
from collections import defaultdict

import requests

from constants import HEADERS


def parse_yaml(file_path):
    """

    Parse the yaml file and return the dictionary.

    Args:
        file_path: file path of yaml file

    Returns:
        Dictionary representation of yaml file
    """
    with open(file_path) as file:
        config = yaml.load(file)
    return config


def get_dags():
    """
    Fetch all dags from the airflow setup and returns as a list of dag ids.

    Returns:
        List of dag ids
    """
    dag_list = {}
    try:
        config = parse_yaml("config.yml")
        host = config["airflow"]["host"]
        url = f"http://{host}/api/v1/dags"
        response = requests.request("GET", url, headers=HEADERS)
        if response.status_code == 200:
            dags = json.loads(response.content.decode("utf-8"))["dags"]
            dag_ids = [dag["dag_id"] for dag in dags]
            dag_list["dag_ids"] = dag_ids
        return dag_list
    except Exception:
        raise


def get_dag_tasks(dag_id):
    """
    Fetch all tasks for a dag id.

    Args:
        dag_id: DAG id of a particular dag

    Returns:
        List if task ids
    """
    task_list = defaultdict(list)
    try:
        config = parse_yaml("config.yml")
        host = config["airflow"]["host"]
        url = f"http://{host}/api/v1/dags/{dag_id}/tasks"
        response = requests.request("GET", url, headers=HEADERS)
        if response.status_code == 200:
            tasks = json.loads(response.content.decode("utf-8"))["tasks"]
            for task in tasks:
                task_list[task["class_ref"]["class_name"]].append(task["task_id"])
            return task_list
        return task_list
    except Exception:
        raise
