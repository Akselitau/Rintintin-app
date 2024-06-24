import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './MapComponent.css';

// Fix for default icon not showing
const DefaultIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

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

interface MapComponentProps {
  pensions: Pension[];
}

const MapComponent: React.FC<MapComponentProps> = ({ pensions }) => {
  return (
    // @ts-ignore
    <MapContainer center={[48.8566, 2.3522]} zoom={6} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        // @ts-ignore
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {pensions.map(pension => (
        <Marker key={pension.id} position={[pension.lat, pension.lon]}>
          <Popup>
            <b>{pension.name}</b><br />
            {pension.address}<br />
            {pension.phone}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapComponent;
