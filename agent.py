from langchain.agents import create_agent, AgentState
from langchain_ollama import ChatOllama
from prompts import system_prompt

def dxh_agent():
    agent = create_agent(
        # model=ChatOllama(model="qwen3:latest"),
        model="ollama:qwen3:latest",
        tools=[],
        system_prompt=system_prompt,
    )
    return agent

if __name__ == "__main__":
    agent = dxh_agent()
    print("开始调用....")
    result = agent.invoke({
        "messages" : [
            {"role": "user", "content": "请你提供一份广州3天的旅游攻略，出行时间为2026.1.1到2026.1.3"}
        ]
    })
    print(result)
    print("调用结束!!!")
