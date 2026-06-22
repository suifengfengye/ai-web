import Link from 'next/link'
import React from 'react'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div>
            <Link href="/">Home</Link>
        </div>
        {children}
    </body>
    </html>
  )
}