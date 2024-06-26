// src/pages/Signup/SignupPage.tsx
import React, { useState } from 'react';
import { useStytch } from '@stytch/react';
import './SignupPage.css';

const SignupPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const stytch = useStytch();

  const handleSignup = async () => {
    try {
      // @ts-ignore
      await stytch.magicLinks.email.loginOrCreate({
        email,
        login_magic_link_url: `${window.location.origin}/auth/login`,
        signup_magic_link_url: `${window.location.origin}/auth/signup`,
      });
      alert('Check your email for the signup link!');
    } catch (error) {
      console.error('Error signing up:', error);
      // @ts-ignore
      alert('Error signing up: ' + (error.message || 'Unknown error'));
    }
  };

  return (
    <div className="signup-container">
      <h2>Signup</h2>
      <div className="signup-form">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button onClick={handleSignup}>Signup</button>
      </div>
    </div>
  );
};

export default SignupPage;
