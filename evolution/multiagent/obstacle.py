## Benjamin Williams <eeu222@bangor.ac.uk>
## ---
## Class for obstacles in the environment
##    - Only support currently is rects.

try:
	import tkinter
except ImportError:
	import Tkinter as tkinter
	
class Obstacle:
	
	current_obstacle_id = 0;
	
	def __init__(self, x, y, w, h):
		self.collidable = True;
		self.x1 = x;
		self.y1 = y;
		self.x2 = x + w;
		self.y2 = y + h;
		
		self.id = Obstacle.current_obstacle_id;
		Obstacle.current_obstacle_id += 1;
		
		self.fill = "#ff0000";
	
	def set_fill(self, fill):
		self.fill = fill;
		
	def toggle_collisions(self):
		self.collidable = (not self.collidable);
		
	def situate(self, environment):
		self.environment = environment;
		self.shapeTag = ("obstacle%d-shape" % (self.id));

		self.environment.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.fill, width=0, tag=self.shapeTag);