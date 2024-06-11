import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './CreatePensionPage.css';

const CreatePensionPage: React.FC = () => {
  const [name, setName] = useState('');
  const [address, setAddress] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [maxCapacity, setMaxCapacity] = useState(0);
  const [description, setDescription] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/create-pension', {
        name,
        address,
        phone,
        email,
        maxCapacity,
        description,
        imageUrl,
      });
      navigate('/my-pension');
    } catch (error) {
      console.error('Error creating pension:', error);
    }
  };

  return (
    <div className="create-pension-page">
      <h1>Créer une pension</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Nom:
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          Adresse:
          <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} required />
        </label>
        <label>
          Téléphone:
          <input type="text" value={phone} onChange={(e) => setPhone(e.target.value)} required />
        </label>
        <label>
          Email:
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Capacité maximale:
          <input type="number" value={maxCapacity} onChange={(e) => setMaxCapacity(parseInt(e.target.value))} required />
        </label>
        <label>
          Description:
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} required />
        </label>
        <label>
          URL de l'image:
          <input type="text" value={imageUrl} onChange={(e) => setImageUrl(e.target.value)} required />
        </label>
        <button type="submit">Créer</button>
      </form>
    </div>
  );
};

export default CreatePensionPage;
