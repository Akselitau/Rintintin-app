import React from 'react';
import './LegalPage.css';

const LegalPage: React.FC = () => {
  return (
    <div className="legal-page">
      <h1>Mentions légales</h1>
      <p>
        Bienvenue sur le site de RINTINTIN. Voici les informations légales concernant notre entreprise :
      </p>
      <h2>Informations sur l'entreprise</h2>
      <p>
        Nom de l'entreprise : RINTINTIN SAS<br />
        Adresse : 123 Rue de la Pension, 75000 Paris, France<br />
        Téléphone : +33 1 23 45 67 89<br />
        Email : contact@rintintin.com<br />
        Numéro SIRET : 123 456 789 00000
      </p>
      <h2>Hébergement du site</h2>
      <p>
        Notre site est hébergé par :<br />
        Nom de l'hébergeur : Hébergeur SAS<br />
        Adresse : 456 Rue de l'Hébergement, 75000 Paris, France<br />
        Téléphone : +33 1 98 76 54 32
      </p>
      <h2>Conditions d'utilisation</h2>
      <p>
        L'utilisation de ce site est soumise aux conditions d'utilisation suivantes. En utilisant ce site, vous acceptez ces conditions.
      </p>
    </div>
  );
};

export default LegalPage;
