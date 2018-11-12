import json
import logging
import os.path
import sys

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)

TEST_TOPIC = "test_avro_demo"


def get_default_schema():
    """
    Load default schema from a .avsc file.
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, '..', 'schemas', 'person3.avsc')


def get_settings():
    """
    Load default settings from a .json file.
    """
    dirname = os.path.dirname(__file__)
    settings = os.path.join(dirname, '..', 'settings', 'producer.json')
    with open(settings, 'r') as fp:
        return json.load(fp)


class KafkaProducer(object):
    """
    This object produces messages to a Kafka queue.
    """
    def __init__(self, schema):
        self._schema = schema

    def produce(self, data):
        print("Start Producer")

        avro_producer = AvroProducer(get_settings())
        avro_producer.poll(0)
        avro_producer.produce(
            topic=TEST_TOPIC,
            value=data,
            value_schema=self._schema
        )
        avro_producer.flush()
        print('Produced message: {}'.format(data))


if __name__ == '__main__':
    try:
        new_user = sys.argv[1]
    except IndexError:
        new_user = 'me'

    default_schema = avro.load(get_default_schema())

    producer = KafkaProducer(default_schema)
    producer.produce({
        'username': new_user,
        'companyId': 1,
        'bio': 'This is a cool person.',
        'fullTime': True,
        'address': 'Current address',
        'affiliations': [
            'new-team',
            'python-developers']
    })
