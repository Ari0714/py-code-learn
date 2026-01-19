# plugins/metadata/metadata_plugin.py

from airflow.plugins_manager import AirflowPlugin
from airflow.models import TaskInstance
from airflow.utils.session import provide_session
from airflow.models import Variable
from datetime import datetime

import sys
sys.path.append('/root/airflow2.2.5/02_airflow')

from kafka_client import safe_send

# Kafka 配置（来自 Airflow Variables）
KAFKA_BOOTSTRAP = Variable.get(
    "KAFKA_BOOTSTRAP",
    default_var="hdp:9092"
).split(",")

KAFKA_TOPIC = Variable.get(
    "KAFKA_METADATA_TOPIC",
    default_var="airflow_metadata"
)


def _build_payload(context, status):
    ti: TaskInstance = context["ti"]

    return {
        "dag_id": ti.dag_id,
        "task_id": ti.task_id,
        "run_id": ti.run_id,
        "try_number": ti.try_number,
        "state": status,
        "execution_date": str(ti.execution_date),
        "hostname": ti.hostname,
        "operator": ti.operator,
        "queue": ti.queue,
        "timestamp": datetime.utcnow().isoformat(),
    }


@provide_session
def _emit(context, status, session=None):
    payload = _build_payload(context, status)
    safe_send(KAFKA_BOOTSTRAP, KAFKA_TOPIC, payload)


# ======================
# Airflow Hook Functions
# ======================

def pre_execute(context):
    _emit(context, status="STARTED")


def post_execute(context, result=None):
    _emit(context, status="SUCCESS")


def on_failure(context):
    _emit(context, status="FAILED")


# ======================
# Plugin Definition
# ======================

class MetadataPlugin(AirflowPlugin):
    name = "metadata_plugin"




