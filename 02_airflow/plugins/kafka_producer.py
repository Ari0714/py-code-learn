from kafka import KafkaProducer
import json
import logging

class AirflowKafkaProducer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=3,
            linger_ms=10
        )

    def send(self, topic, message):
        try:
            self.producer.send(topic, message)
            self.producer.flush()
        except Exception as e:
            logging.exception("Kafka send failed")
