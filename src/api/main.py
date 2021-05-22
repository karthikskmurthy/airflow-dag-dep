import os

from fastapi import FastAPI
from py2neo import Graph

from helpers import get_dags, get_dag_tasks
from constants import GRAPH_PORT, GRAPH_SCHEME, QUERY_DEPENDENCY, QUERY_NON_DEPENDENCY

app = FastAPI()

GRAPH_PASSWORD = os.environ.get("NEO_PASSWORD")
graph = Graph(password=GRAPH_PASSWORD, port=GRAPH_PORT, scheme=GRAPH_SCHEME)


@app.get("/")
def create_dag_relation():
    """Build relation between dags and pushes the nodes and relations to neo4j db."""
    try:
        dag_id_list = get_dags()
        identifier = "name"
        print(dag_id_list)
        for dag in dag_id_list["dag_ids"]:
            tasks = get_dag_tasks(dag)
            print(tasks)
            if "ExternalTaskSensor" in tasks.keys():
                dependent_tasks = tasks["ExternalTaskSensor"]
                for task in dependent_tasks:
                    query = QUERY_DEPENDENCY.format(identifier, dag, task)
                    graph.run(query)
            else:
                query = QUERY_NON_DEPENDENCY.format(identifier, dag)
                graph.run(query)
        return True
    except Exception:
        raise
