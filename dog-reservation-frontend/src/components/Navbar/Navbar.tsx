import React from 'react';
import './Navbar.css';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          RINTINTIN
        </Link>
      </div>
      <div className="search-container">
        <input type="text" placeholder="Rechercher une pension" className="search-input" />
        <button className="search-button">
          <svg width="24" height="24" viewBox="0 0 24 24">
            <path d="M10 18c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8zm8.293 1.707l4.707 4.707-1.414 1.414-4.707-4.707c-.391.391-.902.707-1.414.707s-1.023-.316-1.414-.707c-.391-.391-.707-.902-.707-1.414s.316-1.023.707-1.414c.391-.391.902-.707 1.414-.707s1.023.316 1.414.707c.391.391.707.902.707 1.414s-.316 1.023-.707 1.414zm-8.293-2c3.314 0 6-2.686 6-6s-2.686-6-6-6-6 2.686-6 6 2.686 6 6 6z" />
          </svg>
        </button>
      </div>
      <div className="buttons">
        <Link to="/register-pension">
          <button className="btn outline">Je suis une pension</button>
        </Link>
        {isAuthenticated ? (
          <div className="user-menu">
            <img src={user?.profile_photo_url || 'default-profile.png'} alt="Profile" className="profile-pic" />
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
