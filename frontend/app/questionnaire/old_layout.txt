import type { Metadata } from 'next'
import { Inter } from 'next/font/google'



const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Document Review Demo - OfCounsel.ai',
  description: 'Edit / revise document',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div>
        
    <html lang="en">
        
      <body>{children}</body>
    </html>
    </div>
  )
}
