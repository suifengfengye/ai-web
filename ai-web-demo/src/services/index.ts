
export const fetchAI = async (params: any) => {
  const response: any = await fetch(`http://127.0.0.1:8000/ai_polish/conversationId`, {
    method: 'POST',
    headers: new Headers({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify({
      ...params,
      // engine: 'llama2',
    }),
  })
  return response.body.getReader()
}
