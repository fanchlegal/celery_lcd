from .celery import app

import socket
import json
import base64


from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
	
@app.task
def text_lcd(name):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("", 1111))
	data = json.dumps({ 'type' : 'text', 'pos': (0,10), 'size': len(name)})
	s.send(data.encode('utf-8'))
	s.recv(1)
	s.send(name.encode('utf-8'))
	
	
@app.task
def img_lcd(image):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("", 1111))
	data = json.dumps({ 'type' : 'image', 'size': len(image)})
	s.send(data.encode('utf-8'))
	s.recv(1)
	s.send(image.encode('utf-8'))
	