# plugins/metadata/kafka_client.py

import json
import logging
from kafka import KafkaProducer

_producer = None

def get_producer(bootstrap_servers):
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            request_timeout_ms=3000,
            api_version_auto_timeout_ms=3000,
            retries=0,
            linger_ms=5,
        )
    return _producer


def safe_send(bootstrap_servers, topic, message):
    try:
        producer = get_producer(bootstrap_servers)
        producer.send(topic, message)
    except Exception:
        # ⚠️ 绝不能影响 Airflow 主流程
        logging.exception("Kafka send failed, ignored")



