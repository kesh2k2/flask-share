from flask import Flask, render_template, request, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Manually set CORS headers
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Render HTML
@app.route('/')
def index():
    return render_template('index.html')

# Flask Endpoints
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return jsonify({"message": f"File '{file.filename}' uploaded successfully!"})

@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return jsonify({"files": files})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": f"File '{filename}' deleted successfully!"})
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)