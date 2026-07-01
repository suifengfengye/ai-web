import { createDeepSeek } from '@ai-sdk/deepseek'
import { NextRequest, NextResponse } from 'next/server'
import { createUIMessageStreamResponse, streamText, toUIMessageStream } from 'ai'

import { API_KEY } from './key'

const deepseek = createDeepSeek({
  apiKey: API_KEY,
})

export async function GET() {
  return NextResponse.json({
    ok: true,
    message: 'chat route is available, use POST /api/chat to send messages',
  })
}

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => ({}))
  console.log(`@@@body`, body)
  const messages = Array.isArray(body?.messages) && body.messages.length > 0
    ? body.messages
    : [
        {
          role: 'user',
          content: '请问你是 deepseek 吗？你是不是世界上最强的模型？',
        },
      ]

  const result = streamText({
    model: deepseek('deepseek-chat'),
    messages,
    system: '现在你是一个博学多才的教授，名字叫做花花。',
  })

  return createUIMessageStreamResponse({
    stream: toUIMessageStream({
      stream: result.stream,
    }),
  })
}
