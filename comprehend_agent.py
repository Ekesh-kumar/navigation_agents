from langchain_community.chat_models import ChatOpenAI
import dotenv
import os
import json
import time
from screendeciderAgent import screenDeciderAgent
from prompts import prompts_provider

dotenv.load_dotenv()

class ComprehendAgent:   
    # 
    # Comprehend Agent analyzes screen data and checks if a given process step
    # can be performed based on the screen elements available.
    # 
    def __init__(self ):
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model_name="gpt-4-turbo", temperature = 0.3, openai_api_key=openai_api_key)
        self.prompt_provider = prompts_provider()

    def analyze_process_step(self, process_conditions,  prompt: str, summary:str) -> str:
        # Identifies the action to perform by comprehending JSON data to check for prompt requirement.
        screen_decider_Agent = screenDeciderAgent()
        check = screen_decider_Agent.analyze_screen(summary, prompt)

        if check in ["False", "false"]:
            return '["Screen is not suitable for the operation"]'
        
        process_analysis_results = self.per_screen_process_analyzer(process_conditions, summary)
        simplified_results = self.getSimplifiedResults(process_analysis_results)
        print(simplified_results)
        
        actions_prompt = self.prompt_provider.get_prompt("action_generator")
        actions_prompt = actions_prompt.format(process_analysis_results=process_analysis_results, summary=summary, prompt=prompt)
        response = self.llm.invoke(actions_prompt)
        return response.content

    def per_screen_process_analyzer(self,formatted_conditions, screen_data):

            condion_prompt = self.prompt_provider.get_prompt("process_analyzer") 
            prompt = condion_prompt.format(screen_data=screen_data, formatted_conditions=formatted_conditions)
            response = self.llm.invoke(prompt)
            return response.content


    def getSimplifiedResults(self, process_analysis_results):
        response = self.llm.invoke(f'''Given screen condition analysis in json data - {process_analysis_results},
                                     Give summary of conditions and results in the simple, userfriendly, readable format like 'what is the condition checked : condition analysis result'.'
                                  ''')
        return response.content


        
