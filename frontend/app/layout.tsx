import { ReactNode } from 'react';
import Navbar from './components/navbar/Navbar';
import './styles/tailwind.css';
import type { AppProps } from 'next/app';
import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';

type LayoutProps = {
  children: ReactNode;
  showNavbar?: boolean;
};

const Layout = ({ children, showNavbar = true }: LayoutProps) => {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {showNavbar && <Navbar />}
          {children}
        </AuthProvider>
      </body>
    </html>
  );
};

export default Layout;

// function getLayout(Component) {
//   return Component.noNavbar ? (pageProps) => <>{pageProps.children}</> : Layout;
// }

// export default function App({ Component, pageProps }: AppProps) {
//   const LayoutComponent = getLayout(Component);

//   return (
//     <AuthProvider>
//       <LayoutComponent>
//         <Component {...pageProps} />
//       </LayoutComponent>
//     </AuthProvider>
//   );
// }


// import { Inter } from 'next/font/google';
// import { ReactNode } from 'react';
// import Navbar from './components/navbar/Navbar';
// import './styles/tailwind.css';

// const inter = Inter({ subsets: ['latin'] });

// type CombinedLayoutProps = {
//   children: ReactNode;
//   showNavbar?: boolean;
// };

// const CombinedLayout = ({ children, showNavbar = true }: CombinedLayoutProps) => {
//   return (
//     <html lang="en">
//       <body className={inter.className}>
//         {showNavbar && <Navbar />}
//         <div>{children}</div>
//       </body>
//     </html>
//   );
// };

// export default CombinedLayout;
