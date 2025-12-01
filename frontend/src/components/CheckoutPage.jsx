import React, { useState } from 'react';
import { useStripe, useElements, PaymentElement } from '@stripe/react-stripe-js';
import './CheckoutPage.css';

function CheckoutPage() {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setLoading(true);
    setMessage('');

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/completion`,
      },
    });

    if (error) {
      setMessage(error.message);
      setLoading(false);
    }
  };

  return (
    <div className="checkout-container">
      {/* Header */}
      <header className="checkout-header">
        <div className="logo">ETHOS</div>
        <div className="help-section">
          <span className="help-text">CALL US FOR HELP</span>
          <a href="tel:4159150665" className="phone-number">(415) 915-0665</a>
        </div>
      </header>

      {/* Progress Steps */}
      <div className="progress-container">
        <div className="progress-step completed">
          <div className="step-circle">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M16.6 5L7.5 14.1L3.4 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="step-label">Beneficiaries</div>
        </div>
        
        <div className="progress-line completed"></div>
        
        <div className="progress-step completed">
          <div className="step-circle">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M16.6 5L7.5 14.1L3.4 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="step-label">Coverage</div>
        </div>
        
        <div className="progress-line"></div>
        
        <div className="progress-step active">
          <div className="step-circle">3</div>
          <div className="step-label">Secure Checkout</div>
        </div>
      </div>

      {/* Main Content */}
      <div className="checkout-content">
        <h1 className="main-heading">You're one step away from protecting Katy.</h1>
        <p className="sub-heading">Nice work, Brent! Just add payment and start your coverage.</p>

        {/* Payment Form */}
        <div className="payment-section">
          <div className="section-header">
            <h2>Secure checkout</h2>
            <div className="norton-badge">
              <svg width="113" height="59" viewBox="0 0 113 59" fill="none" xmlns="http://www.w3.org/2000/svg">
                {/* Badge Background */}
                <rect x="0.5" y="0.5" width="112" height="58" rx="29" fill="white" stroke="#E5E5E5"/>
                
                {/* Yellow Circle */}
                <circle cx="29" cy="29" r="13" fill="#FFC107"/>
                
                {/* Checkmark */}
                <path d="M26 29L28.5 31.5L33 27" stroke="#1A1A1A" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                
                {/* norton text */}
                <text x="46" y="25" fontFamily="Arial, sans-serif" fontSize="12" fontWeight="bold" fill="#1A1A1A">
                  norton
                </text>
                
                {/* SECURED text */}
                <text x="46" y="37" fontFamily="Arial, sans-serif" fontSize="10" fill="#666666" letterSpacing="1">
                  SECURED
                </text>
              </svg>
              <div className="norton-subtitle">
                <span style={{fontSize: '10px', color: '#999', marginTop: '2px'}}>powered by</span>
                <span style={{fontSize: '11px', color: '#666', fontWeight: '500', marginLeft: '3px'}}>Symantec</span>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="payment-form">
            <div className="payment-element-container">
              <PaymentElement 
                options={{
                  layout: {
                    type: 'accordion',
                    defaultCollapsed: true,
                    radios: true,
                    spacedAccordionItems: true
                  },
                  fields: {billingDetails: {name:"never"},
                    email: {required: "never"},
                    phone: {required: "never"},
                    address: {required: "never"},
                    paymentMethodOrder: ['us_bank_account', 'card', 'link']
                  }
                }}
              />
            </div>

            {/* Payment Summary */}
            <div className="payment-summary">
              <div className="summary-title">Payment Summary</div>
              <div className="summary-amounts">
                <div className="monthly-amount">$490.50/month</div>
                <div className="daily-amount">$17.72/day</div>
              </div>
            </div>

            {/* SSL Badge */}
            <div className="ssl-badge">
              <svg width="16" height="20" viewBox="0 0 16 20" fill="none">
                <path d="M14 8H13V6C13 3.24 10.76 1 8 1C5.24 1 3 3.24 3 6V8H2C0.9 8 0 8.9 0 10V18C0 19.1 0.9 20 2 20H14C15.1 20 16 19.1 16 18V10C16 8.9 15.1 8 14 8ZM8 15C6.9 15 6 14.1 6 13C6 11.9 6.9 11 8 11C9.1 11 10 11.9 10 13C10 14.1 9.1 15 8 15ZM11 8H5V6C5 4.34 6.34 3 8 3C9.66 3 11 4.34 11 6V8Z" fill="#00875A"/>
              </svg>
              <span>Certified SSL</span>
              <span className="security-text">SECURITY</span>
            </div>

            {/* Terms */}
            <div className="terms">
              By continuing, I confirm I've viewed my <a href="#" className="terms-link">application.</a>
            </div>

            {/* Submit Button */}
            <button 
              type="submit" 
              disabled={!stripe || loading} 
              className="submit-button"
            >
              {loading ? 'Processing...' : 'Start my coverage'}
            </button>

            {message && <div className="error-message">{message}</div>}
          </form>
        </div>
      </div>
    </div>
  );
}

export default CheckoutPage;

