from flask import Flask, jsonify
import subprocess

"""app = Flask(__name__)

@app.route('/runscript', methods=['GET'])
def run_script():
    try:
        # Replace 'python' with 'python3' if required by your environment
        result = subprocess.run(['python', 'C:/GitHub/EVI-AI/pipeline_scripts/user.py'], stdout=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        return jsonify({'success': True, 'output': output}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)"""
