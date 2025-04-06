import json
import os
import requests
import random

# MITRE ATT&CK Enterprise Matrix
# This is a simplified version for the demo
# In production, you would use the official MITRE ATT&CK APIs or data files
MITRE_TACTICS = {
    "TA0001": "Initial Access",
    "TA0002": "Execution",
    "TA0003": "Persistence",
    "TA0004": "Privilege Escalation",
    "TA0005": "Defense Evasion",
    "TA0006": "Credential Access",
    "TA0007": "Discovery",
    "TA0008": "Lateral Movement",
    "TA0009": "Collection",
    "TA0010": "Exfiltration",
    "TA0011": "Command and Control",
    "TA0040": "Impact"
}

# Sample mapping of attack patterns to MITRE techniques
# In a real implementation, this would be much more comprehensive
ATTACK_PATTERN_MAPPING = {
    'malware': {
        'tactics': ['TA0002', 'TA0003', 'TA0005'],
        'techniques': [
            {'id': 'T1204', 'name': 'User Execution', 'tactic': 'TA0002'},
            {'id': 'T1027', 'name': 'Obfuscated Files or Information', 'tactic': 'TA0005'},
            {'id': 'T1059', 'name': 'Command and Scripting Interpreter', 'tactic': 'TA0002'}
        ]
    },
    'phishing': {
        'tactics': ['TA0001', 'TA0002'],
        'techniques': [
            {'id': 'T1566', 'name': 'Phishing', 'tactic': 'TA0001'},
            {'id': 'T1204', 'name': 'User Execution', 'tactic': 'TA0002'},
            {'id': 'T1566.001', 'name': 'Spearphishing Attachment', 'tactic': 'TA0001'}
        ]
    },
    'ddos': {
        'tactics': ['TA0040'],
        'techniques': [
            {'id': 'T1498', 'name': 'Network Denial of Service', 'tactic': 'TA0040'},
            {'id': 'T1498.001', 'name': 'Direct Network Flood', 'tactic': 'TA0040'},
            {'id': 'T1498.002', 'name': 'Reflection Amplification', 'tactic': 'TA0040'}
        ]
    },
    'exploit': {
        'tactics': ['TA0001', 'TA0004', 'TA0005'],
        'techniques': [
            {'id': 'T1190', 'name': 'Exploit Public-Facing Application', 'tactic': 'TA0001'},
            {'id': 'T1203', 'name': 'Exploitation for Client Execution', 'tactic': 'TA0002'},
            {'id': 'T1068', 'name': 'Exploitation for Privilege Escalation', 'tactic': 'TA0004'}
        ]
    },
    'injection': {
        'tactics': ['TA0001', 'TA0002', 'TA0004'],
        'techniques': [
            {'id': 'T1190', 'name': 'Exploit Public-Facing Application', 'tactic': 'TA0001'},
            {'id': 'T1059', 'name': 'Command and Scripting Interpreter', 'tactic': 'TA0002'},
            {'id': 'T1027', 'name': 'Obfuscated Files or Information', 'tactic': 'TA0005'}
        ]
    },
    'mitm': {
        'tactics': ['TA0010', 'TA0011'],
        'techniques': [
            {'id': 'T1557', 'name': 'Man-in-the-Middle', 'tactic': 'TA0010'},
            {'id': 'T1040', 'name': 'Network Sniffing', 'tactic': 'TA0007'},
            {'id': 'T1557.001', 'name': 'LLMNR/NBT-NS Poisoning and SMB Relay', 'tactic': 'TA0010'}
        ]
    },
    'bruteforce': {
        'tactics': ['TA0006'],
        'techniques': [
            {'id': 'T1110', 'name': 'Brute Force', 'tactic': 'TA0006'},
            {'id': 'T1110.001', 'name': 'Password Guessing', 'tactic': 'TA0006'},
            {'id': 'T1110.002', 'name': 'Password Cracking', 'tactic': 'TA0006'}
        ]
    },
    'backdoor': {
        'tactics': ['TA0003', 'TA0004', 'TA0011'],
        'techniques': [
            {'id': 'T1133', 'name': 'External Remote Services', 'tactic': 'TA0003'},
            {'id': 'T1505', 'name': 'Server Software Component', 'tactic': 'TA0003'},
            {'id': 'T1219', 'name': 'Remote Access Software', 'tactic': 'TA0011'}
        ]
    },
    'cryptojacking': {
        'tactics': ['TA0040'],
        'techniques': [
            {'id': 'T1496', 'name': 'Resource Hijacking', 'tactic': 'TA0040'},
            {'id': 'T1059', 'name': 'Command and Scripting Interpreter', 'tactic': 'TA0002'},
            {'id': 'T1053', 'name': 'Scheduled Task/Job', 'tactic': 'TA0003'}
        ]
    },
    'data_breach': {
        'tactics': ['TA0009', 'TA0010'],
        'techniques': [
            {'id': 'T1005', 'name': 'Data from Local System', 'tactic': 'TA0009'},
            {'id': 'T1039', 'name': 'Data from Network Shared Drive', 'tactic': 'TA0009'},
            {'id': 'T1048', 'name': 'Exfiltration Over Alternative Protocol', 'tactic': 'TA0010'}
        ]
    }
}

