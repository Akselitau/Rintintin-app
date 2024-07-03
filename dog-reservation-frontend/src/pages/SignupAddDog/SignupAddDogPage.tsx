import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Pane,
  TextInputField,
  Button,
  Tablist,
  Tab,
  Paragraph,
} from 'evergreen-ui';
import './SignupAddDogPage.css';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useAuth } from '../../context/AuthContext';


const SignupAddDogPage: React.FC = () => {
  const [step, setStep] = useState(1);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [dogName, setDogName] = useState('');
  const [breed, setBreed] = useState('');
  const [age, setAge] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [passwordError, setPasswordError] = useState('');
  const [signupError, setSignupError] = useState('');

  const navigate = useNavigate();
  const { login, forceUpdate } = useAuth();
  const { user } = useAuth();

  const handleNext = async () => {
    if (step === 1) {
      if (password !== confirmPassword) {
        toast.error('Les mots de passe ne correspondent pas.');
        return;
      }
  
      try {
        const response = await axios.post('http://localhost:8000/create-user', {
          name: name,
          email: email,
          password: password,
        });
        localStorage.setItem('token', response.data.token);
        login(response.data.token);
        forceUpdate();
        toast.success('Compte créé avec succès !');
        setStep(2);
        setSelectedIndex(2);
      } catch (error: any) {
        console.error('Error signing up:', error);
        toast.error('Erreur lors de la création du compte : ' + (error.response?.data?.message || 'Erreur inconnue'));
      }
    } else if (step === 2) {
      const data = { name: dogName, breed: breed, age: age, user_id: user.user_id };
  
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
          toast.success('Chien ajouté avec succès !');
          navigate('/');
        } else {
          toast.error('Erreur lors de l\'ajout du chien');
          console.error('Failed to add dog');
        }
      } catch (error) {
        toast.error('Erreur lors de l\'ajout du chien : ' + 'Erreur inconnue');
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
    <Pane className="signup-add-dog-container">
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
            <TextInputField
              label="Race"
              placeholder="Race"
              value={breed}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setBreed(e.target.value)
              }
            />
            <TextInputField
              label="Âge"
              placeholder="Âge"
              value={age}
              type="number"
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setAge(e.target.value)
              }
            />
            <Button
              appearance="primary"
              onClick={handleNext}
              disabled={!dogName || !breed || !age}
            >
              Ajouter un chien
            </Button>
            <Button appearance="default" onClick={handleSkip} marginLeft={16}>
              Faire plus tard
            </Button>
          </Pane>
        )}
      </Pane>
    </Pane>
  );
};

export default SignupAddDogPage;
