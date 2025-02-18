import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';

import Routes from "./routes";

import GlobalStyle  from './styles/global';

import { AuthProvider } from './context/AuthContext';

const App: React.FC = () => (
  <Router>
    <AuthProvider>
      <Routes />
    </AuthProvider>
    <GlobalStyle />
  </Router>
);

export default App;
