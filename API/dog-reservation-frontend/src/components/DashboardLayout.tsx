import React from 'react';
import { Link, Outlet, useParams } from 'react-router-dom';
import './DashboardLayout.css';

const DashboardLayout: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();

  return (
    <div className="dashboard-layout">
      <div className="sidebar">
        <h2>Menu</h2>
        <ul>
          <li><Link to={`/dashboard/${userId}/info`}>Informations</Link></li>
          <li><Link to={`/dashboard/${userId}/pension-reservations`}>Réservations de la Pension</Link></li>
        </ul>
      </div>
      <div className="content">
        <Outlet />
      </div>
    </div>
  );
};

export default DashboardLayout;
