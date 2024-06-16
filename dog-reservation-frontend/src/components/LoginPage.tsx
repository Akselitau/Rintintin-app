import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './LoginPage.css';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        login(data.token);
        navigate('/');
      } else {
        const errorData = await response.json();
        console.error('Error logging in:', errorData);
        alert(`Error logging in: ${errorData.message || 'Unknown error'}`);
      }
    } catch (error) {
      if (error instanceof Error) {
        console.error('Error logging in:', error);
        alert(`Error logging in: ${error.message || 'Unknown error'}`);
      } else {
        console.error('Unknown error:', error);
        alert('An unknown error occurred.');
      }
    }
  };

  return (
    <div className="login-container">
      <h2>Connexion</h2>
      <div className="login-form">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Mot de passe"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Connexion</button>
      </div>
      <hr />
      <div className="signup-link">
        <Link to="/signup">Je créer un compte</Link>
      </div>
    </div>
  );
};

export default LoginPage;
