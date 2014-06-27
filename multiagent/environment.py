## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Environment class
##

import tkinter

from .util import Vector2D
from .patch import Patch

class Environment:
	def __init__(self, width, height, wrap=True):
		#Set origin point to 0.0, 0.0 by default
		self.origin = Vector2D(0,0);
		
		#Setup dimensions of environment
		self.width  = width;
		self.height = height;
		
		#Generate a tkinter window and canvas to draw on, set to instance vars
		self.tk     = tkinter.Tk();
		self.canvas = tkinter.Canvas(self.tk, width=width, height=height);
		
		#Setup wrapping bool
		self.wrap = wrap;
		
		#And pack (to start drawing)
		self.canvas.pack();			
		
	def draw(self):
		#On draw, just call canvas.update()
		self.canvas.update();		
	
	def create_patches(self, amountX, amountY, fill=Patch.default_fill):
		self.patches = [];
		
		sizeX = (self.width  / amountX);
		sizeY = (self.height / amountY);
		
		for x in range(0, amountX):
			for y in range(0, amountY):
				topLeft     = Vector2D(x * sizeX, y * sizeY);
				bottomRight = Vector2D(topLeft.x + sizeX, topLeft.y + sizeY);
				
				patchToAppend = Patch(topLeft.x, topLeft.y, bottomRight.x, bottomRight.y, environment=self, fill=fill);
				self.patches.append(patchToAppend);
