import bs4
from core.llm_setup import get_llm
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableMap
from langchain_community.document_loaders import WebBaseLoader

# [Function] fetch_web_content
# Parameters: url (str): 웹 페이지 URL
# Returns: str: 웹 페이지에서 가져온 텍스트 콘텐츠
def fetch_web_content(url: str):
    try:
        # WebBaseLoader를 사용하여 URL에서 데이터 로드
        loader = WebBaseLoader(
            web_paths=(url,),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    id="main-content" 
                )
            ),
        )
        
        docs = loader.load()
        full_content = "\n".join([doc.page_content for doc in docs])
        print(f"Web content loaded. Length: {len(full_content)} characters")
        return full_content
    except Exception as e:
        print(f"Error fetching web content: {e}")
        return ""


# [Function] generate_report
# Parameters: response_data (dict): 사용자 데이터, model_name (str): 사용할 모델 이름 ('llama3' 또는 'gpt')
# Returns: str: LLM에서 생성된 사용자 걸음 데이터 보고서
def generate_report(response_data, model_name='llama3'):
    
    url = "https://www.mayoclinic.org/healthy-lifestyle/fitness/in-depth/walking/art-20046261"
    web_content = fetch_web_content(url)

    # Prompt Template 설정
    template = """
    Below is the walking data analysis for the user:
    Steps: {steps}
    Distance: {distance}
    Calories burned: {calories}
    Balance score: {balance_score}
    Gait status: {gait_status}
    Training recommendation: {training_recommendation}

    Additionally, here is relevant health and walking information:
    {retrieved_content}

    Based on this data and the provided information, summarize the user's walking performance and provide further insights or recommendations.
    """
    prompt = PromptTemplate(
        input_variables=["steps", "distance", "calories", "balance_score", "gait_status", "training_recommendation", "retrieved_content"],
        template=template
    )

    # LLM 설정
    llm = get_llm(model_name=model_name)

    # RunnableMap 사용
    sequence = RunnableMap({"llm": llm})

    data = {
        "steps": response_data['steps'],
        "distance": response_data['distance'],
        "calories": response_data['calories'],
        "balance_score": response_data['balance_score'],
        "gait_status": response_data['gait_status'],
        "training_recommendation": response_data['training_recommendation'],
        "retrieved_content": web_content  
    }
    
    formatted_prompt = prompt.format(**data)
    report = sequence.invoke(formatted_prompt)['llm']
    return report

