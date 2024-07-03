import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SignupPage.css';

const SignupPage: React.FC = () => {
  const [name, setName] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      const response = await axios.post('http://localhost:8000/create-user', {
        name: name,
        email: email,
        password: password,
      });
      alert('Account created successfully!');
      navigate('/login');
    } catch (error: any) {
      console.error('Error signing up:', error);
      alert('Error signing up: ' + (error.response?.data?.message || 'Unknown error'));
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-form">
        <h2>Create Account</h2>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Name"
          className="input-field"
        />
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
        <button onClick={handleSignup} className="signup-button">Create Account</button>
        <button onClick={() => navigate('/login')} className="login-button">Back to Login</button>
      </div>
    </div>
  );
};

export default SignupPage;
