import React from 'react';
import './Dashboard.css';

const Dashboard = ({ stats }) => {
  const { found, mitigated, countries, threat_level } = stats;
  
  const getThreatLevelColor = (level) => {
    switch(level.toLowerCase()) {
      case 'high':
        return '#ff4d4d';
      case 'medium':
        return '#ffa64d';
      case 'low':
        return '#66cc66';
      default:
        return '#66cc66';
    }
  };

  return (
    <div className="dashboard">
      <h2>Threat Intelligence Dashboard</h2>
      <div className="metrics-container">
        <div className="metric-card">
          <h3>Threats Found</h3>
          <p className="metric-value">{found}</p>
        </div>
        <div className="metric-card">
          <h3>Threats Mitigated</h3>
          <p className="metric-value">{mitigated}</p>
        </div>
        <div className="metric-card">
          <h3>Countries Affected</h3>
          <p className="metric-value">{countries.length}</p>
        </div>
        <div className="metric-card">
          <h3>Threat Level</h3>
          <p 
            className="metric-value threat-level" 
            style={{ color: getThreatLevelColor(threat_level) }}
          >
            {threat_level}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;