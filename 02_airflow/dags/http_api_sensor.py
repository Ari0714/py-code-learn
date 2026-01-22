from airflow.sensors.base import BaseSensorOperator
from airflow.providers.http.hooks.http import HttpHook
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from typing import Optional, Callable
import sys
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago


class HttpApiSensor(BaseSensorOperator):
    """
    使用 HttpHook 的 HTTP API Sensor
    """

    @apply_defaults
    def __init__(
        self,
        http_conn_id: str,
        endpoint: str,
        method: str = "GET",
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        response_check: Optional[Callable] = None,
        extra_options: Optional[dict] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.http_conn_id = http_conn_id
        self.endpoint = endpoint
        self.method = method.upper()
        self.data = data
        self.headers = headers
        self.response_check = response_check
        self.extra_options = extra_options or {}

    def poke(self, context):
        self.log.info(
            "Poking HTTP endpoint: conn_id=%s endpoint=%s",
            self.http_conn_id,
            self.endpoint,
        )

        hook = HttpHook(
            method=self.method,
            http_conn_id=self.http_conn_id,
        )

        try:
            response = hook.run(
                endpoint=self.endpoint,
                data=self.data,
                headers=self.headers,
                extra_options=self.extra_options,
            )
        except Exception as e:
            self.log.warning("HTTP request failed: %s", e)
            return False

        self.log.info("HTTP status code: %s", response.status_code)

        if response.status_code != 200:
            return False

        if self.response_check:
            try:
                return bool(self.response_check(response))
            except Exception as e:
                raise AirflowException(f"response_check failed: {e}")

        return True

def check_status(resp):
    return resp.json().get("status") == "SUCCESS"



############
with DAG(
    dag_id="http_hook_sensor_demo",
    start_date=days_ago(0),
    schedule_interval=None,
    catchup=False,
) as dag:

    wait_remote_job = HttpApiSensor(
        task_id="wait_remote_job",
        http_conn_id="remote_api",
        endpoint="/api/v1/job/status",
        method="GET",
        response_check=check_status,
        poke_interval=30,
        timeout=60 * 15,
        mode="reschedule",  # 强烈推荐
    )

    t3 = BashOperator(
        task_id='ads',
        bash_command='echo "hello Ari"',
        retries=1,
        dag=dag)

    wait_remote_job >> t3