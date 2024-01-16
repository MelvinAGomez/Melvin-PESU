from flask import Flask, jsonify, request, redirect, url_for
import time
import threading
import requests
import json
import sys
from kafka import KafkaConsumer
from kafka import KafkaProducer


# Set up Kafka producer configuration
kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
i = 1
NODE_ID = sys.argv[1]

## Setup The Consumer
consumer_1 = KafkaConsumer("test_config",bootstrap_servers="localhost:9092", value_deserializer=lambda x: json.loads(x.decode('utf-8')))
consumer_2 = KafkaConsumer("trigger",bootstrap_servers="localhost:9092", value_deserializer=lambda x: json.loads(x.decode('utf-8')))
app = Flask(__name__)

latencies = []  # List to store latencies for each request
metrics = {}  # To send all the metrics to the Orchestrator
test_details = {}  # To store the details of each test_id

o1_url = 'http://localhost:5004/display_metrics'

# Add a global variable to store the heartbeat status
heartbeat_status = {}

# Function to periodically send heartbeat messages
def send_heartbeat():
    while True:
        # Send a heartbeat message to the orchestrator
        kafka_producer.send("heartbeat", value={"NODE_ID": NODE_ID, "status": "alive"})
        time.sleep(5)  # Adjust the interval as needed



# Avalanche Test
def send_request_avalanche(url):
    start_time = time.time()
    requests.get(url)
    end_time = time.time()

    # Calculate latency for the current request
    latency = end_time - start_time
    latencies.append(latency)

# Tsunami Test
def send_request_tsunami(url, delay):
    start_time = time.time()
    requests.get(url)
    end_time = time.time()

    # Calculate latency for the current request
    latency = end_time - start_time
    latencies.append(latency)

    # Introduce delay before the next request
    time.sleep(delay)


@app.route('/', methods=['POST', 'GET'])
def home():
    for msg in consumer_1:
        if msg.value == 'END':
            break
        test_config = msg.value
        print("Received Test Configuration:")
        print(json.dumps(test_config, indent=2))
        test_id = test_config['test_id']
        test_details[test_id] = test_config
        

    return redirect('test')



@app.route('/test', methods=['GET', 'POST'])
def index():
    global i,NODE_ID
    for msg in consumer_2:
        if msg.value == 'END':
            break
        trigger_message = msg.value
        print("Running Test")
        url = 'http://localhost:5001/ping'
        test_id = trigger_message['test_id']
        print(test_id)

        # Getting the Test Config from Orchestrator
        test_config = test_details.get(test_id)
        if not test_config:
            return jsonify({"error": "Test configuration not found."}), 404

        print("Received Test Configuration:")
        print(json.dumps(test_config, indent=2))

        number_of_requests = int(test_config['message_count_per_driver'])
        test_type = test_config['test_type']
        print("number of requests:",number_of_requests)
        print("Test Type:",test_type)

        if test_type == "AVALANCHE":
            # Use threading to simulate avalanche testing
            print("Performing the avalanche test")
            threads = []
            for _ in range(number_of_requests):
                thread = threading.Thread(target=send_request_avalanche, args=(url,))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()

        if test_type == "TSUNAMI":
            delay_between_requests = float(test_config['test_message_delay'])
            # Use threading to simulate tsunami testing
            print("Performing the tsunami test")
            threads = []
            for _ in range(number_of_requests):
                thread = threading.Thread(target=send_request_tsunami, args=(url, delay_between_requests))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()

        # Calculate metrics
        mean_latency = sum(latencies) / len(latencies) if latencies else 0
        median_latency = sorted(latencies)[len(latencies) // 2] if latencies else 0
        min_latency = min(latencies) if latencies else 0
        max_latency = max(latencies) if latencies else 0

        # Showing the metrics
        print(f"Mean Latency: {mean_latency} seconds")
        print(f"Median Latency: {median_latency} seconds")
        print(f"Min Latency: {min_latency} seconds")
        print(f"Max Latency: {max_latency} seconds")

        
        metrics[NODE_ID] = {"Test_ID":test_id,"Mean_Latency": mean_latency, "Median_Latency": median_latency, "Min_Latency": min_latency,"Max_Latency": max_latency}

        
    return redirect(url_for('send_metrics'))


#Sending the metrics to the ochestrator
@app.route('/send_metrics_oc',methods=['GET','POST'])
def send_metrics():
    time.sleep(1)
    kafka_producer.send("metrics", value=metrics)
    return "metrics sent"


if __name__ == '__main__':

    # Start the heartbeat thread
    heartbeat_thread = threading.Thread(target=send_heartbeat)
    heartbeat_thread.start()
    app.run(debug=True, port=5017)
