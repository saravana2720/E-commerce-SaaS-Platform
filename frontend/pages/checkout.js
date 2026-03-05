import { useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import api from '../services/api';

export default function Checkout() {
  const [address, setAddress] = useState('');
  const router = useRouter();

  const handleCheckout = async () => {
    const res = await api.post('/orders/checkout', { address: { line1: address, city: 'Bengaluru', pincode: '560001' } });
    router.push(`/order-success?orderId=${res.data.order_id}`);
  };

  return (
    <Layout>
      <h2>Checkout</h2>
      <input value={address} onChange={(e) => setAddress(e.target.value)} placeholder="Address" />
      <button onClick={handleCheckout}>Pay with Razorpay</button>
    </Layout>
  );
}
