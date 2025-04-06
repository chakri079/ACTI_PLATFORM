import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
  const location = useLocation();

  return (
    <nav className="navigation">
      <div className="logo">
        <Link to="/">
          <h1>CyberThreatIntel</h1>
        </Link>
      </div>
      <ul className="nav-links">
        <li className={location.pathname === "/" ? "active" : ""}>
          <Link to="/">Home</Link>
        </li>
        <li className={location.pathname === "/dashboard" ? "active" : ""}>
          <Link to="/dashboard">Dashboard</Link>
        </li>
        <li className={location.pathname === "/videos" ? "active" : ""}>
          <Link to="/videos">Videos</Link>
        </li>
        <li className={location.pathname === "/news" ? "active" : ""}>
          <Link to="/news">News</Link>
        </li>
        <li className={location.pathname === "/chat" ? "active" : ""}>
          <Link to="/chat">Chat</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navigation;