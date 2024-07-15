import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import HomePage from './pages/Home/HomePage';
import PensionList from './pages/PensionList/PensionList';
import PensionDetail from './pages/PensionDetail/PensionDetail';
import LoginPage from './pages/Login/LoginPage';
import SignupAddDogPage from './pages/SignupAddDog/SignupAddDogPage';
import DogPage from './pages/Dog/DogPage';
import ProfilePage from './pages/Profile/ProfilePage';
import Footer from './components/Footer/Footer';
import { AuthProvider, useAuth } from './context/AuthContext';
import RegisterPension from './pages/RegisterPension/RegisterPension';
import ContactPage from './pages/Contact/ContactPage';
import LegalPage from './pages/Legal/LegalPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import PensionInfo from './components/PensionInfo/PensionInfo';
import PensionReservationsPage from './pages/PensionReservation/PensionReservationsPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AlphaBanner from './components/BannerAlphaWarning/AlphaBanner';
import ReservationsPage from './pages/Reservations/ReservationsPage';
import AboutPage from './pages/About/About';
import PasswordForgotten from './pages/PasswordForgotten/PasswordForgotten';

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <LoginPage />;
};

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
              <Route path="/password-forgotten" element={<PasswordForgotten/>} />
              <Route path="/signup" element={<SignupAddDogPage />} />
              <Route
                path="/my-pension/*"
                element={
                  <ProtectedRoute>
                    <DashboardPage />
                  </ProtectedRoute>
                }
              >
                <Route path="info" element={<PensionInfo />} />
                <Route path="reservations" element={<PensionReservationsPage />} />
              </Route>
              <Route path="/my-dog" element={<DogPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/reservations" element={<ReservationsPage />} />
              <Route path="/register-pension" element={<RegisterPension />} />
              <Route path="/contact" element={<ContactPage />} />
              <Route path="/legal" element={<LegalPage />} />
              <Route path="/about" element={<AboutPage />} />
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
