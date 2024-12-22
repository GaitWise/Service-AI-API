# core : 핵심기능, 전역적으로 사용되는 설정 파일 관리
from langchain_ollama import OllamaLLM
from langchain.chat_models import ChatOpenAI

def get_llm(model_name='llama3'):
    if model_name == 'gpt':
        return ChatOpenAI(
            openai_api_key="", 
            model="gpt-4", 
            temperature=0.7  
        )
    return OllamaLLM(
        model=model_name,
        base_url="http://192.168.25.31:11434"
    )