import React, { useState } from 'react';
import './PasswordForgotten.css';

const PasswordForgottenPage: React.FC = () => {
  const [email, setEmail] = useState('');

  const handlePasswordReset = (event: React.FormEvent) => {
    event.preventDefault();
    console.log('Réinitialiser le mot de passe pour:', email);
  };

  return (
    <div className="password-forgotten-container">
      <h2>Réinitialiser le mot de passe</h2>
      <form onSubmit={handlePasswordReset}>
        <div className="form-group">
          <label htmlFor="email">Adresse e-mail :</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit">Réinitialiser le mot de passe</button>
      </form>
    </div>
  );
};

export default PasswordForgottenPage;
