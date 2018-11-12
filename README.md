avro-kafka-demo
===============

This set of demo scripts and schemas uses the
`confluent-kafka-python` library to test publishing
and consuming messages with Kafka.

Python Setup
------------

Python 3 required.

```
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Kafka Setup
-----------

These demo setup instructions are for macOS.

Install the Confluent Kafka packages (requires java8):
```
brew install confluent-oss
```

After installing Confluent, run all the services via commandline.

You must start Zookeeper in a shell before starting Kafka:
```
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties
```
By default, Zookeeper should run on port 2181.

Run Kafka in a separate shell:
```
kafka-server-start /usr/local/etc/kafka/server.properties
```
By default, Kafka should run on port 9092.

Then run the schema registry:
```
schema-registry-start /usr/local/etc/schema-registry/schema-registry.properties
```
By default, the schema registry should run on port 8081.
The registry may need to be configured to change the compatibility
in order to verify schema evolution (using different schemas
for the same topic). Modify and run the `change_compatibility.sh`
script in order to control registry compatibility.

Alternatively, see the docker setup:
https://docs.confluent.io/current/installation/docker/docs/installation/single-node-client.html

Demo
----

In one shell run the consumer:
```
python src/consumer.py
```

In another shell run the producer:
```
python src/producer.py <username>
```

Modify the data sent to Kafka in the producer code and test different 
schemas to verify schema evolution.
