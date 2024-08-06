import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';

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
  const [error, setError] = useState<string | null>('Tu n\'as pas de pension pour l\'instant. Veuillez en créer une pour voir les réservations.');

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

            if (reservationsResponse.data.reservations.length > 0) {
              setReservations(reservationsResponse.data.reservations);
              setError(null);
            } else {
              setError('Aucune réservation trouvée pour cette pension');
            }
          } else {
            setError('Tu n\'as pas de pension pour l\'instant. Veuillez en créer une pour voir les réservations.');
          }
        } catch (error) {
          if (axios.isAxiosError(error) && error.response?.status === 404) {
            setError('Tu n\'as pas de pension pour l\'instant. Veuillez en créer une pour voir les réservations.');
          } else {
            setError('Erreur lors de la récupération des réservations');
          }
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
        console.error('Échec de la mise à jour du statut de la réservation');
      }
    } catch (error) {
      console.error('Erreur lors de la mise à jour du statut de la réservation:', error);
    }
  };

  if (!user) {
    return <p>L'utilisateur n'est pas connecté</p>;
  }

  if (loading) {
    return <p>Chargement...</p>;
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
            <p><strong>Nom du chien:</strong> {reservation.dog_name}</p>
            <p><strong>Race du chien:</strong> {reservation.dog_breed}</p>
            <p><strong>Date de début:</strong> {reservation.start_date}</p>
            <p><strong>Date de fin:</strong> {reservation.end_date}</p>
            <p><strong>Statut:</strong> {reservation.status}</p>
            <button onClick={() => updateReservationStatus(reservation.reservation_id, 'Accepted')}>Accepter</button>
            <button onClick={() => updateReservationStatus(reservation.reservation_id, 'Rejected')}>Rejeter</button>
            <hr />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PensionReservationsPage;
