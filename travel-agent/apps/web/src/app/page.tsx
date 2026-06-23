'use client'
import React, { useEffect, useState } from "react"
import Link from 'next/link'

export default function HomePage({}: {}) {
    const [count, setCount] = useState(0)
    // useEffect(() => {
    //     (new Promise((resolve) => {
    //         setTimeout(() => {
    //             resolve({ success: true })
    //         }, 3000)
    //     })).then(() => {
    //         setCount(1)
    //     })
    // }, [])

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