import os
import pytest

from mock import Mock, patch

from helpers import parse_yaml, get_dags, get_dag_tasks


def test_parse_yaml():
    path = os.path.join("tests", "api", "sample_config.yml")
    actual_output = parse_yaml(path)
    expected_output = {"test": {"test_host": "localhost:8080"}}
    assert actual_output == expected_output


@patch("helpers.parse_yaml")
@patch("helpers.requests")
@patch("helpers.json")
def test_get_dags(patched_json, patched_requests, patched_parse_yaml):
    patched_parse_yaml.return_value = {"airflow": {"host": "localhost"}}
    patched_requests.request = Mock()
    patched_requests.request().status_code = 200
    patched_json.loads.return_value = {"dags": [{"dag_id": "dag1"}, {"dag_id": "dag2"}]}
    actual_dag_list = get_dags()
    expected_dag_list = {"dag_ids": ["dag1", "dag2"]}
    assert actual_dag_list == expected_dag_list


@patch("helpers.parse_yaml")
@patch("helpers.requests")
@patch("helpers.json")
def test_get_dag_tasks(patched_json, patched_requests, patched_parse_yaml):
    patched_parse_yaml.return_value = {"airflow": {"host": "localhost"}}
    patched_requests.request = Mock()
    patched_requests.request().status_code = 200
    patched_json.loads.return_value = {
        "tasks": [
            {"task_id": "a", "class_ref": {"class_name": "task_type"}},
            {"task_id": "b", "class_ref": {"class_name": "task_type"}},
            {"task_id": "c", "class_ref": {"class_name": "task_type"}},
        ]
    }
    actual_task_list = get_dag_tasks("sample")
    expected_task_list = {"task_type": ["a", "b", "c"]}
    assert actual_task_list == expected_task_list


@patch("helpers.parse_yaml")
@patch("helpers.requests")
@patch("helpers.json")
def test_get_dag_tasks_exception(patched_json, patched_requests, patched_parse_yaml):
    patched_parse_yaml.side_effect = Exception()
    with pytest.raises(Exception):
        get_dag_tasks("sample")
    patched_requests.request.assert_not_called()
    patched_json.loads.assert_not_called()
