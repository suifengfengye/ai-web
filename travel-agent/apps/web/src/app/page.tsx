'use client'
import { useEffect } from 'react'
import Link from 'next/link'
import { redirect } from 'next/navigation'

export default function HomePage({}: {}) {
    useEffect(() => {
        redirect('/chat')
    }, [])
    return (
        <div>
            <h1>Home Page</h1>
            <ul>
                <li>
                    <Link href="/dashboard">Dashboard</Link>
                </li>
            </ul>
        </div>
    )
}