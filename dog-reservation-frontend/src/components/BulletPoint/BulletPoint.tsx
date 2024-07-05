// src/components/BulletPoint/BulletPoint.tsx
import React, { useEffect, useState } from 'react';
import { useInView } from 'react-intersection-observer';
import './BulletPoint.css';

interface BulletPointProps {
  title: string;
  description: string;
}

const BulletPoint: React.FC<BulletPointProps> = ({ title, description }) => {
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
      <h3 className="bullet-point-title">{title}</h3>
      <p className="bullet-point-description">{description}</p>
    </div>
  );
};

export default BulletPoint;
