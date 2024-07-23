import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import { useAuth } from '../context/AuthContext';
import { Pane, TextInputField, Button, SelectMenu } from 'evergreen-ui';
import { toast } from 'react-toastify';

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
    birthdate: '',
    profile_photo_url: ''
  });
  const [breeds, setBreeds] = useState<{ label: string, value: string }[]>([]);

  useEffect(() => {
    const fetchBreeds = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/get-dog-breeds`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          setBreeds(data.breeds.map((breed: { breed_id: number, name: string }) => ({ label: breed.name, value: breed.name })));
        } else {
          console.error('Failed to fetch dog breeds');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchBreeds();
  }, []);

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
        toast.success('Chien ajouté avec succès !');
      } else {
        console.error('Failed to add dog');
        toast.error('Erreur lors de l\'ajout du chien');
      }
    } catch (error) {
      console.error('Error:', error);
      toast.error('Erreur lors de l\'ajout du chien : Erreur inconnue');
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="Ajouter un chien"
    >
      <h2>Ajouter un chien</h2>
      <Pane className="form-section">
        <TextInputField
          label="Nom du chien"
          placeholder="Nom du chien"
          name="name"
          value={formData.name}
          onChange={handleInputChange}
        />
        <SelectMenu
          title="Sélectionner une race"
          options={breeds}
          selected={formData.breed}
          onSelect={(item: any) => setFormData({ ...formData, breed: item.value })}
        >
          <Button>{formData.breed || 'Sélectionner une race'}</Button>
        </SelectMenu>
        <TextInputField
          label="Date de naissance"
          placeholder="Date de naissance"
          type="date"
          name="birthdate"
          value={formData.birthdate}
          onChange={handleInputChange}
        />
        <TextInputField
          label="URL de la photo de profil"
          placeholder="URL de la photo de profil"
          name="profile_photo_url"
          value={formData.profile_photo_url}
          onChange={handleInputChange}
        />
        <Button
          appearance="primary"
          onClick={handleAddDog}
          disabled={!formData.name || !formData.breed || !formData.birthdate}
        >
          Ajouter un chien
        </Button>
        <Button appearance="default" onClick={onRequestClose} marginLeft={16}>
          Fermer
        </Button>
      </Pane>
    </Modal>
  );
};

export default AddDogModal;
