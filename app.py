import os
from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

session = None

def get_session():
    global session
    if session is None:
        from rembg import new_session
        session = new_session("u2netp")  # Modelo ultra ligero de muy bajo consumo de RAM
    return session

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    
    from rembg import remove
    
    file = request.files['image']
    input_image = Image.open(file.stream)
    
    sess = get_session()
    output_image = remove(input_image, session=sess)
    
    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
