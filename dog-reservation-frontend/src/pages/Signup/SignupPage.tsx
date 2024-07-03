import React, { useState } from 'react';
import axios from 'axios';
import { TextInputField, Button, Text, Pane } from 'evergreen-ui';
import './SignupPage.css';

const SignupPage: React.FC = () => {
  const [name, setName] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleSignup = async () => {
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      await axios.post('http://localhost:8000/create-user', { name, email, password });
      alert('Account created successfully!');
    } catch (error: any) {
      console.error('Error signing up:', error);
      alert('Error signing up: ' + (error.response?.data?.message || 'Unknown error'));
    }
  };

  return (
    <Pane>
      <TextInputField
        label="Name"
        value={name}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setName(e.target.value)}
        placeholder="Name"
      />
      <TextInputField
        label="Email"
        value={email}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <TextInputField
        label="Password"
        type="password"
        value={password}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <TextInputField
        label="Confirm Password"
        type="password"
        value={confirmPassword}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setConfirmPassword(e.target.value)}
        placeholder="Confirm Password"
      />
      {error && <Text color="danger">{error}</Text>}
      <Button onClick={handleSignup} appearance="primary">Create Account</Button>
    </Pane>
  );
};

export default SignupPage;
