import React, { useState, useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';
import CheckoutPage from './components/CheckoutPage';
import CompletionPage from './components/CompletionPage';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function App() {
  const [stripePromise, setStripePromise] = useState(null);
  const [clientSecret, setClientSecret] = useState('');
  const [currentPage, setCurrentPage] = useState('checkout');

  useEffect(() => {
    // Fetch publishable key from backend
    fetch(`${API_URL}/config`)
      .then((res) => res.json())
      .then((data) => {
        setStripePromise(loadStripe(data.publishableKey));
      })
      .catch((error) => {
        console.error('Error fetching Stripe config:', error);
      });

    // Simple routing based on URL path
    const path = window.location.pathname;
    if (path.includes('completion')) {
      setCurrentPage('completion');
    }
  }, []);

  useEffect(() => {
    // Create PaymentIntent when component mounts
    if (currentPage === 'checkout') {
      fetch(`${API_URL}/create-payment-intent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: 490050, // $490.50 in cents
          currency: 'usd',
          customer_name: 'Katy',
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.clientSecret) {
            setClientSecret(data.clientSecret);
          } else {
            console.error('Error creating payment intent:', data.error);
          }
        })
        .catch((error) => {
          console.error('Error creating payment intent:', error);
        });
    }
  }, [currentPage]);

  const options = {
    clientSecret,
  };

  return (
    <div className="App">
      {currentPage === 'completion' ? (
        <CompletionPage />
      ) : (
        stripePromise && clientSecret && (
          <Elements stripe={stripePromise} options={options}>
            <CheckoutPage />
          </Elements>
        )
      )}
      {currentPage === 'checkout' && !clientSecret && (
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          minHeight: '100vh',
          fontSize: '18px',
          color: '#666'
        }}>
          Loading payment form...
        </div>
      )}
    </div>
  );
}

export default App;

