import React from 'react';
import { useNavigate } from 'react-router-dom';
import './PensionCard.css';

interface PensionCardProps {
  id: number;
  imageUrls: string[]; // Modifié pour être un tableau de chaînes de caractères
  name: string;
  rating: number;
  address: string; // Ajout de la propriété address
  distanceKm?: number;
  description: string;
}

const PensionCard: React.FC<PensionCardProps> = ({ id, imageUrls, name, rating, address, distanceKm, description }) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate(`/pensions/${id}`);
  };

  return (
    <div className="pension-card" onClick={handleCardClick}>
      <img src={imageUrls[0]} alt={name} className="pension-card-image" />
      <div className="pension-card-content">
        <div className="pension-card-header">
          <h2 className="pension-card-title">{name}</h2>
          <div className="pension-card-rating">{rating} ⭐</div>
        </div>
        <p className="pension-card-address">{address}</p> {/* Ajout de l'affichage de l'adresse */}
        <p className="pension-card-distance">{distanceKm ? `${distanceKm.toFixed(2)} km` : ''}</p>
        <p className="pension-card-description">{description}</p>
      </div>
    </div>
  );
};

export default PensionCard;
