import React, { useState } from 'react';
import Modal from 'react-modal';
import { useAuth } from '../context/AuthContext';

Modal.setAppElement('#root'); // Important pour l'accessibilité

interface AddDogModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
  onDogAdded: (dog: any) => void;
}

const AddDogModal: React.FC<AddDogModalProps> = ({ isOpen, onRequestClose, onDogAdded }) => {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    breed: '',
    profile_photo_url: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleAddDog = async () => {
    const data = { ...formData, user_id: user?.user_id };

    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/create-dog-profile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Dog added successfully:', result);
        onDogAdded({ ...data, dog_id: result.dog_id });
        onRequestClose(); // Ferme la modal après l'ajout du chien
      } else {
        console.error('Failed to add dog');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="Ajouter un chien"
    >
      <h2>Ajouter un chien</h2>
      <form>
        <input type="text" name="name" placeholder="Nom" onChange={handleInputChange} />
        <input type="text" name="breed" placeholder="Race" onChange={handleInputChange} />
        <input type="text" name="profile_photo_url" placeholder="URL de la photo de profil" onChange={handleInputChange} />
        <button type="button" onClick={handleAddDog}>Ajouter un chien</button>
      </form>
      <button onClick={onRequestClose}>Fermer</button>
    </Modal>
  );
};

export default AddDogModal;
