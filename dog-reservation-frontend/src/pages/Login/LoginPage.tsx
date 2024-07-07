import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';
import Divider from '@mui/material/Divider';
import { Button } from 'evergreen-ui';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:8000/login', {
        email: email,
        password: password,
      });
      localStorage.setItem('token', response.data.user.token);
      alert('Logged in successfully!');
      navigate('/');
    } catch (error: any) {
      console.error('Error logging in:', error);
      alert('Error logging in: ' + (error.response?.data?.message || 'Unknown error'));
    }
  };

  return (
    <div className="login-container">
      <div className="login-image"></div>
      <div className="login-form-container">
        <h2>Vous avez déjà utilisé Rintintin ?</h2>
        <form>
          <label htmlFor="email">Email *</label>
          <input 
            type="email" 
            id="email" 
            placeholder="Email" 
            value={email}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          />
          
          <label htmlFor="password">Mot de passe *</label>
          <input 
            type="password" 
            id="password" 
            placeholder="Mot de passe" 
            value={password}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
          />
          
          <a href="#">Mot de passe oublié ?</a>
          
          <Button onClick={handleLogin} className="login-button">Se connecter</Button>
          
          <Divider>OU</Divider>
          
          <h3>Nouveau sur Rintintin ?</h3>
          <Button appearance="minimal" className="create-account" onClick={() => navigate('/signup')}>Créer mon compte</Button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
