import matplotlib.pyplot as plt
import io
import base64
from PIL import Image
from django.shortcuts import render
from .script import ltsm

def compress_image(image):
    # Open the image using PIL
    img = Image.open(image)

    # Convert the image to RGB mode if it's in RGBA mode
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Resize the image to reduce dimensions (adjust dimensions as needed)
    img = img.resize((800, 600))

    # Compress and save the image to a bytes buffer
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=70)
    buffer.seek(0)
    
    return buffer


def index(request):
    fig, ax = ltsm()

    # Convert the Matplotlib figure to a PNG image in memory
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    # Compress the image
    compressed_buffer = compress_image(buffer)

    # Encode the compressed image buffer to base64
    plot_image = base64.b64encode(compressed_buffer.getvalue()).decode()
    compressed_buffer.close()
    buffer.close()

    # Pass the base64 encoded image to the HTML template
    return render(request, 'index.html', {'plot_image': plot_image})
