import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './LoginPage.css';
import Divider from '@mui/material/Divider';
import { Button } from 'evergreen-ui';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const navigate = useNavigate();

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault(); // Empêche le rechargement de la page
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/login`, {
        email: email,
        password: password,
      });
      localStorage.setItem('token', response.data.user.token);
      toast.success('Connexion réussie !'); // Notification de succès
      navigate('/');
    } catch (error: any) {
      console.error('Error logging in:', error);
      toast.error('Erreur lors de la connexion : ' + (error.response?.data?.message || 'Erreur inconnue')); // Notification d'erreur
    }
  };

  return (
    <div className="login-container">
      <div className="login-image"></div>
      <div className="login-form-container">
        <h2>Vous avez déjà utilisé Rintintin ?</h2>
        <form onSubmit={handleLogin}>
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
          
          <Button type="submit" className="login-button">Se connecter</Button>
          
          <Divider>OU</Divider>
          
          <h3>Nouveau sur Rintintin ?</h3>
          <Button appearance="minimal" className="create-account" onClick={() => navigate('/signup')}>Créer mon compte</Button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
