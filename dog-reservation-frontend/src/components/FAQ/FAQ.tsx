// src/components/FAQ/FAQ.tsx
import React, { useState } from 'react';
import './FAQ.css';

interface FAQItem {
  question: string;
  answer: string;
}

const faqItems: FAQItem[] = [
  { question: "Will I get lifetime updates?", answer: "Yes, you will get lifetime updates for free." },
  { question: "Can I use the Landify for a client's product?", answer: "Yes, you can use it for a client's product." },
  { question: "Do you have a free trial of Landify?", answer: "Yes, we offer a free trial." },
  { question: "Who can use Landify?", answer: "Anyone can use Landify for their projects." }
];

const FAQ: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="faq-section">
      <h2 className="faq-title">Frequently Asked Questions</h2>
      <p className="faq-subtitle">If you have any further questions please contact us.</p>
      <div className="faq-list">
        {faqItems.map((item, index) => (
          <div
            key={index}
            className={`faq-item ${openIndex === index ? 'open' : ''}`}
            onClick={() => toggleFAQ(index)}
          >
            <div className="faq-question">
              {item.question}
              <span className="faq-toggle">{openIndex === index ? '−' : '+'}</span>
            </div>
            <div className="faq-answer">
              <p>{item.answer}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FAQ;
