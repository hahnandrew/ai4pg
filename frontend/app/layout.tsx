import { Inter } from 'next/font/google';
import { ReactNode } from 'react';
import Navbar from './components/navbar/Navbar';
import './styles/tailwind.css';

const inter = Inter({ subsets: ['latin'] });

type CombinedLayoutProps = {
  children: ReactNode;
  showNavbar?: boolean;
};

const CombinedLayout = ({ children, showNavbar = true }: CombinedLayoutProps) => {
  return (
    <html lang="en">
      <body className={inter.className}>
        {showNavbar && <Navbar />}
        <div>{children}</div>
      </body>
    </html>
  );
};

export default CombinedLayout;
