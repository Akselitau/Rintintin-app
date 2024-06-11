import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CreatePensionPage from './CreatePensionPage';
import { useAuth } from '../context/AuthContext';

interface Pension {
  id: number;
  name: string;
  address: string;
  phone: string;
  email: string;
  max_capacity: number;
  current_occupancy: number;
  rating: number;
  description: string;
  image_urls: string[];
  equipment: string[];
  size: string;
  hours: string;
}

const PensionPage: React.FC = () => {
  const { user } = useAuth();
  const [pension, setPension] = useState<Pension | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPension = async () => {
      if (user) {
        const token = localStorage.getItem('token');
        try {
          const response = await axios.get(`http://127.0.0.1:8000/get-pension-user/${user.user_id}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          console.log('Response:', response.data);
          if (response.data.pension) {
            setPension(response.data.pension);
          } else {
            setError('No pension found for user');
          }
        } catch (error) {
          console.error('Error fetching pension:', error);
          setError('Error fetching pension');
        } finally {
          setLoading(false);
        }
      }
    };

    fetchPension();
  }, [user]);

  if (!user) {
    return <p>User is not logged in</p>;
  }

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!pension) {
    return <CreatePensionPage />;
  }

  return (
    <div>
      <h1>{pension.name}</h1>
      <p><strong>Address:</strong> {pension.address}</p>
      <p><strong>Phone:</strong> {pension.phone}</p>
      <p><strong>Email:</strong> {pension.email}</p>
      <p><strong>Max Capacity:</strong> {pension.max_capacity}</p>
      <p><strong>Current Occupancy:</strong> {pension.current_occupancy}</p>
      <p><strong>Rating:</strong> {pension.rating}</p>
      <p><strong>Description:</strong> {pension.description}</p>
      <p><strong>Size:</strong> {pension.size}</p>
      <p><strong>Hours:</strong> {pension.hours}</p>
      <div>
        <h2>Equipment</h2>
        <ul>
          {pension.equipment.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
      <div>
        <h2>Images</h2>
        {pension.image_urls.map((url, index) => (
          <img key={index} src={url} alt={`Pension image ${index}`} style={{ width: '200px', margin: '10px' }} />
        ))}
      </div>
    </div>
  );
};

export default PensionPage;
