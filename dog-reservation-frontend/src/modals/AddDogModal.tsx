import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import { useAuth } from '../context/AuthContext';
import { Pane, TextInputField, Button, SelectMenu } from 'evergreen-ui';
import { toast } from 'react-toastify';
import './AddDogModal.css';

Modal.setAppElement('#root');

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
    profile_photo: null as File | null,
    information: ''  // Ajout de l'information
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
    const { name, value, files } = e.target;
    if (name === 'profile_photo' && files) {
      setFormData({ ...formData, profile_photo: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleAddDog = async () => {
    if (!formData.profile_photo) {
        toast.error('Please select a photo for the dog.');
        return;
    }

    try {
        // Generate presigned URL
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/generate-upload-url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                file_name: formData.profile_photo.name,
                file_type: formData.profile_photo.type
            })
        });

        const presignedData = await response.json();

        // Upload file to S3
        const formDataForS3 = new FormData();
        Object.keys(presignedData.fields).forEach(key => {
            formDataForS3.append(key, presignedData.fields[key]);
        });
        formDataForS3.append('file', formData.profile_photo);

        const uploadResponse = await fetch(presignedData.url, {
            method: 'POST',
            body: formDataForS3
        });

        if (uploadResponse.ok) {
            // Corriger l'URL ici
            const imageUrl = `${presignedData.url}${presignedData.fields.key}`;
            // Create dog profile
            const profileResponse = await fetch(`${process.env.REACT_APP_API_BASE_URL}/create-dog-profile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    user_id: user.user_id,
                    name: formData.name,
                    breed: formData.breed,
                    birthdate: formData.birthdate,
                    information: formData.information,
                    profile_photo_url: imageUrl  // URL corrigée
                })
            });

            if (profileResponse.ok) {
                const newDog = await profileResponse.json();
                toast.success('Dog profile created successfully!');
                onDogAdded(newDog);
                onRequestClose();
            } else {
                toast.error('Failed to create dog profile');
            }
        } else {
            toast.error('Failed to upload file to S3');
        }
    } catch (error) {
        console.error('Error:', error);
        toast.error('An error occurred while uploading the dog photo');
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
          label="Informations supplémentaires"
          placeholder="Informations sur le chien"
          name="information"
          value={formData.information}
          onChange={handleInputChange}
        />
        <TextInputField
          label="Photo de profil"
          placeholder="Photo de profil"
          name="profile_photo"
          type="file"
          onChange={handleInputChange}
        />
        <div className="button-group">
          <Button
            appearance="primary"
            onClick={handleAddDog}
            disabled={!formData.name || !formData.breed || !formData.birthdate}
          >
            Ajouter un chien
          </Button>
          <Button appearance="default" onClick={onRequestClose}>
            Fermer
          </Button>
        </div>
      </Pane>
    </Modal>
  );
};

export default AddDogModal;
