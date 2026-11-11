import os
from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

session = None

def get_session():
    global session
    if session is None:
        session = new_session("u2netp")
    return session

# strict_slashes=False permite recibir tanto /remove-bg como /remove-bg/
@app.route('/remove-bg', methods=['POST'], strict_slashes=False)
def remove_bg():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    
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
