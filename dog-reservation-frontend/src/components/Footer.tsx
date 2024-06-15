import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>&copy; 2024 RINTINTIN. Tous droits réservés.</p>
        <div className="footer-links">
          <Link to="/contact">Nous contacter</Link>
          <Link to="/legal">Mentions légales</Link>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
