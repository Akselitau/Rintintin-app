import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Button, TextInput, Card, Heading } from 'evergreen-ui';
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
      <Card elevation={2} padding={32} borderRadius={8} className="login-form">
        <Heading size={700} marginBottom={24} className="login-title">Login</Heading>
        <TextInput
          value={email}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          placeholder="Email"
          className="input-field"
        />
        <TextInput
          type="password"
          value={password}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
          placeholder="Password"
          className="input-field"
        />
        <Button appearance="primary" onClick={handleLogin} className="login-button">Login</Button>
        <Button appearance="minimal" onClick={() => navigate('/signup')} className="signup-button">Create Account</Button>
      </Card>
    </div>
  );
};

export default LoginPage;
