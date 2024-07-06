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
        <img src="https://media.licdn.com/dms/image/D4E03AQF9HfNi1Ehxyw/profile-displayphoto-shrink_400_400/0/1687605238823?e=2147483647&v=beta&t=a7XjFn6KvYPjv4EAVMA1qcA12X9NZSBk-cq5YvHZCsw" alt="Social Proof" />
      </div>
      <div ref={textRef} className={`social-proof-text ${textAnimated ? 'animate' : ''}`}>
        <h2>Ils sont géniaux !</h2>
        <p>
          J'ai trouvé des professionnels à l'écoute des besoins de mon chien, tout c'est passé via Rintintin et c'était super.
        </p>
      </div>
    </div>
  );
};

export default SocialProof;
