// src/components/Navbar/Navbar.tsx
import React, { useEffect, useState } from 'react';
import './Navbar.css';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [isFloating, setIsFloating] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 0) {
        setIsFloating(true);
      } else {
        setIsFloating(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <nav className={`navbar ${isFloating ? 'floating' : 'normal'}`}>
      <div className="logo">
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          RINTINTIN
        </Link>
      </div>
      <div className="nav-links">
        <Link to="/pensions" className="nav-link">Nos pensions</Link>
        <Link to="/about" className="nav-link">À propos</Link>
        <span className="nav-link disabled">Blog</span>
      </div>
      <div className="buttons">
        <Link to="/register-pension">
          <button className="btn outline">Je suis une pension</button>
        </Link>
        {isAuthenticated ? (
          <div className="user-menu">
            <img src={user?.profile_photo_url || 'https://img.freepik.com/vecteurs-premium/photo-profil-avatar-homme-illustration-vectorielle_268834-538.jpg'} alt="Profile" className="profile-pic" />
            <div className="dropdown">
              <button className="dropbtn">☰</button>
              <div className="dropdown-content">
                <Link to="/profile">Mon profil</Link>
                <Link to="/my-pension">Ma pension</Link>
                <Link to="/my-dog">Mon chien</Link>
                <Link to="/reservations">Mes reservations</Link>
                <button onClick={logout}>Se déconnecter</button>
              </div>
            </div>
          </div>
        ) : (
          <Link to="/login">
            <button className="btn filled">Connexion</button>
          </Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
