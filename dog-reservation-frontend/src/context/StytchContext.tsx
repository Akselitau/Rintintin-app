// src/context/StytchContext.tsx
import React, { createContext, useContext, ReactNode } from 'react';
import { StytchProvider, useStytch } from '@stytch/react';

const StytchContext = createContext(null);

export const StytchAuthProvider = ({ children }: { children: ReactNode }) => {
  const stytch = useStytch();

  return (
    // @ts-ignore
    <StytchContext.Provider value={stytch}>
      {children}
    </StytchContext.Provider>
  );
};

export const useStytchAuth = () => useContext(StytchContext);
