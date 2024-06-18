import React from 'react';
import ReservationList from '../../components/ReservationList/ReservationList';
import { useAuth } from '../../context/AuthContext';

const ReservationsPage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div>
      <h1>Mes Réservations</h1>
      {user ? <ReservationList userId={user.user_id} /> : <p>User is not logged in</p>}
    </div>
  );
};

export default ReservationsPage;
