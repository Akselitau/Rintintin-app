import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

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
      <div className="login-form">
        <h2>Login</h2>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="input-field"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="input-field"
        />
        <button onClick={handleLogin} className="login-button">Login</button>
        <button onClick={() => navigate('/signup')} className="signup-button">Create Account</button>
      </div>
    </div>
  );
};

export default LoginPage;
