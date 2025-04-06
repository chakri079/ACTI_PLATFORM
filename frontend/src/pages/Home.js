import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <h1>AI-Driven Cyber Threat Intelligence</h1>
          <p>
            Proactively detect, analyze, and respond to cyber threats 
            with our real-time intelligence platform powered by AI.
          </p>
          <Link to="/dashboard" className="cta-button">
            View Threat Dashboard
          </Link>
        </div>
      </section>
      
      <section className="features">
        <h2>Key Features</h2>
        <div className="feature-grid">
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Real-Time Threat Detection</h3>
            <p>
              Continuously collect and analyze data from multiple sources 
              including social media and threat intelligence feeds.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI-Powered Analysis</h3>
            <p>
              Leverage machine learning models to identify attack patterns
              and predict emerging threats before they impact your systems.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Interactive Dashboards</h3>
            <p>
              Visualize threat data and risk severity with intuitive
              dashboards for quick decision-making.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🛡️</div>
            <h3>Automated Mitigation</h3>
            <p>
              Receive AI-generated mitigation recommendations to quickly
              respond to identified threats.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔗</div>
            <h3>MITRE ATT&CK Integration</h3>
            <p>
              Map threats to the MITRE ATT&CK framework for standardized
              threat intelligence and response.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">💬</div>
            <h3>AI Assistant</h3>
            <p>
              Ask questions and get expert cybersecurity guidance from our
              AI-powered chat assistant.
            </p>
          </div>
        </div>
      </section>
      
      <section className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3>Collection</h3>
              <p>
                Our platform continuously collects threat data from Twitter and 
                Open Threat Exchange (OTX).
              </p>
            </div>
          </div>
          
          <div className="step">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3>Analysis</h3>
              <p>
                Advanced NLP models analyze the collected data to identify 
                potential threats and attack patterns.
              </p>
            </div>
          </div>
          
          <div className="step">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3>Visualization</h3>
              <p>
                Threats are displayed on an intuitive dashboard with severity 
                scores and geographical impact.
              </p>
            </div>
          </div>
          
          <div className="step">
            <div className="step-number">4</div>
            <div className="step-content">
              <h3>Response</h3>
              <p>
                Generate mitigation strategies using AI and map threats to the 
                MITRE ATT&CK framework.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;