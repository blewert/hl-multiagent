## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Utility class (misc. bits and bobs)
##

class Vector2D:
	#Like a namedtuple, but mutable (so like recordtype).
	def __init__(self, x, y):
		self.x = x;
		self.y = y;
		
class CRect:
	def __init__(self, x, y, w):
		self.tl = Vector2D(x - w, y - w);
		self.tr = Vector2D(x + w, y - w);
		self.br = Vector2D(x + w, y + w);
		self.bl = Vector2D(x - w, y + w);
		
class VisionCone:
	#Vision cone for each agent. Set up default fill colour
	default_fill = "#cccccc";
	
	def __init__(self, interiorAngle, length, agent, tag=None, fill=None):
		#Setup vision cone instance variables
		self.interiorAngle = interiorAngle;
		self.length = length;
		self.fill = fill;
		self.tag = tag;
		self.agent = agent;
	
	def set_fill(self, color):
		self.fill = color;
		self.agent.environment.canvas.itemconfigure(self.tag, fill=self.fill); 