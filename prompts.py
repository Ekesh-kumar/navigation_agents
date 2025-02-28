
class prompts_provider :
    
    def __init__(self):
        self.prompts = {
            "action_generator" : '''  
                                You are an intelligent mainframe terminal agent. Your task is to return ONLY the ordered set of keys required to perform the specified action, given as a prompt.

                                ### **Step 1: Validate Process Conditions**
                                - Analysze the json file - `{process_analysis_results}` and if json file contains any failed conditions, return:
                                
                                ["Condtions failed"] and Do not proceed further.

                                - If all conditions are satisfied, proceed to Step 2.

                                ### **Step 2: Task Execution (Generate Actions)**
                                - Given the screen summary -{summary} in the json format, which contains details of the screen ordered in different key value pairs, which you need to work on.
                                - Given the task for actions to be performed in the text-{prompt}.
                                Instructions for action generation:
                               ** Note edge case : 
                                -If asked for login"
                                return hardcoded response as:
                                ['CREDENTIALS'].
                                Clearly determine and list the keys or inputs required, in the correct execution order.
                                ** Go through the entire screen json file for determing the best action to give.                             
                                ** If task is to select a perticular option then give what value we need type to select the value, don't give enter in response just give key to press.
                                ** If action is to extract any fields from the screen, go through the entire screen info and select the values which best soots for the description.
                                ** If any task says direclty to select some perticular option from screen, return that options itself as response.
                                Action Types: 
                                Navigation: Specify keys needed for navigation.
                                Field Extraction: Provide keys required for extracting/interacting with fields.
                                Important:
                                Return only the ordered keys in Python list format.
                                Do NOT include explanations or additional context.
                                ''',
                                
            "process_analyzer" : '''
                                You are an AI assistant responsible for verifying process conditions based on the provided screen data.
                                Your task is to analyze the given conditions and provide an output in the required format.
        
                                ### **Screen Data:**
                                The screen data is structured as JSON, containing fields, subfields, nested arrays, and options.
                                - **Screen Data:** {screen_data}
                                - ** Understand all the fields in screen data clearly.

                                ### **Conditions to Check:**
                                The conditions define the criteria that must be met before proceeding with the process.
                                - **Formatted Conditions JSON:** {formatted_conditions}
                                - if no conditons are specified , then return "All the conditions are satisfied".
                                - **Important:** Field names in conditions **may not exactly match** the screen data keys, so use **semantic understanding** to relate them correctly.
                                    
                                ### **Instructions:**
                                1. **Identify and Extract Fields Dynamically:**
                                - Do not assume a single occurrence of a field.
                                - If a field exists inside an **array** (e.g., `benefits[]`), iterate over **all** occurrences.
                                - **Ensure all required fields** related to the condition are checked.

                                2. **Verify Field Values Are Valid:**
                                - A field is **invalid** if it is empty (`""`), `"null"`, `"N/A"`, or `None`.
                                - If a required field exists but contains **invalid data**, the condition must be **NOT met**.

                                3. **Use Semantic Matching for Field Names:**
                                - Match fields based on **meaning, not exact words**.
                                - Use **fuzzy matching** to detect variations like:
                                    - `"benefitCode"` ≈ `"benefit_code"`, `"benefit identifier"`, `"coverage code"`
                                    - `"paymentIndicator"` ≈ `"pay_status"`, `"payment_flag"`
                                - Ensure the AI finds **the best matching field** dynamically.

                                4. **Strict Condition Evaluation:**
                                - If **ANY** required field **fails**, mark the condition as **NOT met**.
                                - If **ALL** relevant fields pass, mark the condition as **met**.

                                5. **Return Output in Strict JSON Format:**
                                ```json
                                {{"condition_name": "condition met or not and reason in few words"}}.
                                6. **Dont give entire analysis sumamry give only short summary weather condition met or not
                                ''',

            "screen_analyzer" : """
                Given the following screen data which is in json format :
                {screen_data}.
                And the following task prompt:
                {task_prompt}.

                ** Understand the all the fields of screen data clearly.
                ** Determine if the task can be executed based on the screen's current state.

                ### **Validation Criteria:**
                - Identify the fields required to execute the task from the given task prompt.
                - Use **semantic matching** to recognize variations in wording for actions and fields required for action(e.g., "Type Y and Enter" ≈ "Press Y and hit Enter" ≈ "Input Y and confirm").
                - Assume that an **input field is always present** unless the screen explicitly states otherwise.
                - If the task requires **pressing a key (e.g., 'Enter')**, assume the system supports this action unless explicitly restricted.
                - If **all** required fields are present in the screen data (or functionally equivalent), return `true`.
                - If **any** required field is **explicitly missing**, return `false`.
                ### **Important Notes:**
                - If an action like "Type or Enter" is required, assume that an **input box exists** and can accept the key press.
                - **Do not be overly strict** with wording—if functionally equivalent elements exist, they should be considered a match.
                --**return summary in few words
                - **Strictly return only `true` if tasks mentioned in the prompt are matching the screen data else return `false` dont return any explanations.
                """
        }

    def get_prompt(self, prompt_name):
        return self.prompts.get(prompt_name)
            