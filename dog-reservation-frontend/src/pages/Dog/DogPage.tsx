import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import Modal from 'react-modal';
import './DogPage.css';

Modal.setAppElement('#root');

const DogPage: React.FC = () => {
  const { user } = useAuth();
  const [dogs, setDogs] = useState<any[]>([]);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    breed: '',
    profile_photo_url: ''
  });

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

    if (user) {
      fetchDogs();
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
      } else {
        console.error('Failed to add dog');
      }
    } catch (error) {
      console.error('Error:', error);
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
        <form>
          <input type="text" name="name" placeholder="Nom" onChange={handleInputChange} />
          <input type="text" name="breed" placeholder="Race" onChange={handleInputChange} />
          <input type="text" name="profile_photo_url" placeholder="URL de la photo de profil" onChange={handleInputChange} />
          <button type="button" onClick={handleAddDog}>Ajouter un chien</button>
        </form>
        <button onClick={() => setModalIsOpen(false)}>Fermer</button>
      </Modal>
    </div>
    </div>
  );
};

export default DogPage;
