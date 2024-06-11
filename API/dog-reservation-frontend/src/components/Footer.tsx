import React from 'react';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>&copy; 2024 RINTINTIN. Tous droits réservés.</p>
        <div className="footer-links">
          <a href="/contact">Nous contacter</a>
          <a href="/legal">Mentions légales</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
