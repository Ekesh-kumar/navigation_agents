from langchain_community.chat_models import ChatOpenAI
import dotenv
import os
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
        breaked_conditions = self.condition_break_down(process_conditions)
        process_analysis_results = self.per_screen_process_analyzer(breaked_conditions, summary)
        simplified_results = self.getSimplifiedResults(process_analysis_results)
        print(simplified_results)

        results =self.condition_sumamry_analyzer(process_analysis_results)
        if("conditions not met" in results.lower()):
            return '["conditions failed"]'
        
        actions_prompt = self.prompt_provider.get_prompt("action_generator")
        actions_prompt = actions_prompt.format(screen_data=summary, prompt=prompt)
        response = self.llm.invoke(actions_prompt)
        return response.content

    def per_screen_process_analyzer(self,formatted_conditions, screen_data):

            condition_prompt = self.prompt_provider.get_prompt("process_analyzer") 
            prompt = condition_prompt.format(screen_data=screen_data, formatted_conditions=formatted_conditions)
            response = self.llm.invoke(prompt)
            return response.content


    def getSimplifiedResults(self, process_analysis_results):

        condition_prompt = self.prompt_provider.get_prompt("condition_summarizer") 
        prompt = condition_prompt.format(process_analysis_results = process_analysis_results)
        response = self.llm.invoke(prompt)
        return response.content

    
    def condition_sumamry_analyzer(self, process_analysis_results):
        condition_prompt = self.prompt_provider.get_prompt("conditions_summary_analyzer") 
        prompt = condition_prompt.format(conditions_analysis = process_analysis_results)
        response = self.llm.invoke(prompt)

        return response.content
    
    def condition_break_down(self, conditions):
         
         response = self.llm.invoke(f'''
                                    Given the conditions - {conditions},break down the combined conditions into individual conditions and return in json format.
                                    Only analyse the givn condtions and don't give any general response or summary.
                                    output format : {{condition_name: condition description}}.
                                    If no conditions are present return "No conditions to check".
                                     ''')
         return response.content      

        
