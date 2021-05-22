[![CircleCI](https://circleci.com/gh/karthikskmurthy/airflow-dag-dep.svg?style=svg)](https://circleci.com/gh/karthikskmurthy/airflow-dag-dep/?branch=main)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
# airflow-dag-dep
Airflow is a data orchestration tool which is used to stick different operators together.
As the number of DAGs in airflow increases there are high changes that these dags are dependent on each other . And one way to hook these DAGs together is to use ExternalTaskSensor in downstream DAGs , so that downstream DAG will trigger only when upstream DAG is marked success.

