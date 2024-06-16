import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import Modal from 'react-modal';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './PensionInfo.css';

interface Pension {
  id: number;
  name: string;
  address: string;
  phone: string;
  email: string;
  max_capacity: number;
  current_occupancy: number;
  rating: number;
  description: string;
  image_urls: string[];
  equipment: string[];
  size: string;
  hours: string;
}

const PensionInfo: React.FC = () => {
  const { user } = useAuth();
  const [pension, setPension] = useState<Pension | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [updatedPension, setUpdatedPension] = useState<Pension | null>(null);

  useEffect(() => {
    const fetchPension = async () => {
      if (user) {
        const token = localStorage.getItem('token');
        try {
          const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/get-pension-user/${user.user_id}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          console.log('Response:', response.data);
          if (response.data.pension) {
            setPension(response.data.pension);
            setUpdatedPension(response.data.pension);
          } else {
            setError('No pension found for user');
          }
        } catch (error) {
          console.error('Error fetching pension:', error);
          setError('Error fetching pension');
        } finally {
          setLoading(false);
        }
      }
    };

    fetchPension();
  }, [user]);

  const handleOpenModal = () => {
    setModalIsOpen(true);
  };

  const handleCloseModal = () => {
    setModalIsOpen(false);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    if (updatedPension) {
      setUpdatedPension({
        ...updatedPension,
        [name]: value,
      });
    }
  };

  const handleUpdatePension = async () => {
    if (updatedPension) {
      const token = localStorage.getItem('token');
      try {
        await axios.post(`${process.env.REACT_APP_API_BASE_URL}/update-pension`, updatedPension, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
        toast.success('Pension updated successfully!');
        setPension(updatedPension);
        handleCloseModal();
      } catch (error) {
        console.error('Error updating pension:', error);
        toast.error('Failed to update pension');
      }
    }
  };

  if (!user) {
    return <p className="error">User is not logged in</p>;
  }

  if (loading) {
    return <p className="loading">Loading...</p>;
  }

  if (error) {
    return <p className="error">{error}</p>;
  }

  if (!pension) {
    return <p className="error">No pension found. Please create one.</p>;
  }

  return (
    <div className="pension-info">
      <h1>{pension.name}</h1>
      <p><strong>Address:</strong> {pension.address}</p>
      <p><strong>Phone:</strong> {pension.phone}</p>
      <p><strong>Email:</strong> {pension.email}</p>
      <p><strong>Max Capacity:</strong> {pension.max_capacity}</p>
      <p><strong>Current Occupancy:</strong> {pension.current_occupancy}</p>
      <p><strong>Rating:</strong> {pension.rating}</p>
      <p><strong>Description:</strong> {pension.description}</p>
      <p><strong>Size:</strong> {pension.size}</p>
      <p><strong>Hours:</strong> {pension.hours}</p>
      <div>
        <h2>Equipment</h2>
        <ul>
          {pension.equipment.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
      <div>
        <h2>Images</h2>
        {pension.image_urls.map((url, index) => (
          // eslint-disable-next-line jsx-a11y/img-redundant-alt
          <img key={index} src={url} alt={`Pension image ${index}`} />
        ))}
      </div>
      <button onClick={handleOpenModal}>Update Pension</button>
      <Modal isOpen={modalIsOpen} onRequestClose={handleCloseModal}>
        <h2>Update Pension</h2>
        <input
          type="text"
          name="name"
          value={updatedPension?.name || ''}
          onChange={handleChange}
          placeholder="Name"
        />
        <input
          type="text"
          name="address"
          value={updatedPension?.address || ''}
          onChange={handleChange}
          placeholder="Address"
        />
        <input
          type="text"
          name="phone"
          value={updatedPension?.phone || ''}
          onChange={handleChange}
          placeholder="Phone"
        />
        <input
          type="email"
          name="email"
          value={updatedPension?.email || ''}
          onChange={handleChange}
          placeholder="Email"
        />
        <input
          type="number"
          name="max_capacity"
          value={updatedPension?.max_capacity || ''}
          onChange={handleChange}
          placeholder="Max Capacity"
        />
        <textarea
          name="description"
          value={updatedPension?.description || ''}
          onChange={handleChange}
          placeholder="Description"
        />
        <textarea
          name="equipment"
          value={updatedPension?.equipment.join(', ') || ''}
          onChange={handleChange}
          placeholder="Equipment"
        />
        <input
          type="text"
          name="hours"
          value={updatedPension?.hours || ''}
          onChange={handleChange}
          placeholder="Hours"
        />
        <button onClick={handleUpdatePension}>Save</button>
        <button onClick={handleCloseModal}>Cancel</button>
      </Modal>
    </div>
  );
};

export default PensionInfo;
