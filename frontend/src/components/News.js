import React, { useEffect, useState } from 'react';
import './News.css';

const News = () => {
    const [articles, setArticles] = useState([]);
    const API_KEY = '8ea401147dce4f3b9e55b2dc1a554eb1'; // Replace with your actual API key
    const query = 'cyber security';
    
    useEffect(() => {
        const fetchNews = async () => {
            try {
                const response = await fetch(
                    `https://newsapi.org/v2/everything?q=${encodeURIComponent(query)}&language=en&sortBy=publishedAt&apiKey=${API_KEY}`
                );
                const data = await response.json();
                setArticles(data.articles || []);
            } catch (error) {
                console.error('Error fetching news:', error);
            }
        };
        fetchNews();
    }, []);

    return (
        <div className="news-container">
            <h2>Latest Cybersecurity News</h2>
            <div className="news-grid">
                {articles.map((article, index) => (
                    <div className="news-item" key={index}>
                        <img 
                            src={article.urlToImage || 'https://via.placeholder.com/300'} 
                            alt="News Thumbnail"
                        />
                        <h3>{article.title}</h3>
                        <p>{article.description || 'No description available.'}</p>
                        <a href={article.url} target="_blank" rel="noopener noreferrer">Read More</a>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default News;
