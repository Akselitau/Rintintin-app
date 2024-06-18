import React, { useState, useEffect } from 'react';
import './ModalUpdatePension.css';

interface ModalProps {
  show: boolean;
  handleClose: () => void;
  handleSave: (updatedPension: any) => void;
  pension: any;
}

const ModalComponent: React.FC<ModalProps> = ({ show, handleClose, handleSave, pension }) => {
  const [updatedPension, setUpdatedPension] = useState(pension);

  useEffect(() => {
    setUpdatedPension(pension);
  }, [pension]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setUpdatedPension((prev: any) => ({ ...prev, [name]: value }));
  };

  const onSave = () => {
    console.log('Saving data:', updatedPension); // Log the data to verify it
    handleSave(updatedPension);
  };

  return (
    <div className={`modal ${show ? 'show' : ''}`}>
      <div className="modal-content">
        <span className="close" onClick={handleClose}>&times;</span>
        <h2>Modifier les informations de la pension</h2>
        <input type="text" name="name" value={updatedPension.name} onChange={handleChange} placeholder="Nom" />
        <input type="text" name="address" value={updatedPension.address} onChange={handleChange} placeholder="Adresse" />
        <input type="text" name="phone" value={updatedPension.phone} onChange={handleChange} placeholder="Téléphone" />
        <input type="email" name="email" value={updatedPension.email} onChange={handleChange} placeholder="Email" />
        <input type="number" name="max_capacity" value={updatedPension.max_capacity} onChange={handleChange} placeholder="Capacité maximale" />
        <input type="number" name="current_occupancy" value={updatedPension.current_occupancy} onChange={handleChange} placeholder="Occupation actuelle" />
        <textarea name="description" value={updatedPension.description} onChange={handleChange} placeholder="Description"></textarea>
        <input type="text" name="hours" value={updatedPension.hours} onChange={handleChange} placeholder="Heures d'ouverture" />
        <button onClick={onSave}>Sauvegarder</button>
      </div>
    </div>
  );
};

export default ModalComponent;
