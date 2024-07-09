import React from 'react';
import { Link, Outlet } from 'react-router-dom';
import './DashboardPage.css';

const DashboardPage: React.FC = () => {
  return (
    <div className="dashboard-page">
      <div className="sidebar">
        <h2>Menu</h2>
        <ul>
          <li><Link to="info">Informations de la Pension</Link></li>
          <li><Link to="reservations">Réservations</Link></li>
        </ul>
      </div>
      <div className="content">
        <Outlet />
      </div>
    </div>
  );
};

export default DashboardPage;
