import re
from langchain_community.chat_models import ChatOpenAI
import dotenv
import os
from comprehend_agent import ComprehendAgent
from navigation_screen_set import navigation_set
from emulator_client import EmulatorClient
import sys
import ast

dotenv.load_dotenv()

class processAgent:

    def perform_process(self, navigation, nextScreenstart) -> tuple[str, int]:
        agent = ComprehendAgent()
        navigation_data = navigation_set()
        
        navigation_info = navigation_data.get_navigation(navigation)    
         
        start_command = navigation_info.get("Emulator_starting_command")
        size = len(navigation_info)
        client = EmulatorClient() 
        screens = client.process_command(start_command)
        if nextScreenstart is None:
            screen_index = 1
        else:
            screen_index = navigation_info.get(nextScreenstart).get("index")
        # screen_index = nextScreenstart
        for i in range(screen_index, size) :

            key = "screen" + str(i)
            print(key)
            __condition = navigation_info.get(key).get("condition")
            __step = navigation_info.get(key).get("step")

            # you are going to check if this is issuing a REPEAT COMMAND
            # if it does do not continue anything just restart from the next screen
            pattern = r"\[REPEAT FROM (\w+) (\d+) Times\]"
            match = re.search(pattern, __step.strip())
            
            if match:
                screen_name = match.group(1)
                repeat_count = int(match.group(2))
                return screen_name, repeat_count

            actionstr = agent.analyze_process_step(__condition, __step, screens)

            print("actions..........."+actionstr)
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
                    print("pressed Key" + actionKey)
                    screens  =  client.process_command(actionKey)
                    
        
        return "process completed.....", 1
    


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

        nextScreenstart = None
        maxCount = 1
        currentCount = 0
        
        while True:
        
            if currentCount > maxCount:
                break
            
            result_string, result_int = proccess_agent.perform_process(navigation, nextScreenstart) # tuple[str, int]

            maxCount = result_int
            nextScreenstart = result_string
            currentCount = currentCount+1
            
            # just to not stuck in endless loop
            if currentCount > 5:
                break
        
  