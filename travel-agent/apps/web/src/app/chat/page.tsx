"use client"
import React, { useState } from "react";
import { useChat } from '@ai-sdk/react'
import {
    RotateCwIcon,
    MessageCircleDashedIcon,
    PlusIcon,
    PaperclipIcon,
    ImageIcon,
    TelescopeIcon,
    GlobeIcon,
    ArrowUpIcon,
} from 'lucide-react'

import {
    MessageScroller,
    MessageScrollerButton,
    MessageScrollerContent,
    MessageScrollerItem,
    MessageScrollerProvider,
    MessageScrollerViewport,
} from '@/components/ui/message-scroller'
import {
  Message,
  MessageAvatar,
  MessageContent,
  MessageFooter,
} from "@/components/ui/message"
import {
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardAction,
    CardContent,
    CardFooter,
} from '@/components/ui/card'
import {
    Tooltip,
    TooltipProvider,
    TooltipTrigger,
    TooltipContent,
} from '@/components/ui/tooltip'
import {
    Button
} from '@/components/ui/button'
import {
    Empty,
    EmptyHeader,
    EmptyMedia,
    EmptyTitle,
    EmptyDescription,
} from '@/components/ui/empty'
import {
    InputGroup,
    InputGroupAddon,
    InputGroupButton,
} from '@/components/ui/input-group'
import {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu'
import {
    Textarea,
} from '@/components/ui/textarea'
import {
    Bubble,
    BubbleContent,
    BubbleGroup,
    BubbleReactions,
} from "@/components/ui/bubble"
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"

export default function ChatPage() {
    const [userText, setUserText] = useState<string>('')
    const { messages, sendMessage, setMessages, status, stop } = useChat()
    const isBusy = status === 'submitted' || status === 'streaming'

    return (
        <div style={{ padding: 24 }}>
            <MessageScrollerProvider autoScroll>
                <div className="relative flex flex-col gap-4">
                    <Card className="mx-auto w-full gap-0">
                        <CardHeader className="gap-1 border-b">
                            <CardTitle>旅游攻略对话</CardTitle>
                            <CardDescription>我今天能帮您什么忙？</CardDescription>
                            <CardAction>
                                <TooltipProvider>
                                    <Tooltip>
                                        <TooltipTrigger asChild>
                                            <Button variant="outline" size="icon" aria-label="Reset conversation"
                                                onClick={() => {
                                                    if (isBusy) {
                                                        stop()
                                                    }
                                                    setMessages([])
                                                    setUserText('')
                                                }}
                                                disabled={messages.length === 0 && userText.trim().length === 0}>
                                                <RotateCwIcon />
                                            </Button>
                                        </TooltipTrigger>
                                        <TooltipContent>
                                            <p>Reset</p>
                                        </TooltipContent>
                                    </Tooltip>
                                </TooltipProvider>
                            </CardAction>
                        </CardHeader>
                        <CardContent className="flex-1 overflow-hidden p-0 pt-4 pb-4">
                            {
                                messages?.length <= 0 ? (
                                    <Empty className="h-full">
                                        <EmptyHeader>
                                            <EmptyMedia variant="icon">
                                                <MessageCircleDashedIcon />
                                            </EmptyMedia>
                                            <EmptyTitle>您好!</EmptyTitle>
                                            <EmptyDescription>
                                                我们今天来做什么呢？点击发送开始新的对话
                                            </EmptyDescription>
                                        </EmptyHeader>
                                    </Empty>
                                ) : (
                                    <MessageScroller>
                                        <MessageScrollerViewport>
                                            <MessageScrollerContent>
                                                {
                                                    messages.map((messageItem, index) => {
                                                        const isUser = messageItem.role === 'user'
                                                        const isLastMessage = index === messages.length - 1
                                                        return (
                                                            <MessageScrollerItem
                                                                key={messageItem.id}
                                                                messageId={messageItem.id}
                                                                scrollAnchor={isLastMessage}
                                                            >
                                                                <Message align={isUser ? 'end' : 'start'}>
                                                                    <MessageAvatar>
                                                                        <Avatar>
                                                                            <AvatarImage src={isUser? "/avatars/user.png": "/avatars/robot.png"} className="p-[6px]" alt="@robot" />
                                                                            <AvatarFallback>U</AvatarFallback>
                                                                        </Avatar>
                                                                    </MessageAvatar>
                                                                    {/* 
                                                                        {
                                                                            "id":"xxx",
                                                                            "role": "user",
                                                                            "parts": [
                                                                                {
                                                                                    "type": "text",
                                                                                    "text": "xxx"
                                                                                }
                                                                            ]
                                                                        }
                                                                    */}
                                                                    <MessageContent>
                                                                        <Bubble variant={isUser ? 'default' : 'muted'}>
                                                                            <BubbleContent>
                                                                                {(messageItem?.parts || []).map((partItem) => {
                                                                                    if (partItem?.type === 'text') {
                                                                                        return (
                                                                                            <span>
                                                                                                {partItem?.text}
                                                                                            </span>
                                                                                        )
                                                                                    }
                                                                                    return ''
                                                                                })}
                                                                            </BubbleContent>
                                                                        </Bubble>
                                                                    </MessageContent>
                                                                </Message>
                                                            </MessageScrollerItem>
                                                        )
                                                    })
                                                }
                                            </MessageScrollerContent>
                                        </MessageScrollerViewport>
                                        <MessageScrollerButton direction="end" />
                                    </MessageScroller>
                                )
                            }

                        </CardContent>
                        <CardFooter className="flex-col gap-2">
                            <form
                                onSubmit={(e) => {
                                    // e.preventDefault()
                                    // if (!nextMessage || isBusy) {
                                    // return
                                    // }
                                    // void sendMessage(nextMessage)
                                }}
                                className="w-full"
                            >
                                <InputGroup>
                                    <div className="h-14 w-full px-3 py-2.5">
                                        <Textarea 
                                        className="border-none rounded-none focus-visible:ring-0" 
                                        placeholder="请输入您的问题"
                                        style={{ maxHeight: 50 }} 
                                        value={userText}
                                        onChange={(e) => {
                                            setUserText(e?.target?.value)
                                        }}/>
                                        {/* {nextMessage ? (
                                    getMessageText(nextMessage)
                                    ) : (
                                    <span className="text-muted-foreground">
                                        No messages queued. Reset the conversation.
                                    </span>
                                    )} */}
                                    </div>
                                    <InputGroupAddon align="block-end" className="pt-1">
                                        {/* <DropdownMenu>
                                            <DropdownMenuTrigger asChild>
                                                <InputGroupButton
                                                    aria-label="Add files"
                                                    type="button"
                                                    size="icon-sm"
                                                    variant="outline"
                                                >
                                                    <PlusIcon />
                                                </InputGroupButton>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent
                                                align="start"
                                                side="top"
                                                className="w-44"
                                            >
                                                <DropdownMenuItem>
                                                    <PaperclipIcon />
                                                    Add Photos & Files
                                                </DropdownMenuItem>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuItem>
                                                    <ImageIcon />
                                                    Create Image
                                                </DropdownMenuItem>
                                                <DropdownMenuItem>
                                                    <TelescopeIcon />
                                                    Deep Research
                                                </DropdownMenuItem>
                                                <DropdownMenuItem>
                                                    <GlobeIcon />
                                                    Web Search
                                                </DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu> */}
                                        <InputGroupButton
                                            // type="submit"
                                            variant="default"
                                            size="icon-sm"
                                            disabled={isBusy}
                                            className="ml-auto"
                                            onClick={() => {
                                                sendMessage({ text: userText })
                                                setUserText('')
                                            }}
                                        >
                                            <ArrowUpIcon />
                                            <span className="sr-only">Send</span>
                                        </InputGroupButton>
                                    </InputGroupAddon>
                                </InputGroup>
                            </form>
                        </CardFooter>
                    </Card>
                </div>
            </MessageScrollerProvider>
        </div>
    )
}
