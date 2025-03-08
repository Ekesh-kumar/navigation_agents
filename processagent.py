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
    def perform_process(self, navigation, callback=None) -> str:
        navigation_data = navigation_set()
        navigation_info = navigation_data.get_navigation(navigation)    
        start_command = navigation_info.get("Emulator_starting_command")
        size = len(navigation_info)
        client = EmulatorClient()
        screens = client.process_command(start_command)
        
        # Send initial feedback
        if callback:
            callback(f"Starting navigation: {navigation}")
            callback(f"Emulator started with command: {start_command}")
        
        starting_step = 1
        loop_counter = 1
        counter = 0
        
        while counter < loop_counter:
            starting_step, loop_counter, screens = self.execute_step(
                navigation_info, 
                starting_step, 
                client, 
                screens, 
                size, 
                callback
            )
            counter = counter + 1
            
            if callback:
                callback(f"Completed round {counter} of {loop_counter}")
        
        if callback:
            callback("Navigation process completed successfully")
            
        return "process completed....."
   
    def execute_step(self, navigation_info, starting_screen_index, client, screens, size, callback=None) -> tuple:
        agent = ComprehendAgent()  
        
        for i in range(starting_screen_index, size):            
            key = "screen" + str(i)
            conditon = navigation_info.get(key).get("condition")
            step = navigation_info.get(key).get("step")
            
            # Send step information
            if callback:
                callback(f"Processing step {i}: {step}")
           
            pattern = r"REPEAT FROM SCREEN(\d+) (\d+) Times"
            match = re.search(pattern, step.strip())
            screen_name = "screen1"
            repeat_count = 1
           
            if match:
                screen_name = int(match.group(1))
                repeat_count = int(match.group(2))
                if callback:
                    callback(f"Detected loop: Repeating from screen {screen_name} for {repeat_count} times")
                return screen_name, repeat_count, screens
                
            actionstr = agent.analyze_process_step(conditon, step, screens)
            
            # Make sure actionstr is valid before evaluating
            try:
                actions = ast.literal_eval(actionstr.strip())
                
                if callback:
                    callback(f"Generated {len(actions)} actions for step {i}")
                
                for a in range(0, len(actions)):
                    if "conditions failed" in actions[a].lower():
                        if callback:
                            callback(f"Condition failed : {actions[a]}")
                        return starting_screen_index, 0, screens
                    elif "display" in actions[a].split(':')[0]:
                        message = actions[a].split(":")[1]
                        if callback:
                            callback(f"Display : {message}")
                    else:
                        actionKey = actions[a].split(":")[1]
                        if callback:
                            callback(f"Typing : {actionKey}")
                        screens = client.process_command(actionKey)
            except (SyntaxError, ValueError) as e:
                if callback:
                    callback(f"Error parsing actions: {e}. Raw response: {actionstr}")
                # Continue to next step instead of breaking completely
                continue
           
        return starting_screen_index, repeat_count, screens