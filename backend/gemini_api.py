import requests
import json
import config

# Gemini API base URL
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def get_gemini_response(prompt):
    """Get a response from Gemini API"""
    api_url = f"{GEMINI_API_BASE}?key={config.GEMINI_API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1024,
        }
    }
    
    try:
        response = requests.post(api_url, json=payload)
        
        if response.status_code != 200:
            print(f"Error from Gemini API: {response.status_code}")
            return "I couldn't generate a response at this time. Please try again later."
        
        result = response.json()
        
        # Extract the generated text from the response
        if 'candidates' in result and len(result['candidates']) > 0:
            if 'content' in result['candidates'][0] and 'parts' in result['candidates'][0]['content']:
                for part in result['candidates'][0]['content']['parts']:
                    if 'text' in part:
                        return part['text']
        
        return "I couldn't generate a meaningful response. Please try again."
    
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "An error occurred while communicating with the AI service. Please try again later."

def get_mitigation_steps(threat):
    """Get mitigation recommendations for a threat using Gemini API"""
    # Extract relevant information from the threat
    threat_description = threat.get('description', threat.get('text', ''))
    attack_patterns = threat.get('attack_patterns', [])
    attack_patterns_str = ', '.join(attack_patterns) if attack_patterns else 'unknown'
    
    # Construct the prompt for Gemini
    prompt = f"""
As a cybersecurity expert, provide specific mitigation steps for the following threat:

Threat Description: {threat_description}

Attack Patterns Identified: {attack_patterns_str}

Please provide:
1. A brief summary of the threat
2. 3-5 specific, actionable mitigation steps
3. Potential long-term preventive measures
    """
    
    # Get the response from Gemini
    mitigation_text = get_gemini_response(prompt)
    
    return mitigation_text

def get_chat_response(query):
    """Get a response for the cybersecurity chatbot using Gemini API"""
    # Construct the prompt for Gemini
    prompt = f"""
You are an AI cybersecurity assistant. Provide clear, accurate, and helpful information in response to the following query related to cybersecurity:

Query: {query}

If the question is not related to cybersecurity, politely inform the user that you're focused on helping with cybersecurity topics.
    """
    
    # Get the response from Gemini
    response_text = get_gemini_response(prompt)
    
    return response_text

# For testing
if __name__ == "__main__":
    test_query = "What is a zero-day vulnerability?"
    response = get_chat_response(test_query)
    print(f"Query: {test_query}")
    print(f"Response: {response}")
    
    test_threat = {
        'description': 'Potential phishing threat detected in social media discussions. New campaign using fake Microsoft emails to steal credentials.',
        'attack_patterns': ['phishing', 'credential_theft']
    }
    
    mitigation = get_mitigation_steps(test_threat)
    print("\nMitigation Steps:")
    print(mitigation)