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
	
	def create_patches(self, amountX, amountY, fill=Patch.default_fill, situate=True, grid=True):
		#Set self.patches to a empty list for now
		self.patches = [];
		
		#Specify patch amount (w and h), for later use (patch_at())
		self.patchamount = Vector2D(amountX, amountY);
		
		#Find the size of each patch for the environment
		sizeX = (self.width  / amountX);
		sizeY = (self.height / amountY);
		
		#Set environment to this environment instance if it's true, else pass null
		environment = (self if situate else None);
		
		for x in range(0, amountX):
			for y in range(0, amountY):
				#Run through x and y, define coordinates to draw to/from
				topLeft     = Vector2D(x * sizeX, y * sizeY);
				bottomRight = Vector2D(topLeft.x + sizeX, topLeft.y + sizeY);
				
				#Create a new patch with specified parameters, and append it to the list of patches
				patchToAppend = Patch(topLeft.x, topLeft.y, bottomRight.x, bottomRight.y, environment=environment, fill=fill, grid=grid);
				self.patches.append(patchToAppend);
