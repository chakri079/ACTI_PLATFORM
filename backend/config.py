# API Keys and Configurations
# Replace placeholder values with your actual API keys
from dotenv import load_dotenv
load_dotenv()
# import os
# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

OTX_API_KEY = os.getenv("OTX_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Twitter search terms for cybersecurity threats
TWITTER_SEARCH_TERMS = [
    "cybersecurity threat", 
    "vulnerability", 
    "CVE", 
    "cyber attack", 
    "malware", 
    "ransomware", 
    "zero day", 
    "data breach",
    "phishing",
    "APT"
]

# Number of tweets to fetch per request
TWITTER_FETCH_COUNT = 50

# Threat severity thresholds (1-10 scale)
SEVERITY_THRESHOLD_LOW = 3
SEVERITY_THRESHOLD_MEDIUM = 7