from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Sesión liviana y rápida optimizada para CPU
session = new_session("isnet-general-use")

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    
    file = request.files['image']
    input_image = Image.open(file.stream)
    
    # Procesamiento ultrarrápido sin consumo excesivo de RAM
    output_image = remove(input_image, session=session)
    
    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)