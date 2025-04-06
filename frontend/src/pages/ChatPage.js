import React from 'react';
import Chatbot from '../components/Chatbot';
import './ChatPage.css';

const ChatPage = () => {
  return (
    <div className="chat-page">
      <div className="chat-intro">
        <h1>Cybersecurity AI Assistant</h1>
        <p>
          Get expert guidance and answers to your cybersecurity questions.
          Our AI assistant is trained on the latest threat intelligence and 
          cybersecurity best practices.
        </p>
      </div>
      <div className="chat-container">
        <Chatbot />
      </div>
    </div>
  );
};

export default ChatPage;