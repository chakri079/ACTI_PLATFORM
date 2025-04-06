import React, { useEffect, useState } from 'react';
import './Videos.css';

const Videos = () => {
    const [videos, setVideos] = useState([]);
    const [language, setLanguage] = useState('English');
    const API_KEY = 'AIzaSyDYxdbFXGS6qLCz7n5SXiUoSSNdIOn9nFM'; // Replace with your actual API key
   
    // Language-based search queries
    const queries = {
        English: 'cyber security latest attacks',
        Telugu: 'సైబర్ భద్రత తాజా దాడులు',
        Hindi: 'साइबर सुरक्षा नवीनतम हमले'
    };

    useEffect(() => {
        const fetchVideos = async () => {
            try {
                const response = await fetch(
                    `https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=15&q=${encodeURIComponent(queries[language])}&type=video&key=${API_KEY}`
                );
                const data = await response.json();
                setVideos(data.items || []);
            } catch (error) {
                console.error('Error fetching videos:', error);
            }
        };
        fetchVideos();
    }, [queries]); // Fetch videos when language changes  replace with languages

    return (
        <div className="videos-container">
            <h2>Latest Cyber Security Videos</h2>
            <div className="language-buttons">
                <button onClick={() => setLanguage('English')}>English</button>
                <button onClick={() => setLanguage('Telugu')}>Telugu</button>
                <button onClick={() => setLanguage('Hindi')}>Hindi</button>
            </div>
            <div className="videos-grid">
                {videos.map(video => (
                    <div className="video" key={video.id.videoId}>
                        <iframe 
                            src={`https://www.youtube.com/embed/${video.id.videoId}`} 
                            frameBorder="0" 
                            allowFullScreen
                            title={video.snippet.title}
                        ></iframe>
                        <p>{video.snippet.title}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Videos;
