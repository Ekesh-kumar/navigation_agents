from langchain_community.chat_models import ChatOpenAI
import dotenv
import os
import json
from comprehend_agent import ComprehendAgent
from navigation_screen_set import navigation_set
from emulator_client import EmulatorClient
import sys

dotenv.load_dotenv()

class processAgent:

    def perform_process(self, navigation) -> str:
        agent = ComprehendAgent()
        navigation_data = navigation_set()
        
        navigation_info = navigation_data.get_navigation(navigation)    
         
        start_command = navigation_info.get("Emulator_starting_command")
        size = len(navigation_info)
        client = EmulatorClient() 
        screens = client.process_command(start_command)
        for i in range(1, size) :
            key = "screen" + str(i)
            actionstr = agent.analyze_process_step(navigation_info.get(key).get("condition"),navigation_info.get(key).get("step"), screens)
            actions = json.loads(actionstr)
            for a in range(0, len(actions)):
                if actions[a] == 'Screen is not suitable for the operation':
                    print(actions[a])
                    return
                else:
                    screens  =  client.process_command(actions[a])
        
        return "process completed....."

if __name__ =="__main__":
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
    proccess_agent = processAgent()
    navigation = input("Enter the navigation process:")

    if navigation in ["exit", "end"]:
        sys.exit()

    proccess_agent.perform_process(navigation)
  