import { useEffect } from 'react';
import Layout from '../components/Layout';
import { useCartContext } from '../context/CartContext';
import api from '../services/api';

export default function Cart() {
  const { cart, setCart } = useCartContext();

  useEffect(() => {
    api.get('/cart').then((res) => setCart(res.data));
  }, [setCart]);

  return (
    <Layout>
      <h2>Cart</h2>
      {cart.items.map((i) => (
        <div key={i.product_id}>{i.name} x {i.quantity}</div>
      ))}
      <p>Total: ₹{(cart.total_paise / 100).toFixed(2)}</p>
    </Layout>
  );
}
