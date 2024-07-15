import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Pane, TextInputField, Button, Tablist, Tab, Paragraph, SelectMenu } from 'evergreen-ui';
import './SignupAddDogPage.css';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useAuth } from '../../context/AuthContext';

interface Breed {
  breed_id: number;
  name: string;
}

const SignupAddDogPage: React.FC = () => {
  const [step, setStep] = useState(1);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [dogName, setDogName] = useState('');
  const [breed, setBreed] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [passwordError, setPasswordError] = useState('');
  const [signupError] = useState('');
  const [breeds, setBreeds] = useState<{ label: string, value: string }[]>([]);

  const navigate = useNavigate();
  const { login, user } = useAuth();

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
          setBreeds(data.breeds.map((breed: Breed) => ({ label: breed.name, value: breed.name })));
        } else {
          console.error('Failed to fetch dog breeds');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchBreeds();
  }, []);

  const handleNext = async () => {
    if (step === 1) {
      if (password !== confirmPassword) {
        toast.error('Les mots de passe ne correspondent pas.');
        return;
      }
  
      try {
        const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/create-user`, {
          name: name,
          email: email,
          password: password,
        });
        localStorage.setItem('token', response.data.token);
        login(response.data.token);
        toast.success('Compte créé avec succès !');
        setStep(2);
        setSelectedIndex(2);
      } catch (error: any) {
        console.error('Error signing up:', error);
        toast.error('Erreur lors de la création du compte : ' + (error.response?.data?.message || 'Erreur inconnue'));
      }
    } else if (step === 2) {
        const data = {
          name: dogName,
          breed: breed,
          user_id: user.user_id,
          birthdate: birthDate || null,
        };
    
        if (birthDate) {  // Ajouter birthdate seulement si elle est fournie
          data.birthdate = birthDate;
        }
    
        try {
          const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/create-dog-profile`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
            body: JSON.stringify(data),
          });
    
          if (response.ok) {
            toast.success('Chien ajouté avec succès !');
            navigate('/');
          } else {
            toast.error('Erreur lors de l\'ajout du chien');
            console.error('Failed to add dog');
          }
        } catch (error) {
          toast.error('Erreur lors de l\'ajout du chien : Erreur inconnue');
          console.error('Error adding dog:', error);
        }
      }
    };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
    if (confirmPassword && e.target.value !== confirmPassword) {
      setPasswordError('Les mots de passe ne correspondent pas');
    } else {
      setPasswordError('');
    }
  };

  const handleConfirmPasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmPassword(e.target.value);
    if (password && e.target.value !== password) {
      setPasswordError('Les mots de passe ne correspondent pas');
    } else {
      setPasswordError('');
    }
  };

  const handleSkip = () => {
    navigate('/');
  };

  return (
    <div className="signup-container">
      <div className="signup-image"></div>
      <div className="signup-form-container">
        <Tablist className="tablist">
          <Tab
            key="account"
            isSelected={selectedIndex === 0}
            onSelect={() => setSelectedIndex(0)}
            disabled={selectedIndex !== 0}
          >
            Créer un compte
          </Tab>
          <Tab
            key="dog"
            isSelected={selectedIndex === 2}
            onSelect={() => setSelectedIndex(2)}
            disabled={selectedIndex !== 2}
          >
            Ajouter un chien
          </Tab>
        </Tablist>
        <Pane className="form-container">
          {selectedIndex === 0 && (
            <Pane className="form-section">
              <TextInputField
                label="Nom"
                placeholder="Nom"
                value={name}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setName(e.target.value)
                }
              />
              <TextInputField
                label="Email"
                placeholder="Email"
                value={email}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setEmail(e.target.value)
                }
              />
              <TextInputField
                label="Mot de passe"
                placeholder="Mot de passe"
                type="password"
                value={password}
                onChange={handlePasswordChange}
              />
              <TextInputField
                label="Confirmer le mot de passe"
                placeholder="Confirmer le mot de passe"
                type="password"
                value={confirmPassword}
                onChange={handleConfirmPasswordChange}
              />
              {passwordError && <Paragraph color="danger">{passwordError}</Paragraph>}
              {signupError && <Paragraph color="danger">{signupError}</Paragraph>}
              <Button
                appearance="primary"
                onClick={handleNext}
                disabled={!name || !email || !password || !confirmPassword || password !== confirmPassword}
              >
                Créer un compte
              </Button>
              <Paragraph>J'ai déjà un compte</Paragraph>
              <Button onClick={() => navigate('/login')}>Connexion</Button>
            </Pane>
          )}
          {selectedIndex === 2 && (
            <Pane className="form-section">
              <TextInputField
                label="Nom du chien"
                placeholder="Nom du chien"
                value={dogName}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setDogName(e.target.value)
                }
              />
              <SelectMenu
                options={breeds}
                selected={breed}
                hasFilter={false}
                onSelect={(item: any) => setBreed(item.value)}
              >
                <Button>{breed || 'Sélectionner une race'}</Button>
              </SelectMenu>
              <TextInputField
                label="Date de naissance"
                placeholder="Date de naissance"
                type="date"
                value={birthDate}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setBirthDate(e.target.value)
                }
              />
              <Button
                appearance="primary"
                onClick={handleNext}
                disabled={!dogName || !breed || !birthDate}
              >
                Ajouter un chien
              </Button>
              <Button appearance="default" onClick={handleSkip} marginLeft={16}>
                Faire plus tard
              </Button>
            </Pane>
          )}
        </Pane>
      </div>
    </div>
  );
};

export default SignupAddDogPage;
