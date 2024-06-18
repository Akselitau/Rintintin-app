import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import './PensionInfo.css';

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

const PensionInfo: React.FC = () => {
  const { user } = useAuth();
  const [pension, setPension] = useState<Pension | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
          // eslint-disable-next-line jsx-a11y/img-redundant-alt
          <img key={index} src={url} alt={`Pension image ${index}`} />
        ))}
      </div>
    </div>
  );
};

export default PensionInfo;
