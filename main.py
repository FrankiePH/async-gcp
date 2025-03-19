import os
import requests
from flask import Flask, request, jsonify
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

@app.route('/task-handler', methods=['POST'])
def task_handler():
    '''
    data = request.get_json(silent=True)
    if not data:
        return "Missing important_field", 400
    job_id = data.get("job_id")
    url = data.get("url")
    if not job_id or not url:
        return jsonify({"error": "Missing job_id or url"}), 400

    try:
        response = requests.get(url)
        status_code = response.status_code
    except Exception as e:
        status_code = f"Error: {e}"
    '''

    # Save the result in Firestore. Each job_id gets a document,
    # with each URL's result stored as a field.
    doc_ref = db.collection('job_results').document('my-job')
    # 'merge=True' ensures we add/update without overwriting existing data
    doc_ref.set({'wwwwww': 333}, merge=True)

    return jsonify({"processed_url": 'wwwww', "status_code": 333}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
