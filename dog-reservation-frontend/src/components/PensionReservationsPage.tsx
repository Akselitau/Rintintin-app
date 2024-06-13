import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

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

const PensionReservationsPage: React.FC = () => {
  const { user } = useAuth();
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReservations = async () => {
      if (user) {
        const token = localStorage.getItem('token');
        try {
          const pensionResponse = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/get-pension-user/${user.user_id}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          if (pensionResponse.data.pension) {
            const pensionId = pensionResponse.data.pension.pension_id;
            const reservationsResponse = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/get-reservations-pension/${pensionId}`, {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            });

            console.log('Reservations response:', reservationsResponse.data);

            if (reservationsResponse.data.reservations) {
              setReservations(reservationsResponse.data.reservations);
            } else {
              setError('No reservations found for this pension');
            }
          } else {
            setError('No pension found for user');
          }
        } catch (error) {
          console.error('Error fetching reservations:', error);
          setError('Error fetching reservations');
        } finally {
          setLoading(false);
        }
      }
    };

    fetchReservations();
  }, [user]);

  const updateReservationStatus = async (reservation_id: number, status: string) => {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_BASE_URL}/update-reservation`,
        {
          reservation_id,
          status
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.status === 200) {
        setReservations(prevReservations =>
          prevReservations.map(reservation =>
            reservation.reservation_id === reservation_id
              ? { ...reservation, status }
              : reservation
          )
        );
      } else {
        console.error('Failed to update reservation status');
      }
    } catch (error) {
      console.error('Error updating reservation status:', error);
    }
  };

  if (!user) {
    return <p>User is not logged in</p>;
  }

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h2>Réservations de la Pension</h2>
      <ul>
        {reservations.map((reservation) => (
          <li key={reservation.reservation_id}>
            <p><strong>Dog Name:</strong> {reservation.dog_name}</p>
            <p><strong>Dog Breed:</strong> {reservation.dog_breed}</p>
            <p><strong>Start Date:</strong> {reservation.start_date}</p>
            <p><strong>End Date:</strong> {reservation.end_date}</p>
            <p><strong>Status:</strong> {reservation.status}</p>
            <button onClick={() => updateReservationStatus(reservation.reservation_id, 'Accepted')}>Accept</button>
            <button onClick={() => updateReservationStatus(reservation.reservation_id, 'Rejected')}>Reject</button>
            <hr />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PensionReservationsPage;
