import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../../components/SearchBar/SearchBar';
import './HomePage.css';

const imageUrls = [
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00001pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00002pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00019pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00018pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00017pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00015pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00014pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00013pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00012pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00011pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00010pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00009pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00006pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00003pictureRintintin.jpg',
  'https://rintintin-bucket.s3.eu-west-3.amazonaws.com/00007pictureRintintin.jpg'
];

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [backgroundImage, setBackgroundImage] = useState<string>('');

  useEffect(() => {
    const getRandomImageUrl = () => {
      const randomIndex = Math.floor(Math.random() * imageUrls.length);
      return imageUrls[randomIndex];
    };

    setBackgroundImage(getRandomImageUrl());
  }, []);

  const getCoordinates = async (address: string) => {
    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`);
      const data = await response.json();
      if (data && data.length > 0) {
        const { lat, lon } = data[0];
        return { lat, lon };
      } else {
        throw new Error('No results found');
      }
    } catch (error) {
      console.error('Error fetching coordinates:', error);
      return null;
    }
  };

  const handleSearch = async (address: string) => {
    const coordinates = await getCoordinates(address);
    if (coordinates) {
      navigate('/pensions', { state: { address, coordinates } });
    } else {
      navigate('/pensions', { state: { address } });
    }
  };

  return (
    <div className="home-page">
      <div className="hero-container">
        <section className="hero" style={{ backgroundImage: `url(${backgroundImage})` }}></section>
        <div className="hero-overlay">
          <div className="hero-content">
            <div className="yellow-container">
              <h2>Trouve l'endroit parfait pour ton compagnon de vie</h2>
            </div>
            <div className="search-bar-wrapper">
              <SearchBar withMarginTop={true} onSearch={handleSearch} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
