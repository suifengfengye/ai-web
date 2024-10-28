
export const fetchAI = async (params: any) => {
  const response: any = await fetch(`/ai_api/ai_docs/generate`, {
    method: 'POST',
    headers: new Headers({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify({
      ...params,
    }),
  })
  return response.body.getReader()
}
