from flask import Flask, jsonify, render_template

app = Flask(__name__)
count = 0

@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('target_server.html')

@app.route('/ping', methods=['POST', 'GET'])
def process_data():
    global count
    count = count + 1
    return jsonify({'count': count})


@app.route('/metrics_from_server', methods=['POST', 'GET'])
def metric():
    global count
    return jsonify({'count': count})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
