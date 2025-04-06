import requests
import config
import uuid
import time
from datetime import datetime, timedelta

# OTX API base URL
OTX_API_BASE = "https://otx.alienvault.com/api/v1"

def get_otx_data():
    """Fetch threat data from AlienVault OTX"""
    headers = {"X-OTX-API-KEY": config.OTX_API_KEY}
    collected_data = []
    
    try:
        # Get pulses (threat intelligence data) from the last 24 hours
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Get pulses by modified date
        pulses_url = f"{OTX_API_BASE}/pulses/subscribed?modified_since={yesterday}"
        response = requests.get(pulses_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error fetching OTX data: {response.status_code}")
            return []
        
        pulses_data = response.json().get('results', [])
        
        for pulse in pulses_data:
            # Extract the relevant information from the pulse
            pulse_name = pulse.get('name', '')
            pulse_description = pulse.get('description', '')
            pulse_author = pulse.get('author_name', '')
            pulse_tags = pulse.get('tags', [])
            pulse_malware_families = pulse.get('malware_families', [])
            pulse_industries = pulse.get('industries', [])
            pulse_tlp = pulse.get('tlp', '')
            pulse_created = pulse.get('created', '')
            
            # Extract potentially affected countries
            targeted_countries = pulse.get('targeted_countries', [])
            country = targeted_countries[0] if targeted_countries else None
            
            # Estimate severity based on TLP and tags
            severity = estimate_severity_from_pulse(pulse)
            
            # Create a structured data point
            data_point = {
                'id': str(uuid.uuid4()),
                'source': 'otx',
                'source_id': pulse.get('id', ''),
                'text': f"{pulse_name}: {pulse_description[:200]}...",
                'title': pulse_name,
                'description': pulse_description,
                'created_at': pulse_created,
                'author': pulse_author,
                'tags': pulse_tags,
                'malware_families': pulse_malware_families,
                'industries': pulse_industries,
                'tlp': pulse_tlp,
                'severity': severity,
                'country': country,
                'mitigated': False
            }
            
            collected_data.append(data_point)
        
        return collected_data
        
    except Exception as e:
        print(f"Error fetching OTX data: {e}")
        return []

def estimate_severity_from_pulse(pulse):
    """Estimate the severity of a threat based on pulse data"""
    tags = pulse.get('tags', [])
    tlp = pulse.get('tlp', '').lower()
    
    # Start with a medium baseline
    severity = 5
    
    # TLP color affects severity
    if tlp == 'red':
        severity += 3
    elif tlp == 'amber':
        severity += 2
    elif tlp == 'green':
        severity += 0
    elif tlp == 'white':
        severity -= 1
    
    # Check for severity-related tags
    high_severity_tags = ['critical', 'high', 'severe', 'ransomware', 'apt', 'zero-day', 'exploit']
    medium_severity_tags = ['vulnerability', 'malware', 'phishing', 'trojan']
    
    for tag in tags:
        tag_lower = tag.lower()
        if any(hs_tag in tag_lower for hs_tag in high_severity_tags):
            severity += 1
        elif any(ms_tag in tag_lower for ms_tag in medium_severity_tags):
            severity += 0.5
    
    # Cap at 10
    return min(int(severity), 10)

# For testing
if __name__ == "__main__":
    data = get_otx_data()
    print(f"Collected {len(data)} potential threats from OTX.")
    for d in data[:5]:  # Print first 5 as sample
        print(f"Threat: {d['title']}")
        print(f"Severity: {d['severity']}")
        print(f"Country: {d['country']}")
        print(f"TLP: {d['tlp']}")
        print("---")