import React from 'react';
import './RegisterPension.css';

const RegisterPension: React.FC = () => {
  return (
    <div className="pension-signup-container">
      <h1>Je suis une pension</h1>
      <p>
        Si vous êtes une pension et que vous souhaitez rejoindre notre plateforme, suivez les étapes ci-dessous pour créer votre compte :
      </p>
      <div className="steps-container">
        <div className="step">
          <h2>Étape 1 : Inscription</h2>
          <p>
            Cliquez sur le bouton <strong>Inscription</strong> en haut à droite de cette page et remplissez le formulaire d'inscription avec vos informations personnelles.
          </p>
        </div>
        <div className="step">
          <h2>Étape 2 : Validation de l'email</h2>
          <p>
            Vous recevrez un email de validation. Cliquez sur le lien de validation dans l'email pour confirmer votre adresse.
          </p>
        </div>
        <div className="step">
          <h2>Étape 3 : Création de votre profil</h2>
          <p>
            Connectez-vous à votre compte et complétez votre profil de pension. Fournissez des informations détaillées sur votre pension, y compris l'adresse, le nombre de places disponibles, et des photos.
          </p>
        </div>
        <div className="step">
          <h2>Étape 4 : Mise en ligne</h2>
          <p>
            Une fois votre profil complété, soumettez-le pour approbation. Nous vérifierons vos informations et votre profil sera mis en ligne une fois approuvé.
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPension;
