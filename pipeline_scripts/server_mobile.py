from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/user', methods=['POST'])
def run_script():
    try:
        # Run your user.py script and capture its output
        completed_process = subprocess.run(['python', 'user.py'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # If the script was successful, return its output
        return completed_process.stdout, 200
    except subprocess.CalledProcessError as e:
        # If the script failed, return the error message
        error_message = e.stderr if e.stderr else 'An error occurred while running the script.'
        return error_message, 500

if __name__ == '__main__':
    app.run(debug=True)
