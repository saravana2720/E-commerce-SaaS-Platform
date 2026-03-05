import { useRouter } from 'next/router';
import Layout from '../components/Layout';

export default function OrderSuccess() {
  const { query } = useRouter();
  return <Layout><h2>Order placed successfully</h2><p>Order ID: {query.orderId}</p></Layout>;
}