def map_to_mitre(threat):
    """Map a threat to MITRE ATT&CK tactics and techniques"""
    attack_patterns = threat.get('attack_patterns', [])
    
    if not attack_patterns:
        return {
            "tactics": [],
            "techniques": [],
            "description": "Unable to map to MITRE ATT&CK. No attack patterns identified."
        }
    
    # Collect all tactics and techniques from all identified attack patterns
    all_tactics = []
    all_techniques = []
    
    for pattern in attack_patterns:
        if pattern in ATTACK_PATTERN_MAPPING:
            mapping_info = ATTACK_PATTERN_MAPPING[pattern]
            
            # Add tactics
            for tactic_id in mapping_info['tactics']:
                if tactic_id not in [t.get('id') for t in all_tactics]:
                    all_tactics.append({
                        'id': tactic_id,
                        'name': MITRE_TACTICS.get(tactic_id, 'Unknown')
                    })
            
            # Add techniques
            for technique in mapping_info['techniques']:
                if technique['id'] not in [t.get('id') for t in all_techniques]:
                    all_techniques.append(technique)
    
    # Generate a description
    description = generate_mitre_description(attack_patterns, all_tactics, all_techniques)
    
    return {
        "tactics": all_tactics,
        "techniques": all_techniques,
        "description": description
    }

def generate_mitre_description(attack_patterns, tactics, techniques):
    """Generate a human-readable description of the MITRE mapping"""
    if not tactics or not techniques:
        return "No MITRE ATT&CK mapping available for this threat."
    
    # Format attack patterns
    patterns_str = ", ".join(attack_patterns)
    
    # Format tactics
    tactics_str = ", ".join([f"{t['name']} ({t['id']})" for t in tactics])
    
    # Format primary techniques (limit to top 3 for readability)
    primary_techniques = techniques[:3]
    techniques_str = ", ".join([f"{t['name']} ({t['id']})" for t in primary_techniques])
    
    return f"This threat involves {patterns_str} and maps to the following MITRE ATT&CK tactics: {tactics_str}. Primary techniques include: {techniques_str}."

# For testing
if __name__ == "__main__":
    test_threat = {
        'id': '1',
        'source': 'twitter',
        'text': 'New malware campaign targeting Windows users through phishing emails with malicious attachments.',
        'attack_patterns': ['malware', 'phishing']
    }
    
    mapping = map_to_mitre(test_threat)
    print(f"MITRE Mapping Description: {mapping['description']}")
    print(f"Tactics: {[t['name'] for t in mapping['tactics']]}")
    print(f"Techniques: {[t['name'] for t in mapping['techniques']]}")