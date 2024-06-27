import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import HomePage from './pages/Home/HomePage';
import PensionList from './components/PensionList/PensionList';
import PensionDetail from './pages/PensionDetail/PensionDetail';
import LoginPage from './pages/Login/LoginPage';
import SignupPage from './pages/Signup/SignupPage';
import DogPage from './pages/Dog/DogPage';
import ProfilePage from './pages/Profile/ProfilePage';
import Footer from './components/Footer/Footer';
import { AuthProvider } from './context/AuthContext';
import RegisterPension from './components/RegisterPension/RegisterPension';
import ContactPage from './pages/Contact/ContactPage';
import LegalPage from './pages/Legal/LegalPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import PensionInfo from './components/PensionInfo/PensionInfo';
import PensionReservationsPage from './pages/PensionReservation/PensionReservationsPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AlphaBanner from './components/BannerAlphaWarning/AlphaBanner';
import ReservationsPage from './pages/Reservations/ReservationsPage';
import AuthHandler from './context/AuthHandler';

const App: React.FC = () => {
  return (
    <Router>
      <AuthProvider>
        <div className="App">
          <AlphaBanner />
          <Navbar />
          <div className="content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/pensions" element={<PensionList />} />
              <Route path="/pensions/:id" element={<PensionDetail />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/auth/login" element={<AuthHandler />} />
              <Route path="/auth/signup" element={<AuthHandler />} />
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
      </AuthProvider>
    </Router>
  );
};

export default App;
