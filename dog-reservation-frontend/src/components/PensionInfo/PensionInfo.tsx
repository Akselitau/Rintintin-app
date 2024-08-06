import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import ModalComponent from '../../modals/ModalUpdatePension';
import './PensionInfo.css';

const PensionInfo: React.FC = () => {
  const { user } = useAuth();
  const [pension, setPension] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);  // Ajout de l'état pour la modal

  useEffect(() => {
    const fetchPension = async () => {
      if (user) {
        const token = localStorage.getItem('token');
        try {
          const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/get-pension-user/${user.user_id}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          if (response.data.pension) {
            setPension(response.data.pension);
            setError(null); // Clear any existing error
          } else {
            setPension(null);
            setError('Tu n\'as pas de pension pour l\'instant. Veuillez en créer une pour voir les détails.');
          }
        } catch (error) {
          if (axios.isAxiosError(error) && error.response?.status === 404) {
            setError('Tu n\'as pas de pension pour l\'instant. Veuillez en créer une pour voir les détails.');
          } else {
            setError('Erreur lors de la récupération de la pension');
          }
        } finally {
          setLoading(false);
        }
      }
    };

    fetchPension();
  }, [user]);

  const handleUpdatePension = async (updatedPension: any) => {
    const updatedPensionData = {
      id: updatedPension.pension_id,
      name: updatedPension.name,
      address: updatedPension.address,
      phone: updatedPension.phone,
      email: updatedPension.email,
      max_capacity: updatedPension.max_capacity,
      current_occupancy: updatedPension.current_occupancy,
      rating: updatedPension.rating,
      description: updatedPension.description,
      image_urls: updatedPension.image_urls,
      equipment: updatedPension.equipment,
      hours: updatedPension.hours,
      night_price: updatedPension.night_price,
    };

    if (user) {
      const token = localStorage.getItem('token');
      try {
        const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/update-pension`, updatedPensionData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log('Update Response:', response.data);
        toast.success('Pension mise à jour avec succès !');
        setPension(updatedPension); // Mettre à jour l'état de la pension avec les nouvelles données
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.error('Erreur lors de la mise à jour de la pension:', error.response?.data || error.message);
          toast.error(`Erreur lors de la mise à jour de la pension: ${error.response?.data.message || error.message}`);
        } else {
          console.error('Erreur inattendue lors de la mise à jour de la pension:', error);
          toast.error('Une erreur inattendue est survenue');
        }
      }
    }
  };

  if (!user) {
    return <p className="error">L'utilisateur n'est pas connecté</p>;
  }

  if (loading) {
    return <p className="loading">Chargement...</p>;
  }

  if (error) {
    return <p className="error">{error}</p>;
  }

  if (!pension) {
    return <p className="info">Tu n'as pas de pension pour l'instant. Veuillez en créer une pour voir les détails.</p>;
  }

  return (
    <div className="pension-info">
      <h1>{pension.name}</h1>
      <p><strong>Adresse:</strong> {pension.address}</p>
      <p><strong>Téléphone:</strong> {pension.phone}</p>
      <p><strong>Email:</strong> {pension.email}</p>
      <p><strong>Capacité Max:</strong> {pension.max_capacity}</p>
      <p><strong>Occupation Actuelle:</strong> {pension.current_occupancy}</p>
      <p><strong>Évaluation:</strong> {pension.rating}</p>
      <p><strong>Description:</strong> {pension.description}</p>
      <p><strong>Heures:</strong> {pension.hours}</p>
      <div>
        <h2>Équipements</h2>
        <ul>
          {pension.equipment.map((item: string, index: number) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
      <div>
        <h2>Images</h2>
        {pension.image_urls.map((url: string, index: number) => (
          <img key={index} src={url} alt={`Pension view ${index + 1}`} />
        ))}
      </div>
      <button onClick={() => setShowModal(true)}>Mettre à jour la pension</button>
      <ModalComponent
        show={showModal}
        handleClose={() => setShowModal(false)}
        handleSave={handleUpdatePension}
        pension={pension}
      />
    </div>
  );
};

export default PensionInfo;
