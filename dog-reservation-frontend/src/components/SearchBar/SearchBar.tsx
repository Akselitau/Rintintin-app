import React, { useState } from 'react';
import './SearchBar.css';

interface SearchBarProps {
  onSearch: (address: string) => void;
  withMarginTop?: boolean; // Ajout de la nouvelle prop
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, withMarginTop = false }) => {
  const [address, setAddress] = useState('');

  const handleSearch = () => {
    onSearch(address);
  };

  return (
    <div className={`search-bar-container ${withMarginTop ? 'margin-top' : ''}`}>
      <div className="search-bar">
        <div className="search-input-container">
          <label htmlFor="location" >Où ?</label>
          <input
            id="location"
            type="text"
            placeholder="L'endroit idéal"
            className="search-input"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
          />
        </div>
        <div className="separator"></div>
        <div className="search-input-container">
          <label htmlFor="start-date" style={{ marginRight: '8px' }}>Du</label>
          <input id="start-date" type="date" placeholder="Date d'arrivée" className="search-input" />
        </div>
        <div className="separator"></div>
        <div className="search-input-container">
          <label htmlFor="end-date" style={{ marginRight: '8px' }}>Au</label>
          <input id="end-date" type="date" placeholder="Date de départ" className="search-input" />
        </div>
        <button className="search-btn" style={{ marginLeft: '24px' }} onClick={handleSearch}>
          <svg width="24" height="24" viewBox="0 0 24 24">
            <path d="M10 18c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8zm8.293 1.707l4.707 4.707-1.414 1.414-4.707-4.707c-.391.391-.902.707-1.414.707s-1.023-.316-1.414-.707c-.391-.391-.707-.902-.707-1.414s.316-1.023.707-1.414c.391-.391.902-.707 1.414-.707s1.023.316 1.414.707c.391.391.707.902.707 1.414s-.316 1.023-.707 1.414c-.391.391-.902.707-1.414.707s-1.023-.316-1.414-.707z" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default SearchBar;
