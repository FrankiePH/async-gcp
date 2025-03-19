import os
import requests
from flask import Flask, request, jsonify
from google.cloud import firestore
import shortuuid


app = Flask(__name__)
db = firestore.Client()



@app.route('/task-handler', methods=['POST'])
def task_handler():
    
    data = request.get_json(silent=True)
    if not data:
        return "Missing important_field", 400
    try:
        job_id = data.get("job_id")
        url = data.get("url")
    except KeyError:
        return "Missing important_field", 40
    if not job_id or not url:
        return jsonify({"error": "Missing job_id or url"}), 400

    try:
        response = requests.get(url)
        status_code = response.status_code
    except Exception as e:
        status_code = f"Error: {e}"

    # Save the result in Firestore. Each job_id gets a document
    
    # hash the url to use it as a key
    doc_id = shortuuid.uuid() 
    doc_ref = db.collection('url_checker_results').document(doc_id)
    doc_ref.set({"status_code": status_code, "processed_url": str(url)}, merge=True)

    return jsonify({"processed_url": str(url), "status_code":status_code}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
