
class prompts_provider :
    
    def __init__(self):
        self.prompts = {
            "action_generator" : '''  
                                You are an intelligent mainframe terminal agent. Your task is to return ONLY the ordered set of keys required to perform the specified action, given as a prompt.

                                ### **Task Executor (Generate Actions)**
                                **Screen Data:**
                                    Given the screen data which is structured in json format , containing fields, subfields, nested arrays, and options.
                                    Use this screen data as information source for your tasks executions.
                                    - Understand all the fields in screen data clearly.
                                    - Screen Data: {screen_data}.
                                
                                **Task Prompt:**
                                 - Given the tasks for actions to be performed in the screen
                                  tasks :- {prompt}.

                               **Instructions for action generation:**
                               ** Note edge case : 
                                -If asked for login"
                                return hardcoded response as:
                                ['action:CREDENTIALS'].
                                Clearly determine and list the keys or inputs required, in the correct execution order.
                                ** Go through the entire screen json file for determing the best action to give.                             
                                ** If task is to select a perticular option then in the format 'action:value'give what value we need type to select the value, don't give enter in response just give key to press.
                                ** If action is to extract or display any fields from the screen, go through the entire screen info and extract the values of field which best soots for the description, and give them in format 'display:value'.
                                ** If any task says direclty to select some perticular option from screen, return that options itself as response.
                                ** If any tasks says about 
                               ** Action Types which may be in the task: 
                                Navigation: Specify keys needed for navigation.
                                Field Extraction: Provide value of key asked for extracting/displaying.
                                
                                Important:
                                There will be two types of tasks in the prompt, 1. Action task 2. Display task.
                                If task is about performing action or selecting some options it will be action task so return response as 'action:key'.
                                If the task about displaying or extracting any fields then add extracted field value as 'display:extracted value'.
                                Return only the ordered keys or extracted value in Python list format.
                                Do NOT include explanations or any additional characters for output, return only valid python list.

                                **output format:**
                                Strictly follow the Example output format in response ,Example output:  ['display:newyork','action:O', 'action:1'].
                                ''',
                                
            "process_analyzer" : '''
                                    You are an AI assistant responsible for verifying process conditions based on the provided screen data.
                                    Your task is to analyze the given conditions and provide an output in the required format.
            
                                    ### **Screen Data:**
                                    Given the screen data structured in json foramt containing fields, subfields, nested arrays, and options.
                                    You need check the data in screen Data against the condition provided.
                                    Use this screen data as data source for your condition checks.
                                    Understand all the fields in screen data clearly.
                                    - Screen Data: {screen_data}
                                    
                                    ### **Conditions to Check:**
                                    - The conditions define the criteria that must be met before proceeding with the process.
                                    - Given conditions in the json format to be checked against the screen data : {formatted_conditions}.
                                    - If no conditons are specified , then return "No condtions to check", and don't proceed further.
                                    - **Important:** Field names in conditions **may not exactly match** the screen data keys, so use **semantic understanding** to relate them correctly.
                                        
                                    ### **Instructions for execution:**
                                        
                                    1. **Identify and Extract Fields Dynamically from screen data:**
                                    - Dont assume that strucutred data is given for conditon analysis, Extract all the required fields from screen data for analysing the conditions.
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
                                  
                                  **output format:**
                                    *for each condition return Output in Strict JSON Format:*
                                    ```json
                                    {{"condition_name": "condition met or not and reason in few words"}}.
                                    *Dont give entire analysis sumamry give output as mentioned in output format.
                                    '''
                                    ,

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
                                    """,

            "conditions_summary_analyzer" : '''
                                             Given the condition analysis in json data - {conditions_analysis},
                                             Check if any condition is not met.
                                             If no conditions to check in the json data return "Ok".
                                             If any one of the conditions is also not met, return only "Conditions not met", else return only "Ok".
                                             Dont return extra sumamry or analysis.
                                            ''',
            "condition_summarizer" : '''
                                     ** Given condition analysis in json data - {process_analysis_results},
                                     ** Your job is to analyze the given json data below, Give a small response of each condition checked in a simple, userfriendly and readable format like condition name : result of condition check in given data'.
                                     ** give result in line by line don't include any json formats, Extra summary.
                                      '''            
        }

    def get_prompt(self, prompt_name):
        return self.prompts.get(prompt_name)
            