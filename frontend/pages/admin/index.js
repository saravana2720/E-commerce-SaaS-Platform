import Link from 'next/link';
import Layout from '../../components/Layout';

export default function AdminHome() {
  return (
    <Layout>
      <h2>Admin Dashboard</h2>
      <ul>
        <li><Link href="/admin/products">Manage Products</Link></li>
        <li><Link href="/admin/orders">View Orders</Link></li>
        <li><Link href="/admin/analytics">Revenue Analytics</Link></li>
        <li><Link href="/admin/inventory">Inventory</Link></li>
      </ul>
    </Layout>
  );
}
