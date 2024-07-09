import React from 'react';
import './ContactPage.css';

const ContactPage: React.FC = () => {
  return (
    <div className="contact-page">
      <h1>Contactez-nous</h1>
      <p>
        Si vous avez des questions ou des préoccupations, n'hésitez pas à nous contacter via les informations ci-dessous :
      </p>
      <p>
        akseelmh@gmail.com
      </p>
      <p>
        N'oubliez pas de joindre vos coordonnées à votre message si vous souhaitez être recontacté plus rapidement. Nous vous répondrons dès que possible.
      </p>
    </div>
  );
};

export default ContactPage;
