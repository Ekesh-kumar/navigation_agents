import os
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
from prompts import prompts_provider

# Load environment variables
load_dotenv()

class screenDeciderAgent :

    def __init__(self ):
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature = 0.3,openai_api_key=openai_api_key)
        self.promptProviderObj = prompts_provider()

    def analyze_screen(self , screen_data, task_prompt) -> str:
        
        prompt = self.promptProviderObj.get_prompt("screen_analyzer")
        prompt = prompt.format(screen_data=screen_data, task_prompt=task_prompt)
        response = self.llm.invoke(prompt)

        return response.content
 
    

