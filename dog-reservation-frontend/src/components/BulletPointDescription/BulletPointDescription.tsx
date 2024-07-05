// src/components/BulletPointDescription/BulletPointDescription.tsx
import React from 'react';
import BulletPoint from '../BulletPoint/BulletPoint';
import './BulletPointDescription.css';

const BulletPointDescription: React.FC = () => {
  const bulletPoints = [
    {
      title: 'Découvre les professionnels autour de chez toi',
      description: 'Accède facilement aux pensions, éducateurs et toiletteurs près de chez toi.',
    },
    {
      title: 'Partage toutes les infos essentielles de ton toutou en 1 clic',
      description: 'Simplifie la vie des professionnels en partageant les détails importants de ton chien.',
    },
    {
      title: 'Planifie facilement les séjours',
      description: 'Organise et planifie les séjours de ton compagnon en toute simplicité.',
    },
  ];

  return (
    <div className="bullet-point-description">
      <h2 className="bullet-point-heading">The process we follow</h2>
      <p className="bullet-point-subheading">As a academy of business, we are going through the development cycle.</p>
      <div className="bullet-point-list">
        {bulletPoints.map((bullet, index) => (
          <BulletPoint key={index} title={bullet.title} description={bullet.description} />
        ))}
      </div>
    </div>
  );
};

export default BulletPointDescription;
