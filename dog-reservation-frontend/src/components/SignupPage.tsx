import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SignupPage.css';

const SignupPage: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/create-user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, password }),
      });

      if (response.ok) {
        navigate('/login');
      } else {
        const errorData = await response.json();
        console.error('Error creating user:', errorData);
        alert(`Error creating user: ${errorData.message || 'Unknown error'}`);
      }
    } catch (error) {
      if (error instanceof Error) {
        console.error('Error creating user:', error);
        alert(`Error creating user: ${error.message || 'Unknown error'}`);
      } else {
        console.error('Unknown error:', error);
        alert('An unknown error occurred.');
      }
    }
  };

  return (
    <div className="signup-container">
      <h2>Créer un compte</h2>
      <div className="signup-form">
        <input
          type="text"
          placeholder="Nom"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
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
        <button onClick={handleSignup}>Créer son compte</button>
      </div>
    </div>
  );
};

export default SignupPage;
