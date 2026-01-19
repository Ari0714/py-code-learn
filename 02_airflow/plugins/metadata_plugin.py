from airflow.plugins_manager import AirflowPlugin
from airflow.models import TaskInstance
from airflow.utils.session import provide_session
from kafka_producer import AirflowKafkaProducer
from datetime import datetime

KAFKA_BOOTSTRAP = ["hdp:9092"]
TOPIC = "airflow_metadata"

producer = AirflowKafkaProducer(KAFKA_BOOTSTRAP)

@provide_session
def send_metadata(context, session=None, status="UNKNOWN"):
    ti: TaskInstance = context["ti"]

    message = {
        "dag_id": ti.dag_id,
        "task_id": ti.task_id,
        "run_id": ti.run_id,
        "execution_date": str(ti.execution_date),
        "try_number": ti.try_number,
        "state": status,
        "hostname": ti.hostname,
        "timestamp": datetime.utcnow().isoformat()
    }

    producer.send(TOPIC, message)


def pre_execute(context):
    send_metadata(context, status="STARTED")


def post_execute(context, result=None):
    send_metadata(context, status="SUCCESS")


class MetadataPlugin(AirflowPlugin):
    name = "metadata_plugin"
