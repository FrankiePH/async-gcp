import os
import requests
from flask import Flask, request, jsonify
from google.cloud import firestore
import shortuuid, time, json
from types import SimpleNamespace



app = Flask(__name__)
db = firestore.Client()

def request_get(url, headers={}, allow_redirects=True):
    total_time_waited = 0
    response_code = 0
    while response_code != 200:
        if total_time_waited > 120:
            return SimpleNamespace(status_code='No Response (The request timed out after 120 seconds)')
        try:
            response = requests.get(url, headers=headers, allow_redirects=allow_redirects)
            response_code = response.status_code
            if response_code in [503, 504]:
                print(f"{time.strftime('%H:%M:%S')} - Got {response_code}. Sleeping for 60 seconds...")
                time.sleep(60)
                total_time_waited += 60
            else:
                return response
        except Exception as e:
            error_message = str(e)
            if "Max retries exceeded" in error_message or "Cannot allocate memory" in error_message:
                print(f"{time.strftime('%H:%M:%S')} - Encountered error: {error_message}. Waiting for 60 seconds before retrying...")
                time.sleep(60)
                total_time_waited += 60
                continue  # try again
            else:
                raise e


@app.route('/task-handler', methods=['POST'])
def task_handler():
    
    data = request.get_json(silent=True)
    print(f"DATA:: {data}")
    if not data:
        return "Missing important_field", 400
    elif data.get('url') == 'end':
        doc_id = shortuuid.uuid() 
        doc_ref = db.collection('link_checker_results').document(doc_id)
        doc_ref.set({"status_code": 'end', "standard_name": 'end', "processed_url": 'end'}, merge=True)
        return jsonify('End')
    try:
        standard_name = data.get("standard_name")
        url = data.get("url")
    except KeyError:
        return "Missing important_field", 40
    if not standard_name or not url:
        return jsonify({"error": "Missing job_id or url"}), 400

    try:
        response = request_get(url)
        status_code = response.status_code
    except Exception as e:
        status_code = f"Error: {e}"

    # Save the result in Firestore. Each job_id gets a document
    
    # hash the url to use it as a key
    doc_id = shortuuid.uuid() 
    doc_ref = db.collection('link_checker_results').document(doc_id)
    doc_ref.set({"status_code": status_code, 
                 "standard_name": standard_name, 
                 "processed_url": str(url)}, merge=True)

    return jsonify({"processed_url": str(url), "status_code":status_code}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
