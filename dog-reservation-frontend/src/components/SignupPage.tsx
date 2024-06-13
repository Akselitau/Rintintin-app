import React, { useState } from 'react';
import './SignupPage.css';
import { useNavigate } from 'react-router-dom';

const SignupPage: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [profilePhotoUrl, setProfilePhotoUrl] = useState('');
  const navigate = useNavigate();

  const handleSignup = async () => {
    const user = {
      name,
      email,
      password,
      profile_photo_url: profilePhotoUrl || null, // Optionnel
    };

    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/create-user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
      });

      if (response.ok) {
        console.log('User created successfully');
        navigate('/login'); // Redirect to login page after successful signup
      } else {
        console.error('Error creating user');
      }
    } catch (error) {
      console.error('Error:', error);
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
        <input
          type="text"
          placeholder="URL de la photo de profil (optionnel)"
          value={profilePhotoUrl}
          onChange={(e) => setProfilePhotoUrl(e.target.value)}
        />
        <button onClick={handleSignup}>Créer son compte</button>
      </div>
    </div>
  );
};

export default SignupPage;
