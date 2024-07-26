import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>&copy; 2024 RINTINTIN. Tous droits réservés.</p>
        <div className="footer-links-container">
          <div className="footer-links">
            <Link to="/pensions">Nos pensions</Link>
            <Link to="/about">À propos de nous</Link>
            <Link to="/login">Se connecter</Link>
            <Link to="/signup">Créer un compte</Link>
            <Link to="/register-pension">Inscrire ma pension</Link>
            <Link to="/contact">Nous contacter</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
