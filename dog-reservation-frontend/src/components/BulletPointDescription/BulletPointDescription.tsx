import React from 'react';
import BulletPoint from '../BulletPoint/BulletPoint';
import './BulletPointDescription.css';

const BulletPointDescription: React.FC = () => {
  const bulletPoints = [
    {
      title: 'Découvre les professionnels autour de chez toi',
      description: 'Accède facilement aux pensions, éducateurs et toiletteurs près de chez toi.',
      iconUrl: 'path_to_icon1',
    },
    {
      title: 'Partage toutes les infos essentielles de ton toutou en 1 clic',
      description: 'Simplifie la vie des professionnels en partageant les détails importants de ton chien.',
      iconUrl: 'path_to_icon2',
    },
    {
      title: 'Planifie facilement les séjours',
      description: 'Organise et planifie les séjours de ton compagnon en toute simplicité.',
      iconUrl: 'path_to_icon3',
    },
  ];

  return (
    <div className="bullet-point-description">
      <h2 className="bullet-point-heading">C'est super simple !</h2>
      <p className="bullet-point-subheading">On est en contact avec les meilleurs professionnels du secteur</p>
      <div className="bullet-point-list">
        {bulletPoints.map((bullet, index) => (
          <BulletPoint key={index} title={bullet.title} description={bullet.description} iconUrl={bullet.iconUrl} />
        ))}
      </div>
    </div>
  );
};

export default BulletPointDescription;
