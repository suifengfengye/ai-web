"use client"
import React from "react";
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
    MessageScrollerProvider
} from '@/components/ui/message-scroller'
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

export default function ChatPage() {
    const isBusy = false
    React.useEffect(() => {
        fetch('/api/chat', {
            method: "POST",
        }).then((result) => {
            console.log(`@@@result`, result)
        })
    }, [])
    return (
        <div style={{ padding: 24 }}>
            <MessageScrollerProvider>
                <div className="relative flex flex-col gap-4">
                    <Card className="mx-auto h-140 w-full gap-0">
                        <CardHeader className="gap-1 border-b">
                            <CardTitle>新对话</CardTitle>
                            <CardDescription>我今天能帮您什么忙？</CardDescription>
                            <CardAction>
                                <TooltipProvider>
                                    <Tooltip>
                                        <TooltipTrigger asChild>
                                            <Button variant="outline" size="icon" aria-label="Reset conversation" 
                                                onClick={() => { 
                                                // todo
                                                }} disabled={isBusy}>
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
                        <CardContent className="flex-1 overflow-hidden p-0">
                            <Empty className="h-full">
                                <EmptyHeader>
                                <EmptyMedia variant="icon">
                                    <MessageCircleDashedIcon />
                                </EmptyMedia>
                                <EmptyTitle>您好, 大小寒!</EmptyTitle>
                                <EmptyDescription>
                                    我们今天来做什么呢？点击发送开始新的对话
                                </EmptyDescription>
                                </EmptyHeader>
                            </Empty>
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
                                <Textarea className="border-none rounded-none focus-visible:ring-0
                                    " style={{ maxHeight: 50 }} />
                                    {/* {nextMessage ? (
                                    getMessageText(nextMessage)
                                    ) : (
                                    <span className="text-muted-foreground">
                                        No messages queued. Reset the conversation.
                                    </span>
                                    )} */}
                                </div>
                                <InputGroupAddon align="block-end" className="pt-1">
                                <DropdownMenu>
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
                                </DropdownMenu>
                                <InputGroupButton
                                    type="submit"
                                    variant="default"
                                    size="icon-sm"
                                    // disabled={!nextMessage || isBusy}
                                    className="ml-auto"
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
