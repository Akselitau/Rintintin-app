import React from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from './SearchBar';
import './HomePage.css';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  // Fonction pour récupérer les coordonnées géographiques
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
      // Passez les coordonnées à la page de liste de pensions
      navigate('/pensions', { state: { address, coordinates } });
    } else {
      // Redirigez sans les coordonnées si elles ne peuvent pas être récupérées
      navigate('/pensions', { state: { address } });
    }
  };

  return (
    <div className="home-page">
      <div className="hero-container">
        <section className="hero"></section>
        <div className="hero-overlay">
          <div className="hero-content">
            <div className="yellow-container">
              <h2>Trouve l'endroit parfait pour ton compagnon de vie</h2>
            </div>
            <SearchBar withMarginTop={true} onSearch={handleSearch} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
