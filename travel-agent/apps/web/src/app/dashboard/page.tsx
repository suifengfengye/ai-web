async function wait(ms: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms)
  })
}

export default async function DashboardPage() {
  // Simulate a slow server render so `dashboard/loading.tsx` can appear.
  await wait(3000)

  return <div>Dashboard Page</div>
}
