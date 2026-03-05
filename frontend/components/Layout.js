import Link from 'next/link';

export default function Layout({ children }) {
  return (
    <div style={{ fontFamily: 'Arial', maxWidth: 1000, margin: '0 auto', padding: 16 }}>
      <nav style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
        <Link href="/">Home</Link>
        <Link href="/products">Products</Link>
        <Link href="/cart">Cart</Link>
        <Link href="/login">Login</Link>
        <Link href="/signup">Signup</Link>
        <Link href="/admin">Admin</Link>
      </nav>
      {children}
    </div>
  );
}
