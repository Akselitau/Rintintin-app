import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import PensionCard from './PensionCard';
import SearchBar from './SearchBar';
import './PensionList.css';

interface Pension {
  id: number;
  name: string;
  address: string;
  phone: string;
  email: string;
  maxCapacity: number;
  currentOccupancy: number;
  rating: number;
  description: string;
  imageUrls: string[];
  distance_km?: number;
  status: string; // Ajout du champ status
}

const PensionList: React.FC = () => {
  const location = useLocation();
  const { address, coordinates } = location.state || {};
  const [pensions, setPensions] = useState<Pension[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchPensions = async (address?: string, coordinates?: { lat: number, lon: number }) => {
    try {
      setLoading(true);
      const params: any = {};
      if (address) params.address = address;
      if (coordinates) {
        params.lat = coordinates.lat;
        params.lon = coordinates.lon;
      }

      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/get-pensions`, { params });
      setPensions(response.data.pensions);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching pensions:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPensions(address, coordinates);
  }, [address, coordinates]);

  const handleSearch = (address: string) => {
    fetchPensions(address);
  };

  return (
    <div className="pension-list-container">
      <SearchBar withMarginTop={false} onSearch={handleSearch} />
      <div className="pension-list">
        {loading ? (
          <p>Loading...</p>
        ) : (
          pensions.map(pension => (
            <PensionCard
              key={pension.id}
              id={pension.id}
              imageUrls={pension.imageUrls}
              name={pension.name}
              rating={pension.rating}
              address={pension.address}
              description={pension.description}
              distanceKm={pension.distance_km}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default PensionList;
