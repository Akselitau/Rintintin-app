import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { StytchProvider } from '@stytch/react';
import { StytchUIClient } from '@stytch/vanilla-js';
import { StytchAuthProvider } from './context/StytchContext';

console.log("Stytch Public Token:", process.env.REACT_APP_STYTCH_PUBLIC_TOKEN);
const stytchClient = new StytchUIClient(process.env.REACT_APP_STYTCH_PUBLIC_TOKEN || '');

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

root.render(
  <React.StrictMode>
    <StytchProvider stytch={stytchClient}>
      <StytchAuthProvider>
        <App />
      </StytchAuthProvider>
    </StytchProvider>
  </React.StrictMode>
);

reportWebVitals();
