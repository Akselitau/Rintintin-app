import React from 'react';
import './ContactPage.css';

const ContactPage: React.FC = () => {
  return (
    <div className="contact-page">
      <h1>Contactez-nous</h1>
      <p>
        Si vous avez des questions ou des préoccupations, n'hésitez pas à nous contacter via les informations ci-dessous :
      </p>
      <ul>
        <li>akseelmh@gmail.com</li>
      </ul>
      <p>
        Nous vous répondrons dès que possible.
      </p>
    </div>
  );
};

export default ContactPage;
