import json
import logging
import os.path

from confluent_kafka.avro import AvroConsumer
from confluent_kafka import KafkaError
from confluent_kafka.avro.serializer import SerializerError

logger = logging.getLogger(__name__)

TEST_TOPIC = "test_avro_demo"


def get_settings():
    """
    Load default settings from a .json file.
    """
    dirname = os.path.dirname(__file__)
    settings = os.path.join(dirname, '..', 'settings', 'consumer.json')
    with open(settings, 'r') as fp:
        return json.load(fp)


def consume_messages():
    print("Start Consumer")

    settings = get_settings()
    consumer = AvroConsumer(settings)
    consumer.subscribe([TEST_TOPIC])

    while True:
        try:
            message = consumer.poll(timeout=5.0)
        except SerializerError as err:
            logger.error("Message deserialization failed {}".format(err))
            continue
        except Exception as err:
            logger.error("Caught exception while polling consumer: {}".format(err))
            continue
        if message is None:
            continue
        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logger.error(message.error())
                continue
        try:
            logger.debug(message.value())
            print(message.value())
        except Exception as err:
            logger.error("Caught exception while processing message: {}".format(err))

if __name__ == '__main__':
    consume_messages()
