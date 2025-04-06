import re
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Define cybersecurity keywords and patterns for our basic NLP model
ATTACK_KEYWORDS = {
    'malware': ['malware', 'virus', 'trojan', 'spyware', 'ransomware', 'adware', 'worm'],
    'phishing': ['phishing', 'spear phishing', 'whaling', 'social engineering'],
    'ddos': ['ddos', 'dos', 'denial of service', 'distributed denial of service', 'botnet'],
    'exploit': ['exploit', 'vulnerability', 'zero day', 'zero-day', 'cve', 'rce', 'buffer overflow'],
    'injection': ['sql injection', 'command injection', 'code injection', 'xss', 'cross site'],
    'mitm': ['man in the middle', 'mitm', 'eavesdropping', 'interception'],
    'bruteforce': ['brute force', 'bruteforce', 'password cracking', 'credential stuffing'],
    'backdoor': ['backdoor', 'trojan', 'rootkit', 'rat', 'remote access'],
    'cryptojacking': ['cryptojacking', 'crypto mining', 'coin mining'],
    'data_breach': ['data breach', 'leak', 'exfiltration', 'information disclosure']
}

def preprocess_text(text):
    """Preprocess text for analysis"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs, special characters, and digits
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    return filtered_tokens

def identify_attack_patterns(tokens):
    """Identify potential attack patterns from tokens"""
    identified_patterns = []
    text = ' '.join(tokens)
    
    for attack_type, keywords in ATTACK_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text or any(keyword == token for token in tokens):
                if attack_type not in identified_patterns:
                    identified_patterns.append(attack_type)
    
    return identified_patterns

def analyze_data(data_points):
    """Analyze collected data to identify threats"""
    analyzed_threats = []
    
    for data_point in data_points:
        # Extract text content
        text_content = data_point.get('text', '')
        
        # Skip if no textual content
        if not text_content:
            continue
        
        # Preprocess the text
        processed_tokens = preprocess_text(text_content)
        
        # Identify attack patterns
        attack_patterns = identify_attack_patterns(processed_tokens)
        
        # If attack patterns are identified, mark as a threat
        if attack_patterns:
            # Create a copy of the data point and add analysis details
            threat = data_point.copy()
            threat['attack_patterns'] = attack_patterns
            
            # Generate a description based on the identified patterns
            threat['description'] = generate_threat_description(threat, attack_patterns)
            
            analyzed_threats.append(threat)
    
    return analyzed_threats

def generate_threat_description(threat, attack_patterns):
    """Generate a description for the identified threat"""
    source = threat.get('source', 'unknown')
    text = threat.get('text', '')
    
    # Truncate text to a reasonable length
    if len(text) > 200:
        text = text[:200] + '...'
    
    # Combine attack patterns into a string
    patterns_str = ', '.join(attack_patterns)
    
    # Generate description
    if source == 'twitter':
        return f"Potential {patterns_str} threat detected in social media discussions. {text}"
    elif source == 'otx':
        title = threat.get('title', '')
        return f"{title}: Threat intelligence indicates {patterns_str} activity. {text}"
    else:
        return f"Potential {patterns_str} threat detected. {text}"

# For testing
if __name__ == "__main__":
    test_data = [
        {
            'id': '1',
            'source': 'twitter',
            'text': 'New malware campaign targeting Windows users through phishing emails with malicious attachments.'
        },
        {
            'id': '2',
            'source': 'otx',
            'text': 'SQL injection vulnerability discovered in popular CMS software. Patch immediately.'
        }
    ]
    
    results = analyze_data(test_data)
    for result in results:
        print(f"Threat: {result['description']}")
        print(f"Attack Patterns: {result['attack_patterns']}")
        print("---")