import React, { useEffect, useState } from 'react';
import { useInView } from 'react-intersection-observer';
import './BulletPoint.css';

interface BulletPointProps {
  title: string;
  description: string;
  iconUrl: string;
}

const BulletPoint: React.FC<BulletPointProps> = ({ title, description, iconUrl }) => {
  const { ref, inView } = useInView({
    triggerOnce: false,
    threshold: 0.1,
  });
  const [isAnimated, setIsAnimated] = useState(false);

  useEffect(() => {
    if (inView) {
      setIsAnimated(true);
    } else {
      setIsAnimated(false);
    }
  }, [inView]);

  return (
    <div ref={ref} className={`bullet-point ${isAnimated ? 'animate' : ''}`}>
      <img src={iconUrl} alt={title} className="bullet-point-icon" />
      <h3 className="bullet-point-title">{title}</h3>
      <p className="bullet-point-description">{description}</p>
      <button className="bullet-point-button">Read More</button>
    </div>
  );
};

export default BulletPoint;
