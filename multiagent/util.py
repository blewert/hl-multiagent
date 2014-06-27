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
		
class VisionCone:
	#Vision cone for each agent. Set up default fill colour
	default_fill = "#cccccc";
	
	def __init__(self, interiorAngle, length, tag=None, fill=None):
		#Setup vision cone instance variables
		self.interiorAngle = interiorAngle;
		self.length = length;
		self.fill = fill;
		self.tag = tag;