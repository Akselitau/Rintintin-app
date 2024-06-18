import React, { useState } from 'react';
import './AlphaBanner.css';

const AlphaBanner: React.FC = () => {
  const [isVisible, setIsVisible] = useState(true);
  const [isFadingOut, setIsFadingOut] = useState(false);

  const handleClose = () => {
    setIsFadingOut(true);
    setTimeout(() => setIsVisible(false), 500); // Correspond à la durée de l'animation de disparition
  };

  if (!isVisible) return null;

  return (
    <div className={`alpha-banner ${isFadingOut ? 'fade-out' : ''}`}>
      <span className="bold-text">Le site est dans sa première phase de développement.</span>
      <br />
      <span >Nous travaillons activement pour améliorer l'expérience utilisateur et ajouter de nouvelles fonctionnalités. Merci de votre compréhension et de votre soutien.</span>
      <button onClick={handleClose} className="close-button">X</button>
    </div>
  );
};

export default AlphaBanner;
