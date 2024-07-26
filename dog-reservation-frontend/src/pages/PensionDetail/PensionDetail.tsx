import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import './PensionDetail.css';
import AddDogModal from '../../modals/AddDogModal';
import { toast } from 'react-toastify';

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
  hours: string;
  night_price: number;
  staff: { first_name: string; role: string; image_url: string }[];
  reviews: { name: string; date: string | null; rating: number; comment: string }[];
  status: string; // Ajout du champ status
}

interface Dog {
  dog_id: number;
  name: string;
  breed: string;
  profile_photo_url: string;
}

const PensionDetail: React.FC = () => {
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();
  const [pension, setPension] = useState<Pension | null>(null);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState<[Date, Date] | null>(null);
  const [numDogs] = useState(1); // Remove setNumDogs if not used
  const [fees] = useState(10);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [dogs, setDogs] = useState<Dog[]>([]);
  const [selectedDog, setSelectedDog] = useState<string | number>('');
  const [user, setUser] = useState<{ name: string; token: string } | null>(null);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [modalIsOpen, setModalIsOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
      axios.get(`${process.env.REACT_APP_API_BASE_URL}/get-profile`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(response => {
        setUser(response.data);
        fetchDogs(response.data.user_id, token);
      }).catch(error => {
        console.error('Error fetching user profile:', error);
        setIsLoggedIn(false);
      });
    }

    if (id) {
      axios.get(`${process.env.REACT_APP_API_BASE_URL}/get-pension/${id}`)
        .then(response => {
          const data = response.data;
          const staff = data.staff.map((member: any) => ({
            first_name: member.first_name,
            role: member.role,
            image_url: member.image_url
          }));
          setPension({ ...data, staff });
          setLoading(false);
        })
        .catch(error => {
          console.error('Error fetching pension:', error);
          setLoading(false);
        });
    }
  }, [id]);

  const fetchDogs = (user_id: number, token: string) => {
    axios.get(`${process.env.REACT_APP_API_BASE_URL}/get-dogs/${user_id}`, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(response => {
      setDogs(response.data.dogs);
    }).catch(error => {
      console.error('Error fetching dogs:', error);
    });
  };

  const handleDateChange = (value: Date | Date[] | null) => {
    if (Array.isArray(value)) {
      setDateRange(value.length === 2 ? (value as [Date, Date]) : null);
    } else {
      setDateRange(value ? [value, value] : null);
    }
  };

  const handleBackButtonClick = () => {
    navigate(-1);
  };

  const formatDate = (date: Date): string => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const handleReservation = () => {
    if (isLoggedIn && dateRange && selectedDog) {
      const checkIn = formatDate(dateRange[0] as Date);
      const checkOut = formatDate(dateRange[1] ? dateRange[1] : dateRange[0]);

      const reservationData = {
        pension_id: id,
        check_in: checkIn,
        check_out: checkOut,
        dog_id: selectedDog
      };

      console.log("Reservation Data:", reservationData); // Pour vérifier les données

      axios.post(`${process.env.REACT_APP_API_BASE_URL}/make-reservation`, reservationData, {
        headers: { Authorization: `Bearer ${user?.token}` }
      }).then(response => {
        toast.success('Réservation réussie !');
      }).catch(error => {
        toast.error('Échec de la réservation : ' + error.response.data.message);
      });
    } else {
      alert('Please select the dates and dog');
    }
  };

  const nextImage = () => {
    if (pension && pension.image_urls.length > 1) {
      setCurrentImageIndex((currentImageIndex + 1) % pension.image_urls.length);
    }
  };

  const prevImage = () => {
    if (pension && pension.image_urls.length > 1) {
      setCurrentImageIndex((currentImageIndex - 1 + pension.image_urls.length) % pension.image_urls.length);
    }
  };

  const handleDogAdded = (newDog: Dog) => {
    setDogs(prevDogs => [...prevDogs, newDog]);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!pension) {
    return <div>Pension not found</div>;
  }

  return (
    <div className="pension-detail">
      <div className="pension-detail-main">
        <div className="pension-detail-content">
          <button className="carousel-button" onClick={handleBackButtonClick}>⬅</button>
          <div className="carousel">
            {pension.image_urls.length > 1 && (
              <button className="carousel-nav-button left" onClick={prevImage}>⬅</button>
            )}
            <img src={pension.image_urls[currentImageIndex]} alt={pension.name} className="carousel-image" />
            {pension.image_urls.length > 1 && (
              <button className="carousel-nav-button right" onClick={nextImage}>➡</button>
            )}
          </div>
          <div className="pension-about">
            <p>{pension.description}</p>
          </div>
          <div className="pension-info">
            <div className="pension-equipment">
              <h2>🏠 Équipement</h2>
              <ul>
                {pension.equipment && pension.equipment.map((item: string, index: number) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="pension-size">
              <h2>🐶 Taille de la pension</h2>
              <p>{pension.max_capacity}</p>
            </div>
            <div className="pension-hours">
              <h2>⏰ Horaires</h2>
              <p>{pension.hours}</p>
            </div>
          </div>
  
          <div className="pension-team">
            <h2>L'équipe</h2>
            <div className="team-members">
              {pension.staff && pension.staff.map((member: { first_name: string; role: string; image_url: string }, index: number) => (
                <div key={index} className="team-member">
                  <img src={member.image_url} alt={member.first_name} />
                  <p><strong>{member.first_name}</strong></p>
                  <p>{member.role}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="pension-reviews">
            <h2>Ce que vous en pensez</h2>
            <div className="reviews">
              {pension.reviews && pension.reviews.map((review: { name: string; date: string | null; rating: number; comment: string }, index: number) => (
                <div key={index} className="review">
                  <p>{review.name}</p>
                  <p>{review.date}</p>
                  <p>{'⭐'.repeat(review.rating)}</p>
                  <p>{review.comment}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
        {pension.status === 'Validated' ? (
          <div className="reservation-section">
            <Calendar
              value={dateRange as [Date, Date]}
              onChange={handleDateChange as any}
              selectRange={true}
            />
            <div className="reservation-details">
              <div className="number-of-dogs">
                <label>Nombre de chiens:</label>
                <input
                  type="number"
                  min="1"
                  value={numDogs}
                  readOnly
                />
              </div>
              <div className="price-details">
                <p>Price: {pension.night_price * numDogs}$ / night</p>
                <p>Fees: {fees}$</p>
                <p>Total: {(pension.night_price * numDogs + fees)}$</p>
              </div>
              {isLoggedIn ? (
                <div className="dog-selection">
                  <label>Choisissez votre chien:</label>
                  <select value={selectedDog} onChange={(e) => setSelectedDog(e.target.value)}>
                    <option value="">Sélectionner un chien</option>
                    {dogs.map(dog => (
                      <option key={dog.dog_id} value={dog.dog_id}>{dog.name}</option>
                    ))}
                  </select>
                  <button className="add-dog-button" onClick={() => setModalIsOpen(true)}>Ajouter un chien</button>
                </div>
              ) : (
                <button className="login-button" onClick={() => navigate('/login')}>Se connecter</button>
              )}
              <button className="reservation-button" onClick={handleReservation} disabled={!dateRange || !selectedDog}>
                Demander à réserver
              </button>
            </div>
          </div>
        ) : (
          <div className="referenced-section">
            <h2>Cette pension est à vous ?</h2>
            <p>Contactez-nous pour pouvoir gérer les réservations facilement !</p>
            <button className="contact-button" onClick={() => navigate('/contact')}>Nous contacter</button>
          </div>
        )}
      </div>
      <AddDogModal 
        isOpen={modalIsOpen} 
        onRequestClose={() => setModalIsOpen(false)} 
        onDogAdded={handleDogAdded} 
      />
    </div>
  );
};

export default PensionDetail;

