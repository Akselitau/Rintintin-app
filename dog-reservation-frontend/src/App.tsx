import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './components/HomePage';
import PensionList from './components/PensionList';
import PensionDetail from './components/PensionDetail';
import LoginPage from './components/LoginPage';
import SignupPage from './components/SignupPage';
import DogPage from './components/DogPage';
import ProfilePage from './components/ProfilePage';
import ReservationsPage from './components/ReservationsPage';
import Footer from './components/Footer';
import { AuthProvider } from './context/AuthContext';
import RegisterPension from './components/RegisterPension';
import ContactPage from './components/ContactPage';
import LegalPage from './components/LegalPage';
import DashboardPage from './components/DashboardPage';
import PensionInfo from './components/PensionInfo';
import PensionReservationsPage from './components/PensionReservationsPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AlphaBanner from './components/AlphaBanner'; // Importer le nouveau composant

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <AlphaBanner /> {/* Ajouter le composant AlphaBanner ici */}
          <Navbar />
          <div className="content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/pensions" element={<PensionList />} />
              <Route path="/pensions/:id" element={<PensionDetail />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/my-pension/*" element={<DashboardPage />}>
                <Route path="info" element={<PensionInfo />} />
                <Route path="reservations" element={<PensionReservationsPage />} />
              </Route>
              <Route path="/my-dog" element={<DogPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/reservations" element={<ReservationsPage />} />
              <Route path="/register-pension" element={<RegisterPension />} />
              <Route path="/contact" element={<ContactPage />} />
              <Route path="/legal" element={<LegalPage />} />
            </Routes>
          </div>
          <Footer />
          <ToastContainer />
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
