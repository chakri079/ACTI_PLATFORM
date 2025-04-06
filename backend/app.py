from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import json
from twitter_scraper import get_twitter_data
from otx_scraper import get_otx_data
from ml_model import analyze_data
from mitre_mapping import map_to_mitre
from gemini_api import get_mitigation_steps, get_chat_response
import config

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for our application
threats = []
threat_stats = {
    "found": 0,
    "mitigated": 0,
    "countries": set(),
    "levels": []
}

def calculate_threat_level():
    if not threat_stats["levels"]:
        return "Low"
    
    avg = sum(threat_stats["levels"]) / len(threat_stats["levels"])
    if avg < 3:
        return "Low"
    elif avg < 7:
        return "Medium"
    else:
        return "High"

def data_collection_job():
    """Background job to collect and analyze threat data"""
    while True:
        try:
            # Collect data from sources
            twitter_data = get_twitter_data()
            otx_data = get_otx_data()
            
            # Combine data for analysis
            combined_data = twitter_data + otx_data
            
            # Process with ML model
            if combined_data:
                new_threats = analyze_data(combined_data)
                
                # Update our in-memory storage
                for threat in new_threats:
                    if not any(t['id'] == threat['id'] for t in threats):
                        threats.append(threat)
                        threat_stats["found"] += 1
                        threat_stats["levels"].append(threat["severity"])
                        if "country" in threat and threat["country"]:
                            threat_stats["countries"].add(threat["country"])
            
            # Sleep for a while before next collection
            time.sleep(300)  # 5 minutes
        except Exception as e:
            print(f"Error in data collection job: {e}")
            time.sleep(60)  # Wait a bit before retrying

# API Routes
@app.route('/api/threats', methods=['GET'])
def get_threats():
    return jsonify({
        "threats": threats,
        "stats": {
            "found": threat_stats["found"],
            "mitigated": threat_stats["mitigated"],
            "countries": list(threat_stats["countries"]),
            "threat_level": calculate_threat_level()
        }
    })

@app.route('/api/mitre-map', methods=['POST'])
def mitre_mapping():
    threat_id = request.json.get('threatId')
    threat = next((t for t in threats if t['id'] == threat_id), None)
    
    if not threat:
        return jsonify({"error": "Threat not found"}), 404
    
    mitre_info = map_to_mitre(threat)
    
    # Update the threat with MITRE mapping
    for t in threats:
        if t['id'] == threat_id:
            t['mitre'] = mitre_info
    
    return jsonify({"mitre": mitre_info})

@app.route('/api/mitigate', methods=['POST'])
def mitigate_threat():
    threat_id = request.json.get('threatId')
    threat = next((t for t in threats if t['id'] == threat_id), None)
    
    if not threat:
        return jsonify({"error": "Threat not found"}), 404
    
    mitigation = get_mitigation_steps(threat)
    
    # Update the threat with mitigation info
    for t in threats:
        if t['id'] == threat_id:
            t['mitigation'] = mitigation
            t['mitigated'] = True
            threat_stats["mitigated"] += 1
    
    return jsonify({"mitigation": mitigation})

@app.route('/api/chat', methods=['POST'])
def chat():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    response = get_chat_response(query)
    return jsonify({"response": response})

if __name__ == '__main__':
    # Start data collection in a background thread
    data_thread = threading.Thread(target=data_collection_job)
    data_thread.daemon = True
    data_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)