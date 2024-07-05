// src/components/SocialProof/SocialProof.tsx
import React, { useEffect, useState } from 'react';
import { useInView } from 'react-intersection-observer';
import './SocialProof.css';

const SocialProof: React.FC = () => {
  const { ref: imageRef, inView: imageInView } = useInView({
    triggerOnce: false,
    threshold: 0.1,
  });
  
  const { ref: textRef, inView: textInView } = useInView({
    triggerOnce: false,
    threshold: 0.1,
  });

  const [imageAnimated, setImageAnimated] = useState(false);
  const [textAnimated, setTextAnimated] = useState(false);

  useEffect(() => {
    if (imageInView) {
      setImageAnimated(true);
    } else {
      setImageAnimated(false);
    }
  }, [imageInView]);

  useEffect(() => {
    if (textInView) {
      setTextAnimated(true);
    } else {
      setTextAnimated(false);
    }
  }, [textInView]);

  return (
    <div className="social-proof">
      <div ref={imageRef} className={`social-proof-image ${imageAnimated ? 'animate' : ''}`}>
        <img src="path/to/image.jpg" alt="Social Proof" />
      </div>
      <div ref={textRef} className={`social-proof-text ${textAnimated ? 'animate' : ''}`}>
        <h2>Our Story</h2>
        <p>
          We specialize in organizing professional training courses and we have been doing it in Poland since 1994. As an academy of business, we are going through the development cycle.
        </p>
      </div>
    </div>
  );
};

export default SocialProof;
