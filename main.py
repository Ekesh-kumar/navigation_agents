from flask import Flask, render_template, jsonify
from processagent import processAgent
from flask_socketio import SocketIO, emit
import dotenv
import os
from navigation_screen_set import navigation_set
import traceback

dotenv.load_dotenv()
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow cross-origin if needed

@app.route('/')
def home():
    navigation_data = navigation_set()
    prompts = navigation_data.getNavigationOptions()
    return render_template('index.html', prompts=prompts)

@socketio.on('start_navigation')
def handle_navigation(data):
    prompt = data['prompt']
    try:
        # Create a callback function that emits Socket.IO events
        def progress_callback(step_result):
            # Make sure step_result is converted to string for safety
            message = str(step_result)
            emit('navigation_step', {'message': message})
       
        # Pass the callback to your process agent
        process_agent = processAgent()
        results = process_agent.perform_process(prompt, progress_callback)
       
        # When all steps are complete
        emit('navigation_complete', {'message': 'Navigation completed successfully'})
    except Exception as e:
        # Get detailed error information
        error_details = traceback.format_exc()
        print(f"Error during navigation: {error_details}")
        emit('navigation_error', {'message': f"Error: {str(e)}"})

@app.route('/update_prompts')
def update_prompts():
    try:
        navigation_data = navigation_set()
        prompts = navigation_data.getNavigationOptions()
        return jsonify(list(prompts))
    except Exception as e:
        print(f"Error updating prompts: {str(e)}")
        return jsonify([])

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8080)