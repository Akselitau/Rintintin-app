import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useOutletContext } from 'react-router-dom';

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
  image_url: string;
  latitude: number;
  longitude: number;
}

interface OutletContext {
  userId: number;
  pensionId: number;
}

const PensionInfo: React.FC = () => {
  const { pensionId } = useOutletContext<OutletContext>();
  const [pension, setPension] = useState<Pension | null>(null);

  useEffect(() => {
    const fetchPension = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/get-pension/${pensionId}`);
        setPension(response.data.pension);
      } catch (error) {
        console.error('Error fetching pension:', error);
      }
    };

    fetchPension();
  }, [pensionId]);

  if (!pension) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h1>{pension.name}</h1>
      <img src={pension.image_url} alt={pension.name} />
      <p><strong>Adresse:</strong> {pension.address}</p>
      <p><strong>Téléphone:</strong> {pension.phone}</p>
      <p><strong>Email:</strong> {pension.email}</p>
      <p><strong>Capacité maximale:</strong> {pension.max_capacity}</p>
      <p><strong>Occupancy actuelle:</strong> {pension.current_occupancy}</p>
      <p><strong>Évaluation:</strong> {pension.rating}</p>
      <p><strong>Description:</strong> {pension.description}</p>
      <p><strong>Latitude:</strong> {pension.latitude}</p>
      <p><strong>Longitude:</strong> {pension.longitude}</p>
    </div>
  );
};

export default PensionInfo;
