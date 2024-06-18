import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "./ReservationList.css"

interface Reservation {
  reservation_id: number;
  dog_id: number;
  pension_id: number;
  start_date: string;
  end_date: string;
  status: string;
  pension_name: string;
  dog_name: string;
  dog_breed: string;
}

interface ReservationListProps {
  userId?: number;
  pensionId?: number;
  canEdit?: boolean; // Indique si l'utilisateur peut modifier le statut
}

const ReservationList: React.FC<ReservationListProps> = ({ userId, pensionId, canEdit = false }) => {
  const [reservations, setReservations] = useState<Reservation[]>([]);

  useEffect(() => {
    const fetchReservations = async () => {
      try {
        let response;
        if (userId) {
          response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/get-reservations-user/${userId}`);
        } else if (pensionId) {
          response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/get-reservations-pension/${pensionId}`);
        }
        if (response && response.data) {
          setReservations(response.data.reservations);
        }
      } catch (error) {
        console.error('Error fetching reservations:', error);
      }
    };

    fetchReservations();
  }, [userId, pensionId]);

  const handleStatusChange = async (reservationId: number, newStatus: string) => {
    try {
      await axios.post(`${process.env.REACT_APP_API_BASE_URL}/update-reservation`, {
        reservation_id: reservationId,
        status: newStatus
      });
      setReservations(reservations.map(reservation => 
        reservation.reservation_id === reservationId ? { ...reservation, status: newStatus } : reservation
      ));
    } catch (error) {
      console.error('Error updating reservation status:', error);
    }
  };

  return (
    <div className="reservation-list">
      {reservations.length === 0 ? (
        <p>Vous n'avez pas de réservation pour le moment</p>
      ) : (
        reservations.map((reservation) => (
          <div key={reservation.reservation_id} className="reservation-card">
            <h2>Réservation pour {reservation.dog_name}</h2>
            <p>Pension: {reservation.pension_name}</p>
            <p>Date de début: {reservation.start_date}</p>
            <p>Date de fin: {reservation.end_date}</p>
            <p>Chien: {reservation.dog_name} ({reservation.dog_breed})</p>
            <p>Status: {reservation.status}</p>
            {canEdit && (
              <>
                <button onClick={() => handleStatusChange(reservation.reservation_id, 'Accepted')}>Accepter</button>
                <button onClick={() => handleStatusChange(reservation.reservation_id, 'Rejected')}>Rejeter</button>
              </>
            )}
          </div>
        ))
      )}
    </div>
  );
};

export default ReservationList;
