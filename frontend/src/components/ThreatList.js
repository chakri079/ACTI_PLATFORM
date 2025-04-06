import React, { useState } from 'react';
import './ThreatList.css';

const ThreatList = ({ threats, onMapThreat, onMitigateThreat }) => {
  const [expandedThreat, setExpandedThreat] = useState(null);
  
  const toggleExpand = (id) => {
    if (expandedThreat === id) {
      setExpandedThreat(null);
    } else {
      setExpandedThreat(id);
    }
  };
  
  const getSourceIcon = (source) => {
    switch(source) {
      case 'twitter':
        return '🐦';
      case 'otx':
        return '🔍';
      default:
        return '📊';
    }
  };
  
  const getSeverityClass = (severity) => {
    if (severity >= 7) return 'high-severity';
    if (severity >= 3) return 'medium-severity';
    return 'low-severity';
  };

  return (
    <div className="threat-list">
      <h2>Active Threats</h2>
      {threats.length === 0 ? (
        <p className="no-threats">No threats detected yet. The system is monitoring potential sources.</p>
      ) : (
        <div className="threats-container">
          {threats.map(threat => (
            <div 
              key={threat.id} 
              className={`threat-card ${expandedThreat === threat.id ? 'expanded' : ''}`}
            >
              <div className="threat-header" onClick={() => toggleExpand(threat.id)}>
                <div className="threat-title">
                  <span className="source-icon">{getSourceIcon(threat.source)}</span>
                  <h3>{threat.title || (threat.text ? threat.text.substring(0, 50) + '...' : 'Unknown Threat')}</h3>
                </div>
                <div className={`severity-badge ${getSeverityClass(threat.severity)}`}>
                  Severity: {threat.severity}/10
                </div>
              </div>
              
              <div className="threat-content">
                <p className="threat-description">
                  {threat.description || threat.text || 'No description available.'}
                </p>
                
                <div className="threat-metadata">
                  <p><strong>Source:</strong> {threat.source === 'twitter' ? 'Twitter' : 'OTX'}</p>
                  {threat.country && <p><strong>Country:</strong> {threat.country}</p>}
                  {threat.attack_patterns && (
                    <p><strong>Attack Patterns:</strong> {threat.attack_patterns.join(', ')}</p>
                  )}
                </div>
                
                {threat.mitre && (
                  <div className="mitre-mapping">
                    <h4>MITRE ATT&CK Mapping</h4>
                    <p>{threat.mitre.description}</p>
                  </div>
                )}
                
                {threat.mitigation && (
                  <div className="mitigation-steps">
                    <h4>Mitigation Steps</h4>
                    <p>{threat.mitigation}</p>
                  </div>
                )}
                
                <div className="threat-actions">
                  {!threat.mitre && (
                    <button 
                      className="map-button"
                      onClick={() => onMapThreat(threat.id)}
                    >
                      Map to MITRE
                    </button>
                  )}
                  
                  {!threat.mitigation && (
                    <button 
                      className="mitigate-button"
                      onClick={() => onMitigateThreat(threat.id)}
                    >
                      Generate Mitigation
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ThreatList;