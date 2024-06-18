import React, { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import './ProfilePage.css';

interface UserProfile {
  user_id: number;
  name: string;
  email: string;
  profile_photo_url?: string;
}

const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);

  useEffect(() => {
    if (user) {
      fetchProfile();
    }
  }, [user]);

  const fetchProfile = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/get-profile`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          setProfile(data);
        } else {
          console.error('Failed to fetch profile:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    }
  };

  return (
    <div className="profile-container">
      <h2>Mon Profil</h2>
      {profile ? (
        <div className="profile-details">
          <img src={profile.profile_photo_url || 'default-profile.png'} alt={profile.name} className="profile-photo" />
          <div className="profile-info">
            <h3>{profile.name}</h3>
            <p>Email: {profile.email}</p>
          </div>
        </div>
      ) : (
        <p>Veuillez vous connecter pour voir vos informations de profil.</p>
      )}
    </div>
  );
};

export default ProfilePage;
