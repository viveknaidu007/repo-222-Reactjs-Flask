import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the token exists
    const token = localStorage.getItem('token');
    if (!token) {
      // If no token, redirect to login page
      navigate('/login');
    } else {
      // Display the welcome message if token exists
      setMessage('Welcome Client');
    }
  }, [navigate]);

  return (
    <div>
      <h2>{message}</h2>
      {/* You can add more content to your dashboard here */}
    </div>
  );
}

export default Dashboard;
