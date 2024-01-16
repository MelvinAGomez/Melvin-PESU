from flask import Flask
import json
import sys
from kafka import KafkaConsumer
from kafka import KafkaProducer


# Set up Kafka producer configuration
kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
NODE_ID = sys.argv[1]

app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def home():

    kafka_producer.send("metrics", value='END')
    return "Test Over Check Orchestrator"


if __name__ == '__main__':
    app.run(debug=True, port=5013)
