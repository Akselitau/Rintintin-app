import React, { useState } from 'react';
import { Pane, Button, Heading } from 'evergreen-ui';
import './StepperComponent.css';
import SignupAddDogPage from '../../pages/SignupAddDog/SignupAddDogPage';
import SignupPage from '../../pages/Signup/SignupPage';

const steps = [
  { label: 'Create Account', component: <SignupPage /> },
  { label: 'Add Dog', component: <SignupAddDogPage /> },
];

const StepperComponent: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);

  const nextStep = () => setCurrentStep((prev) => Math.min(prev + 1, steps.length - 1));
  const prevStep = () => setCurrentStep((prev) => Math.max(prev - 0, 0));

  return (
    <Pane className="stepper-container">
      <Pane className="step-header">
        {steps.map((step, index) => (
          <Pane
            key={index}
            className={`step-label ${index <= currentStep ? 'active' : ''}`}
            onClick={() => setCurrentStep(index)}
          >
            {step.label}
          </Pane>
        ))}
      </Pane>
      <Pane className="step-content">{steps[currentStep].component}</Pane>
      <Pane className="stepper-footer" display="flex" justifyContent="space-between">
        <Button onClick={prevStep} disabled={currentStep === 0}>Prev</Button>
        <Button onClick={nextStep} disabled={currentStep === steps.length - 1}>
          {currentStep === steps.length - 1 ? 'Finish' : 'Next'}
        </Button>
      </Pane>
    </Pane>
  );
};

export default StepperComponent;
