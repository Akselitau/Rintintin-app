import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useStytch } from '@stytch/react';

const AuthHandler: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const stytchClient = useStytch();

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const token = queryParams.get('token');

    if (token) {
      stytchClient.magicLinks.authenticate(token, {
        session_duration_minutes: 60,
      })
        .then(response => {
          console.log('Authentication successful:', response);
          // Rediriger l'utilisateur vers la page d'accueil ou une autre page protégée
          navigate('/');
        })
        .catch(error => {
          console.error('Error authenticating:', error);
          alert('Authentication failed.');
        });
    }
  }, [location.search, navigate, stytchClient]);

  return <div>Authenticating...</div>;
};

export default AuthHandler;
