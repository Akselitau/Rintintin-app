import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStytch } from '@stytch/react';
import './LoginPage.css';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const stytchClient = useStytch();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      console.log("Email:", email, "Type:", typeof email);
      await stytchClient.magicLinks.email.loginOrCreate({
        email: String(email), // Ensure email is a string
        login_magic_link_url: `${window.location.origin}/auth/login`,
        signup_magic_link_url: `${window.location.origin}/auth/signup`,
      } as any);
      alert('Magic link sent! Check your email.');
    } catch (error: any) {
      console.error('Error logging in:', error);
      alert('Error logging in: ' + (error.message || 'Unknown error'));
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button onClick={handleLogin}>Login</button>
      <button onClick={() => handleLogin()}>Login with test email</button>
    </div>
  );
};

export default LoginPage;
