import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/task-handler', methods=['POST'])
def task_handler():
    task_payload = request.get_json(silent=True)
    print(f'Task recieved: {task_payload}')
    return jsonify(task_payload)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)