from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import webbrowser
from threading import Timer
from compressor import compress_image, batch_compress

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part'})
        
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'No file selected or invalid file type'})
        
        target_size_mb = request.form.get('target_size', default=10, type=int)
        
        # Create unique filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        
        # Create absolute paths
        base_dir = os.path.abspath(os.path.dirname(__file__))
        compressed_dir = os.path.join(base_dir, 'static', 'compressed')
        uploads_dir = os.path.join(base_dir, 'static', 'uploads')
        os.makedirs(compressed_dir, exist_ok=True)
        os.makedirs(uploads_dir, exist_ok=True)
        
        output_path = os.path.join(compressed_dir, unique_filename)
        input_path = os.path.join(uploads_dir, unique_filename)
        
        # Save and compress
        file.save(input_path)
        compress_image(input_path, output_path, target_size_mb)
        
        # Get compressed file size
        compressed_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
        
        # Generate relative URL for static file
        file_url = url_for('static', filename=f'compressed/{unique_filename}')
        
        return jsonify({
            'success': True,
            'size': round(compressed_size, 2),
            'output_path': file_url
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400  # Return 400 status code
    
    finally:
        # Clean up input file
        if 'input_path' in locals() and os.path.exists(input_path):
            os.remove(input_path)

def open_browser():
    """Open browser automatically when Flask starts"""
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Only open browser if not in reloader process
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        Timer(1.5, open_browser).start()
    # Run Flask application
    app.run(debug=True)