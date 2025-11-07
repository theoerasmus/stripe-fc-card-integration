import React, { useState, useEffect } from 'react';
import './CompletionPage.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function CompletionPage() {
  const [status, setStatus] = useState('loading');
  const [paymentIntent, setPaymentIntent] = useState(null);
  const [rawAccountData, setRawAccountData] = useState(null);

  useEffect(() => {
    const clientSecret = new URLSearchParams(window.location.search).get(
      'payment_intent_client_secret'
    );

    if (!clientSecret) {
      setStatus('error');
      return;
    }

    // Extract payment intent ID from client secret
    const paymentIntentId = clientSecret.split('_secret_')[0];

    // Fetch payment intent details
    fetch(`${API_URL}/payment-intent?id=${paymentIntentId}`)
      .then((res) => res.json())
      .then((data) => {
        setPaymentIntent(data);
        setStatus(data.status);
        
        // If there's a payment method, try to get raw account details
        // Works for both 'succeeded' and 'processing' statuses
        if (data.payment_method) {
          fetch(`${API_URL}/raw-account?payment_method=${data.payment_method}`)
            .then((res) => res.json())
            .then((accountData) => {
              setRawAccountData(accountData);
            })
            .catch((error) => {
              console.log('Raw account data not available:', error);
            });
        }
      })
      .catch((error) => {
        console.error('Error fetching payment intent:', error);
        setStatus('error');
      });
  }, []);

  return (
    <div className="completion-container">
      <div className="completion-content">
        {status === 'loading' && (
          <div className="status-card">
            <div className="loading-spinner"></div>
            <h2>Processing your payment...</h2>
          </div>
        )}

        {status === 'succeeded' && (
          <div className="status-card success">
            <div className="success-icon">
              <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                <circle cx="32" cy="32" r="32" fill="#00875A"/>
                <path d="M44 24L28 40L20 32" stroke="white" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <h1>Payment Successful!</h1>
            <p>Your coverage has been activated.</p>
            <div className="payment-details">
              <div className="detail-row">
                <span className="detail-label">Amount:</span>
                <span className="detail-value">
                  ${paymentIntent?.amount ? (paymentIntent.amount / 100).toFixed(2) : '0.00'}
                </span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Status:</span>
                <span className="detail-value success-text">{status}</span>
              </div>
            </div>
            
            {/* Raw Account Details Section */}
            {rawAccountData && rawAccountData.us_bank_account && (
              <div className="account-details">
                <h3 style={{ fontSize: '18px', marginBottom: '15px', color: '#1a1a1a' }}>
                  Bank Account Details
                </h3>
                <div className="payment-details">
                  <div className="detail-row">
                    <span className="detail-label">Bank Name:</span>
                    <span className="detail-value">{rawAccountData.us_bank_account.bank_name}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Account Type:</span>
                    <span className="detail-value">{rawAccountData.us_bank_account.account_type}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Routing Number:</span>
                    <span className="detail-value">{rawAccountData.us_bank_account.routing_number}</span>
                  </div>
                  {rawAccountData.us_bank_account.account_number ? (
                    <div className="detail-row">
                      <span className="detail-label">Account Number:</span>
                      <span className="detail-value" style={{ fontFamily: 'monospace' }}>
                        {rawAccountData.us_bank_account.account_number}
                      </span>
                    </div>
                  ) : (
                    <div className="detail-row">
                      <span className="detail-label">Account:</span>
                      <span className="detail-value">****{rawAccountData.us_bank_account.last4}</span>
                    </div>
                  )}
                </div>
                {rawAccountData.note && (
                  <div style={{ 
                    fontSize: '12px', 
                    color: '#666', 
                    marginTop: '10px',
                    padding: '10px',
                    backgroundColor: '#f5f5f5',
                    borderRadius: '4px'
                  }}>
                    ℹ️ {rawAccountData.note}
                  </div>
                )}
              </div>
            )}
            
            <button 
              className="action-button" 
              onClick={() => window.location.href = '/'}
            >
              Back to Home
            </button>
          </div>
        )}

        {status === 'processing' && (
          <div className="status-card">
            <div className="loading-spinner"></div>
            <h2>Payment Processing</h2>
            <p>Your payment is being processed. Please wait...</p>
            
            <div className="payment-details">
              <div className="detail-row">
                <span className="detail-label">Amount:</span>
                <span className="detail-value">
                  ${paymentIntent?.amount ? (paymentIntent.amount / 100).toFixed(2) : '0.00'}
                </span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Status:</span>
                <span className="detail-value">{status}</span>
              </div>
            </div>

            {/* Raw Account Details Section */}
            {rawAccountData && rawAccountData.us_bank_account && (
              <div className="account-details">
                <h3 style={{ fontSize: '18px', marginBottom: '15px', color: '#1a1a1a' }}>
                  Bank Account Details
                </h3>
                <div className="payment-details">
                  <div className="detail-row">
                    <span className="detail-label">Bank Name:</span>
                    <span className="detail-value">{rawAccountData.us_bank_account.bank_name}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Account Type:</span>
                    <span className="detail-value">{rawAccountData.us_bank_account.account_type}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Routing Number:</span>
                    <span className="detail-value">{rawAccountData.us_bank_account.routing_number}</span>
                  </div>
                  {rawAccountData.us_bank_account.account_number ? (
                    <div className="detail-row">
                      <span className="detail-label">Account Number:</span>
                      <span className="detail-value" style={{ fontFamily: 'monospace' }}>
                        {rawAccountData.us_bank_account.account_number}
                      </span>
                    </div>
                  ) : (
                    <div className="detail-row">
                      <span className="detail-label">Account:</span>
                      <span className="detail-value">****{rawAccountData.us_bank_account.last4}</span>
                    </div>
                  )}
                </div>
                {rawAccountData.note && (
                  <div style={{ 
                    fontSize: '12px', 
                    color: '#666', 
                    marginTop: '10px',
                    padding: '10px',
                    backgroundColor: '#f5f5f5',
                    borderRadius: '4px'
                  }}>
                    ℹ️ {rawAccountData.note}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {status === 'requires_payment_method' && (
          <div className="status-card error">
            <div className="error-icon">❌</div>
            <h2>Payment Failed</h2>
            <p>Your payment method was declined. Please try another payment method.</p>
            <button 
              className="action-button" 
              onClick={() => window.location.href = '/'}
            >
              Try Again
            </button>
          </div>
        )}

        {status === 'error' && (
          <div className="status-card error">
            <div className="error-icon">❌</div>
            <h2>Something went wrong</h2>
            <p>We couldn't process your payment. Please try again.</p>
            <button 
              className="action-button" 
              onClick={() => window.location.href = '/'}
            >
              Back to Checkout
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default CompletionPage;

