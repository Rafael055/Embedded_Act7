from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/greeting', methods=['GET'])
def greeting():
    return jsonify({'message': 'Hello from Flask!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
