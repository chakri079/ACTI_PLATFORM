import React, { useState, useEffect } from 'react';
import Dashboard from '../components/Dashboard';
import ThreatList from '../components/ThreatList';
import './DashboardPage.css';

const DashboardPage = () => {
  const [threats, setThreats] = useState([]);
  const [stats, setStats] = useState({
    found: 0,
    mitigated: 0,
    countries: [],
    threat_level: 'Low'
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch threats data
  const fetchThreats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/threats');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setThreats(data.threats);
      setStats(data.stats);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching threats:', err);
      setError('Failed to fetch threat data. Please try again later.');
      setLoading(false);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchThreats();
    
    // Set up polling for real-time updates
    const interval = setInterval(() => {
      fetchThreats();
    }, 30000); // Poll every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  // Handle MITRE mapping
  const handleMapThreat = async (threatId) => {
    try {
      const response = await fetch('http://localhost:5000/api/mitre-map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ threatId }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Update the threat with the MITRE mapping
      setThreats(prevThreats => 
        prevThreats.map(threat => 
          threat.id === threatId 
            ? { ...threat, mitre: data.mitre } 
            : threat
        )
      );
    } catch (err) {
      console.error('Error mapping threat to MITRE:', err);
      alert('Failed to map threat to MITRE ATT&CK framework. Please try again.');
    }
  };

  // Handle threat mitigation
  const handleMitigateThreat = async (threatId) => {
    try {
      const response = await fetch('http://localhost:5000/api/mitigate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ threatId }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Update the threat with mitigation info
      setThreats(prevThreats => 
        prevThreats.map(threat => 
          threat.id === threatId 
            ? { ...threat, mitigation: data.mitigation, mitigated: true } 
            : threat
        )
      );
      
      // Update stats
      setStats(prevStats => ({
        ...prevStats,
        mitigated: prevStats.mitigated + 1
      }));
    } catch (err) {
      console.error('Error generating mitigation:', err);
      alert('Failed to generate mitigation steps. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="dashboard-page loading">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading threat intelligence data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-page error">
        <div className="error-message">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={fetchThreats}>Try Again</button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <Dashboard stats={stats} />
      <ThreatList 
        threats={threats} 
        onMapThreat={handleMapThreat} 
        onMitigateThreat={handleMitigateThreat} 
      />
    </div>
  );
};

export default DashboardPage;