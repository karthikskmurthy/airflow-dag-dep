GRAPH_PORT = 7687
GRAPH_SCHEME = "bolt"
HEADERS = {
    "content-type": "application/json",
    "cache-control": "no-cache",
    "accept": "application/json",
}
QUERY_DEPENDENCY = """
MERGE(c:company{{{0}:'abc'}})
MERGE(d1:DAG{{{0}:'{1}'}})
with c, d1
MERGE (c)-[: dag]->(d1)
MERGE(d2:DAG{{{0}:'{2}'}})
with c, d1, d2
MERGE (c)-[: dag]->(d2)
MERGE (d1)-[: depends_on]->(d2)
"""
QUERY_NON_DEPENDENCY = """
MERGE(c:company{{{0}:'abc'}})
MERGE(d1:DAG{{{0}:'{1}'}})
with c, d1
MERGE (c)-[: dag]->(d1)
"""
