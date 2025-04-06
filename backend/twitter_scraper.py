import tweepy
import config
import time
import re
import uuid
from datetime import datetime

def get_twitter_client():
    """Initialize and return a Twitter API client"""
    client = tweepy.Client(
        bearer_token=config.TWITTER_BEARER_TOKEN,
        consumer_key=config.TWITTER_API_KEY,
        consumer_secret=config.TWITTER_API_SECRET,
        access_token=config.TWITTER_ACCESS_TOKEN,
        access_token_secret=config.TWITTER_ACCESS_SECRET
    )
    return client

def extract_potential_cve(text):
    """Extract potential CVE IDs from text"""
    cve_pattern = r'CVE-\d{4}-\d{4,7}'
    matches = re.findall(cve_pattern, text)
    return matches if matches else []

def extract_country_mentions(text):
    """Extract potential country mentions from text"""
    # This is a simplified approach - a more robust solution would use NLP
    common_countries = [
        "USA", "US", "United States", "UK", "Russia", "China", "Iran", 
        "North Korea", "South Korea", "Japan", "Germany", "France", 
        "Australia", "Canada", "Israel", "Ukraine", "India"
    ]
    
    mentioned_countries = []
    for country in common_countries:
        if re.search(r'\b' + re.escape(country) + r'\b', text, re.IGNORECASE):
            mentioned_countries.append(country)
    
    return mentioned_countries[0] if mentioned_countries else None

def estimate_severity(text):
    """Estimate the severity of a threat based on keywords in the text"""
    high_severity_terms = ["critical", "high", "severe", "urgent", "emergency", "widespread"]
    medium_severity_terms = ["important", "moderate", "attention", "significant"]
    
    text_lower = text.lower()
    
    # Check for CVEs which typically indicate higher severity
    has_cve = bool(extract_potential_cve(text))
    
    # Count severity indicators
    high_count = sum(term in text_lower for term in high_severity_terms)
    medium_count = sum(term in text_lower for term in medium_severity_terms)
    
    # Basic scoring algorithm
    base_score = 5  # Medium baseline
    
    if has_cve:
        base_score += 2
    
    base_score += high_count * 1.5
    base_score += medium_count * 0.5
    
    # Cap at 10
    return min(int(base_score), 10)

def get_twitter_data():
    """Fetch cybersecurity threat-related tweets"""
    client = get_twitter_client()
    collected_data = []
    
    try:
        for search_term in config.TWITTER_SEARCH_TERMS:
            # Search for recent tweets containing the search term
            response = client.search_recent_tweets(
                query=search_term,
                max_results=config.TWITTER_FETCH_COUNT,
                tweet_fields=['created_at', 'author_id', 'text']
            )
            
            if not response.data:
                continue
                
            for tweet in response.data:
                # Process the tweet
                tweet_text = tweet.text
                
                # Skip retweets, replies and tweets with URLs (potential spam)
                if tweet_text.startswith('RT @') or tweet_text.startswith('@') or 'https://' in tweet_text:
                    continue
                    
                # Extract potential CVE IDs
                cves = extract_potential_cve(tweet_text)
                
                # Extract potential country mentions
                country = extract_country_mentions(tweet_text)
                
                # Estimate severity
                severity = estimate_severity(tweet_text)
                
                # Create a structured data point
                data_point = {
                    'id': str(uuid.uuid4()),
                    'source': 'twitter',
                    'source_id': str(tweet.id),
                    'text': tweet_text,
                    'created_at': tweet.created_at.isoformat(),
                    'cves': cves,
                    'severity': severity,
                    'country': country,
                    'mitigated': False
                }
                
                collected_data.append(data_point)
        
        return collected_data
        
    except Exception as e:
        print(f"Error fetching Twitter data: {e}")
        return []

# For testing
if __name__ == "__main__":
    data = get_twitter_data()
    print(f"Collected {len(data)} potential threats from Twitter.")
    for d in data[:5]:  # Print first 5 as sample
        print(f"Threat: {d['text'][:100]}...")
        print(f"Severity: {d['severity']}")
        print(f"CVEs: {d['cves']}")
        print(f"Country: {d['country']}")
        print("---")