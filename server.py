# coding: utf-8 

import socket
import threading
from rgbmatrix import graphics
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import json
from PIL import Image
import io
import base64

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",1111))

options = RGBMatrixOptions()
options.hardware_mapping = "regular"
options.rows = 64
options.cols = 64
options.gpio_slowdown = 4
matrix = RGBMatrix(options = options)
offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("fonts/7x13.bdf")
textColor = graphics.Color(255, 255, 0)
pos = offscreen_canvas.width
my_text = ""

offscreen_canvas.Clear()


while True:
	tcpsock.listen(10)
	print( "En écoute...")
	text = False
	image = False
	
	(clientsocket, (ip, port)) = tcpsock.accept()
	cmd = clientsocket.recv(4096)
	
	if cmd:
		print(cmd)
		data = json.loads(cmd.decode('utf-8'))
		if data.get('type',False):
			if data.get("type") == "text":
				text = True
				pos = data.get('pos',(0,1))
				size = data.get('size',4096)
			elif data.get("type") == "image":
				image = True
				size = data.get('size',4096)
			# on envoie au client le fait qu'on a bien reçu les données
			clientsocket.send(b'1')
			# on attend les datas
			r = clientsocket.recv(size)
			if r:
				if text:
					print("Affichage du texte")
					data = r.decode('utf-8')
					offscreen_canvas.Clear()
					graphics.DrawText(offscreen_canvas, font, pos[0], pos[1], textColor, data)
					offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
				if image:
					print("Affichage de l'image")
					image = Image.open(io.BytesIO(base64.b64decode(r)))
					image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
					offscreen_canvas.Clear()
					matrix.SetImage(image.convert('RGB'))
		
		else:
			print("Pas de type dans la commande, ignoré...")
	else:
		print("Pas de données...")
	
	
			
			
	
