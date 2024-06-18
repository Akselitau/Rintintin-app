import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import ModalComponent from './ModalUpdatePension';
import './PensionInfo.css';

const PensionInfo: React.FC = () => {
  const { user } = useAuth();
  const [pension, setPension] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);

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
          } else {
            setError('No pension found for user');
          }
        } catch (error) {
          setError('Error fetching pension');
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
        toast.success('Pension updated successfully!');
        setShowModal(false);
        setPension(updatedPension); // Mettre à jour l'état de la pension avec les nouvelles données
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.error('Error updating pension:', error.response?.data || error.message);
          toast.error(`Error updating pension: ${error.response?.data.message || error.message}`);
        } else {
          console.error('Unexpected error updating pension:', error);
          toast.error('Unexpected error occurred');
        }
      }
    }
  };

  if (!user) {
    return <p className="error">User is not logged in</p>;
  }

  if (loading) {
    return <p className="loading">Loading...</p>;
  }

  if (error) {
    return <p className="error">{error}</p>;
  }

  if (!pension) {
    return <p className="error">No pension found. Please create one.</p>;
  }

  return (
    <div className="pension-info">
      <h1>{pension.name}</h1>
      <p><strong>Address:</strong> {pension.address}</p>
      <p><strong>Phone:</strong> {pension.phone}</p>
      <p><strong>Email:</strong> {pension.email}</p>
      <p><strong>Max Capacity:</strong> {pension.max_capacity}</p>
      <p><strong>Current Occupancy:</strong> {pension.current_occupancy}</p>
      <p><strong>Rating:</strong> {pension.rating}</p>
      <p><strong>Description:</strong> {pension.description}</p>
      <p><strong>Hours:</strong> {pension.hours}</p>
      <div>
        <h2>Equipment</h2>
        <ul>
          {pension.equipment.map((item: string, index: number) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
      <div>
        <h2>Images</h2>
        {pension.image_urls.map((url: string, index: number) => (
          // eslint-disable-next-line jsx-a11y/img-redundant-alt
          <img key={index} src={url} alt={`Pension image ${index}`} />
        ))}
      </div>
      <button onClick={() => setShowModal(true)}>Update Pension</button>
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
