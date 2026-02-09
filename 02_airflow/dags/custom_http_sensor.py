import requests
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults


class CustomHttpSensor(BaseSensorOperator):
    """
    Custom HTTP Sensor (POST JSON, reschedule supported)
    """

    @apply_defaults
    def __init__(
        self,
        base_url: str,
        endpoint: str,
        payload: dict,
        headers: dict | None = None,
        timeout: int = 10,
        success_status_codes: list[int] | None = None,
        **kwargs,
    ):
        """
        :param base_url: e.g. https://api.example.com:8080
        :param endpoint: e.g. /check
        :param payload: POST json body
        """
        super().__init__(**kwargs)

        self.base_url = base_url.rstrip("/")
        self.endpoint = endpoint.lstrip("/")
        self.payload = payload
        self.headers = headers or {"Content-Type": "application/json"}
        self.timeout = timeout
        self.success_status_codes = success_status_codes or [200]

    @property
    def url(self) -> str:
        return f"{self.base_url}/{self.endpoint}"

    def poke(self, context):
        self.log.info("POST %s payload=%s", self.url, self.payload)

        try:
            resp = requests.post(
                url=self.url,
                json=self.payload,
                headers=self.headers,
                timeout=self.timeout,
            )

            self.log.info(
                "HTTP %s response=%s",
                resp.status_code,
                resp.text[:300],
            )

            return resp.status_code in self.success_status_codes

        except Exception as e:
            self.log.warning("HTTP request failed: %s", e)
            return False


####
from airflow import DAG
from datetime import datetime
from custom_http_sensor import CustomHttpSensor

with DAG(
    dag_id="custom_http_sensor_post_reschedule",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    wait_api_ready = CustomHttpSensor(
        task_id="wait_api_ready",
        base_url="https://api.example.com:8080",
        endpoint="/check",
        payload={"name": "ddf"},
        poke_interval=30,
        timeout=10 * 60,
        mode="reschedule",   # ⭐ 关键点
    )
