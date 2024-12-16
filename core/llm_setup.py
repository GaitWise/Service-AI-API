# core : 핵심기능, 전역적으로 사용되는 설정 파일 관리


def get_llm(model_name='llama3'):
    from langchain_ollama import OllamaLLM
    from langchain.chat_models import ChatOpenAI
    if model_name == 'gpt':
        return ChatOpenAI(
            openai_api_key="sk-proj-Bh0eraNNIQUH5zjni2",  # OpenAI API 키
            model="gpt-4",  # GPT-4 모델
            temperature=0.7  # 생성 다양성 조절
        )
    return OllamaLLM(
        model=model_name,
        base_url="http://localhost:11434"
    )