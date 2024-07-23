import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import Modal from 'react-modal';
import { Pane, TextInputField, Button, SelectMenu } from 'evergreen-ui';
import { toast } from 'react-toastify';
import './DogPage.css';

Modal.setAppElement('#root');

const DogPage: React.FC = () => {
  const { user } = useAuth();
  const [dogs, setDogs] = useState<any[]>([]);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    breed: '',
    birthdate: '',
    profile_photo_url: ''
  });
  const [breeds, setBreeds] = useState<{ label: string, value: string }[]>([]);

  useEffect(() => {
    const fetchDogs = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/get-dogs/${user.user_id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          setDogs(data.dogs);
        } else {
          console.error('Failed to fetch dogs');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

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

    if (user) {
      fetchDogs();
      fetchBreeds();
    }
  }, [user]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleAddDog = async () => {
    const data = { ...formData, user_id: user.user_id };

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
        setDogs([...dogs, { ...data, dog_id: result.dog_id }]);
        setModalIsOpen(false);  // Ferme la modal après l'ajout du chien
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
    <div className="dog-background-container">
      <div className="dog-container">
        <h2>Mes Chiens</h2>
        {dogs.length > 0 ? (
          dogs.map(dog => (
            <div key={dog.dog_id} className="dog-details">
              <img src={dog.profile_photo_url || 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwXrptniMc0-eplVbfcJP42Hp-yChjpat0eXPG2XN_VT0olqpdMtDEpfLmusypE-9aV1Y&usqp=CAU'} alt={dog.name} />
              <div>
                <h3>{dog.name}</h3>
                <p>Race: {dog.breed}</p>
              </div>
            </div>
          ))
        ) : (
          <p>Vous n'avez pas encore de chiens enregistrés.</p>
        )}
        <button className="add-dog-button" onClick={() => setModalIsOpen(true)}>Ajouter un chien</button>

        <Modal
          isOpen={modalIsOpen}
          onRequestClose={() => setModalIsOpen(false)}
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
            <Button appearance="default" onClick={() => setModalIsOpen(false)} marginLeft={16}>
              Fermer
            </Button>
          </Pane>
        </Modal>
      </div>
    </div>
  );
};

export default DogPage;
