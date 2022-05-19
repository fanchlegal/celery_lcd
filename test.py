from rgbmatrix import graphics
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
					format='(%(threadName)-9s) %(message)s',)
from queue import Queue					

def wait_for_event(queue_in):
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
		if not queue_in.empty():
			my_text = queue_in.get()
		offscreen_canvas.Clear()
		graphics.DrawText(offscreen_canvas, font, 0, 30, textColor, my_text)
		offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
		if e.is_set():
			break
			
messages = ["hello","the","world"]		
if __name__ == '__main__':
	e = threading.Event()
	queue1 = Queue()
	
	t2 = threading.Thread(name='non-blocking', 
					  target=wait_for_event, 
					  args=(queue1,))
	t2.start()
	
	logging.debug('Waiting before calling Event.set()')
	for m in messages:
		queue1.put(m)
		#time.sleep(0.2)
	
	time.sleep(30)
	e.set()
	logging.debug('Event is set')