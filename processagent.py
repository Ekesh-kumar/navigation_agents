from langchain_community.chat_models import ChatOpenAI
import dotenv
import os
from comprehend_agent import ComprehendAgent
from navigation_screen_set import navigation_set
from emulator_client import EmulatorClient
import sys
import re
import ast

dotenv.load_dotenv()

class processAgent:

    def perform_process(self, navigation) -> str:
        
        navigation_data = navigation_set()
        
        navigation_info = navigation_data.get_navigation(navigation)    
        start_command = navigation_info.get("Emulator_starting_command")
        size = len(navigation_info)
        client = EmulatorClient() 
        screens = client.process_command(start_command)
        starting_step = 1
        loop_counter = 1
        counter = 0
        loop_counter = 1
        while counter < loop_counter :
           starting_step, loop_counter, screens = self.execute_step(navigation_info,starting_step,client,screens,size)
        #    print(f" starting step {type(starting_step)} , loop counter {loop_counter} , screens {screens}")
           counter = counter + 1
           print("finished one round")
           
        return "process completed....."
    
    def execute_step(self, navigation_info, starting_screen_index, client,screens, size) -> str:
        
        agent = ComprehendAgent()  
        for i in range(starting_screen_index, size) :            
            key = "screen" + str(i)
            conditon = navigation_info.get(key).get("condition")
            step = navigation_info.get(key).get("step")
            
            pattern = r"REPEAT FROM SCREEN(\d+) (\d+) Times"
            match = re.search(pattern, step.strip())
            screen_name = "screen1"
            repeat_count = 1
            
            if match:
                screen_name = int(match.group(1))
                repeat_count = int(match.group(2))
                # print(f"navigation info {navigation_info}  , starting step {screen_name} , loop counter {repeat_count} , screens {screens}")
                return screen_name, repeat_count, screens

            actionstr = agent.analyze_process_step(conditon, step, screens)

            actions = ast.literal_eval(actionstr.strip())
            print(actions)
            for a in range(0, len(actions)):
                if "conditions failed" in actions[a].lower():
                    print(actions[a])
                    return
                elif "display" in actions[a].split(':')[0]:
                    print(actions[a].split(":")[1])
                
                else:
                    actionKey = actions[a].split(":")[1]
                    screens  =  client.process_command(actionKey)
            
        return screen_name, repeat_count,screens
          
if __name__ =="__main__":
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
    proccess_agent = processAgent()
    active = True
    while(active):
        navigation = input("Enter the navigation process:")

        if navigation in ["exit", "end"]:
            active = False
            break
        proccess_agent.perform_process(navigation)
  