from flask import Flask, send_from_directory, jsonify, Response
from flask_cors import CORS
import os
import time
import win32clipboard
from PIL import Image, ImageGrab
import json
import threading
from queue import Queue
import traceback
import pywintypes

app = Flask(__name__, static_folder='public', template_folder='public')
CORS(app)

CLIPBOARD_IMAGE_PATH = os.path.join('public', 'clipboard.png')
last_clipboard_update = 0
last_clipboard_content = ""
clients = []
clipboard_lock = threading.Lock()

def process_clipboard_image():
    try:
        # Try both methods - pywin32 and Pillow
        return process_with_pywin32() or process_with_pillow()
    except Exception as e:
        print(f"Clipboard processing error: {str(e)}")
        return False

def process_with_pywin32():
    try:
        for _ in range(3):  # Retry up to 3 times
            try:
                with clipboard_lock:
                    win32clipboard.OpenClipboard()
                    try:
                        if not win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                            return False
                            
                        clipboard_data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                        
                        if len(clipboard_data) < 4:
                            return False
                            
                        width = abs(clipboard_data[2])
                        height = abs(clipboard_data[3])
                        
                        if width <= 0 or height <= 0 or width > 10000 or height > 10000:
                            return False
                            
                        expected_size = width * height * 4
                        if len(clipboard_data[1]) < expected_size:
                            return False
                            
                        image = Image.frombytes(
                            'RGBA', (width, height),
                            clipboard_data[1], 'raw', 'BGRA', 0, 1
                        )
                        
                        os.makedirs('public', exist_ok=True)
                        image.save(CLIPBOARD_IMAGE_PATH, 'PNG')
                        return True
                        
                    finally:
                        try:
                            win32clipboard.CloseClipboard()
                        except pywintypes.error:
                            pass
            except pywintypes.error as e:
                if e.winerror == 5:  # Access denied
                    time.sleep(0.1)
                    continue
                raise
            break
    except Exception:
        return False
    return False

def process_with_pillow():
    try:
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            os.makedirs('public', exist_ok=True)
            img.save(CLIPBOARD_IMAGE_PATH, 'PNG')
            return True
    except Exception:
        return False
    return False

def monitor_clipboard():
    global last_clipboard_update, last_clipboard_content
    
    while True:
        try:
            if process_clipboard_image():
                update_time = time.time()
                last_clipboard_update = update_time
                last_clipboard_content = "image"
                
                message = json.dumps({
                    'timestamp': update_time,
                    'hasImage': True
                })
                for client in clients[:]:
                    try:
                        client.put(f"data: {message}\n\n")
                    except:
                        clients.remove(client)
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Monitor error: {str(e)}")
            time.sleep(1)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/clipboard')
def get_clipboard_status():
    has_image = os.path.exists(CLIPBOARD_IMAGE_PATH)
    return jsonify({
        'timestamp': last_clipboard_update,
        'hasImage': has_image,
        'debug': {
            'public_dir': os.path.abspath('public'),
            'image_exists': os.path.exists(CLIPBOARD_IMAGE_PATH),
            'image_size': os.path.getsize(CLIPBOARD_IMAGE_PATH) if has_image else 0
        }
    })

@app.route('/clipboard.png')
def serve_clipboard_image():
    try:
        return send_from_directory(app.static_folder, 'clipboard.png')
    except Exception as e:
        return str(e), 404

@app.route('/stream')
def stream():
    def event_stream():
        client_queue = Queue()
        clients.append(client_queue)
        try:
            while True:
                message = client_queue.get()
                yield message
        finally:
            if client_queue in clients:
                clients.remove(client_queue)
    
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/debug')
def debug():
    return jsonify({
        'status': 'running',
        'clients': len(clients),
        'last_update': last_clipboard_update,
        'public_dir_contents': os.listdir('public') if os.path.exists('public') else []
    })

if __name__ == '__main__':
    os.makedirs('public', exist_ok=True)
    threading.Thread(target=monitor_clipboard, daemon=True).start()
    print(f"Server starting... Public dir: {os.path.abspath('public')}")
    app.run(host='0.0.0.0', port=3000, debug=True)