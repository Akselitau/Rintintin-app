import React from 'react';
import './RegisterPension.css';

const RegisterPension: React.FC = () => {
  return (
    <div className="register-pension">
      <h1>Inscrire sa pension sur RINTINTIN</h1>
      <p>
        Bienvenue sur RINTINTIN! Pour inscrire votre pension, suivez les étapes suivantes :
      </p>
      <ol>
        <li>Créez un compte en cliquant sur le bouton "Connexion" en haut à droite.</li>
        <li>Une fois connecté, allez sur votre profil et cliquez sur "Ma pension".</li>
        <li>Remplissez les informations nécessaires sur votre pension, y compris l'adresse, les équipements, la capacité maximale, etc.</li>
        <li>Ajoutez des photos pour mettre en valeur votre pension.</li>
        <li>Une fois toutes les informations remplies, cliquez sur "Soumettre" pour enregistrer votre pension.</li>
      </ol>
      <p>
        Si vous avez des questions, n'hésitez pas à nous contacter via notre page de contact.
      </p>
    </div>
  );
};

export default RegisterPension;
