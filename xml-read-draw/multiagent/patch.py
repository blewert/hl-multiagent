## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Patch class, to represent patches in the environment.
##

from .util import Vector2D

class Patch:

	current_patch_id = 0;
	default_fill = "#ffffff";
	
	def __init__(self, x, y, width, height, environment=None, fill=default_fill, grid=True):
		#Setup local pos, width and height of patch.
		self.pos    = Vector2D(x, y);
		self.width  = width;
		self.height = height;
		
		#Set id and update current id counter.
		self.id     = Patch.current_patch_id;
		Patch.current_patch_id += 1;
		
		#Setup fill colour, and whether or not this patch should display an outline
		self.fill = fill;
		self.grid = grid;
		
		#If environment isn't null (is specified), then situate this patch in the environment.
		if environment != None:
			self.situate(environment);
	
	def situate(self, environment):
		self.environment = environment;
		self.shapeTag = ("patch%d-shape" % (self.id));
		
		ptFrom = Vector2D(self.pos.x, self.pos.y);
		ptTo   = Vector2D(self.pos.x + self.width, self.pos.y + self.height);
		
		if self.grid:
			self.environment.canvas.create_rectangle(ptFrom.x, ptFrom.y, ptTo.x, ptTo.y, fill=self.fill, width=1, tag=self.shapeTag);
		else:
			self.environment.canvas.create_rectangle(ptFrom.x, ptFrom.y, ptTo.x, ptTo.y, fill=self.fill, width=0, tag=self.shapeTag);
			
	
	def set_fill(self, fill):
		self.fill = fill;
		
		if hasattr(self, 'environment'):
			self.environment.canvas.itemconfigure(self.shapeTag, fill=fill);
			
	def get_fill(self, fill):
		return self.fill;
