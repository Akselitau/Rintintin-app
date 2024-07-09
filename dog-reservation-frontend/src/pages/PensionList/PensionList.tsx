import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import PensionCard from '../../components/PensionCard/PensionCard';
import SearchBar from '../../components/SearchBar/SearchBar';
import MapComponent from '../../components/Map/MapComponent';
import { ClipLoader } from 'react-spinners'; // Import the spinner
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
  status: string;
  lat: number;
  lon: number;
}

const PensionList: React.FC = () => {
  const location = useLocation();
  const { address, coordinates } = location.state || {};
  const [pensions, setPensions] = useState<Pension[]>([]);
  const [loading, setLoading] = useState(true);
  const [center, setCenter] = useState<{ lat: number, lon: number } | undefined>(coordinates);

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
      const fetchedPensions: Pension[] = response.data.pensions;
      
      // Get coordinates for each pension
      for (const pension of fetchedPensions) {
        const [lat, lon] = await getCoordinates(pension.address);
        pension.lat = lat;
        pension.lon = lon;
      }
      
      setPensions(fetchedPensions);
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
    getCoordinates(address).then((coords) => {
      setCenter({ lat: coords[0], lon: coords[1] });
      fetchPensions(address, { lat: coords[0], lon: coords[1] });
    });
  };

  return (
    <div className="pension-list-container">
      <SearchBar withMarginTop={false} onSearch={handleSearch} />
      <div className="content-container">
        <div className="pension-cards">
          {loading ? (
            <ClipLoader size={50} color={"#e0b127"} loading={loading} /> // Use the spinner
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
        {center && (
          <div className="map-container">
            <MapComponent pensions={pensions} center={center} />
          </div>
        )}
      </div>
    </div>
  );
};

export default PensionList;

async function getCoordinates(address: string): Promise<[number, number]> {
  try {
    const response = await axios.get('https://nominatim.openstreetmap.org/search', {
      params: {
        q: address,
        format: 'json',
        limit: 1
      },
      headers: {
        'User-Agent': 'my-app/1.0.0'
      }
    });

    if (response.data && response.data.length > 0) {
      const lat = parseFloat(response.data[0].lat);
      const lon = parseFloat(response.data[0].lon);
      return [lat, lon];
    }
  } catch (error) {
    console.error('Error fetching coordinates:', error);
  }
  return [0, 0];
}
