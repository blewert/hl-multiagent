## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Agent/turtle class (will expand to encompass agents more generally soon)
##

try:
	import tkinter
except ImportError:
	import Tkinter as tkinter
	
import math
import random

#Import necessarily local files
from .     import environment
from .util import VisionCone
from .util import Vector2D


class Agent:
	#Static variable for agent id, starting at 0, and turtle size in px
	current_agent_id = 0;
	turtle_size      = 7;
	
	def __init__(self, environment=None, x=0, y=0, heading=0, coneInteriorAngle=45, coneLength=50, fill="black", coneFill=VisionCone.default_fill, outline=True):
		#Set position to specified position, same with heading, and make this agent shown by default
		self.pos     = Vector2D(x, y);
		self.heading = heading;
		self.hidden  = False;
		self.outline = outline;
		
		#Generate an ID for this agent, and increment the static agent id by one for uniqueness
		self.id = Agent.current_agent_id;
		Agent.current_agent_id += 1;
		
		#If environment isn't null (is specified), then situate this agent in the environment.
		if environment != None:
			self.situate(environment);
		
		#Generate vision cone data
		self.create_vision_cone(coneInteriorAngle, coneLength);
		
		self.cone.set_fill(coneFill);
		self.set_fill(fill);
		
		#This agent's per-instance variables
		self.vars = {};
	
	def set_fill(self, fill):
		self.environment.canvas.itemconfigure(self.shapeTag, fill=fill);		
		
	def patch_ahead_idx(self, distance, angle=0.0):
		#Calculate x and y using sin/cos, wrap around environment
		calcX = (self.pos.x + math.cos(math.radians(self.heading + angle)) * distance) % self.environment.width;
		calcY = (self.pos.y + math.sin(math.radians(self.heading + angle)) * distance) % self.environment.height;
		
		#Return the patch index located at this position
		return self.patch_at_idx(calcX, calcY);
		
	def patch_ahead(self, distance, angle=0.0):
		#Calculate x and y using sin/cos, wrap around environment
		calcX = (self.pos.x + math.cos(math.radians(self.heading + angle)) * distance) % self.environment.width;
		calcY = (self.pos.y + math.sin(math.radians(self.heading + angle)) * distance) % self.environment.height;
		
		#Return the patch located at this position
		return self.patch_at(calcX, calcY);
		
	def patch_here_idx(self):
		return self.patch_at_idx(self.pos.x, self.pos.y);
		
	def patch_here(self):
		return self.patch_at(self.pos.x, self.pos.y);
		
	def patch_at_idx(self, x, y):
		#Calculate the size of each patch.
		sizeX = (self.environment.width / self.environment.patchamount.x);
		sizeY = (self.environment.height / self.environment.patchamount.y);
		
		#Set x/y to 1 if 0, because 0 weirdly gives negative indices
		safePosX = x if x != 0.0 else 1;
		safePosY = y if y != 0.0 else 1;
		
		#Find out what patch x and y this agent is on, and minus one from it (zero-based indexing)
		calcX = math.ceil(safePosX / sizeX) - 1;
		calcY = math.ceil(safePosY / sizeY) - 1;
		
		#Calculate the stored index of the patch in self.environment.patches (2D -> linear), and return it.
		patchIDX = (self.environment.patchamount.y * calcX) + calcY;
		return patchIDX;
	
	def patch_at(self, x, y):
		return self.environment.patches[int(self.patch_at_idx(x, y)) % len(self.environment.patches)];		
		
	def face(self, agent):
		return self.facexy(agent.pos);
		
	def facexy(self, point=None):
		point = self.environment.origin if point == None else point;
		
		angle = math.degrees(math.atan2(point.y - self.pos.y, point.x - self.pos.x));
		self.set_heading(angle);
		
	def move_to(self, agent):
		self.pos = agent.pos;
		
	def varexists(self, var):
		return (var in self.vars);
	
	def st(self):
		return show();

	def show(self):
		if self.hidden:
			self.hidden = False;	
			self.environment.canvas.itemconfigure(self.cone.tag, state=tkinter.NORMAL);
			self.environment.canvas.itemconfigure(self.shapeTag, state=tkinter.NORMAL);

	def ht(self):
		return hide();
		
	def hide(self):
		if not self.hidden:
			self.hidden = True;
			self.environment.canvas.itemconfigure(self.cone.tag, state=tkinter.HIDDEN);
			self.environment.canvas.itemconfigure(self.shapeTag, state=tkinter.HIDDEN);
		
	def getvar(self, var):
		if var in self.vars:
			return self.vars[var];
		else:
			return None;
	
	def setvar(self, var, value):
		self.vars[var] = value;
	
	def randomx(self):
		self.pos.x = random.uniform(0, self.environment.width) % self.environment.width;
		
	def randomy(self):
		self.pos.y = random.uniform(0, self.environment.height) % self.environment.height;
		
	def randomxy(self):
		self.randomx();
		self.randomy();
		
	def setxy(self, position):
		self.pos = position;
		
	def distance(self, agent):
		return self.distancexy(agent.pos);
			
	def distancexy(self, point):
		#Euclidean distance - firstly find the sum under the sqrt, and return sqrt of this sum
		sum = (point.x - self.pos.x)**2 + (point.y - self.pos.y)**2;
		return math.sqrt(sum);
	
	def create_vision_cone(self, interiorAngle, length, fill=VisionCone.default_fill):
		#Generate cone tag, generate vision cone (and set to local instance), and create cone shape in place
		coneTag = ("turtle%d-cone" % self.id);
		self.cone = VisionCone(interiorAngle, length, self, coneTag, fill=fill);
		
		#If we want an outline, set the outline colour to black, else the same colour as the cone fill.
		if self.outline:
			self.environment.canvas.create_arc(0, 0, 0, 0, fill=fill, tags=self.cone.tag, outline="black");
		else:
			self.environment.canvas.create_arc(0, 0, 0, 0, fill=fill, tags=self.cone.tag, outline=self.cone.fill);
			
	
	def situate(self, environment):
		#Set instance environment to passed one, and generate shape tag (for agent drawing).
		self.environment = environment;
		self.shapeTag = ("turtle%d-shape" % self.id);
		
		#Find the points to/from for the creation of a circle
		ptFrom = Vector2D(self.pos.x - Agent.turtle_size/2, self.pos.y - Agent.turtle_size/2);
		ptTo   = Vector2D(self.pos.x + Agent.turtle_size/2, self.pos.y + Agent.turtle_size/2);
		
		#Create an oval in place of the agent
		self.environment.canvas.create_oval(ptFrom.x, ptFrom.y, ptTo.x, ptTo.y, fill="black", tags=self.shapeTag);
	
	def set_heading(self, heading):
		self.heading = (heading % 360.0);
	
	def random_turn(self, amount):
		return self.lt(random.uniform(-amount, +amount));
			
	def lt(self, amount):
		return self.rt(-amount);
		
	def rt(self, amount):
		self.heading = (self.heading + amount) % 360.0;
		
	def back(self, amount):
		return self.bk(amount);
		
	def bk(self, amount):
		return self.fd(-amount);
		
	def forward(self, amount):
		return self.fd(amount);
		
	def fd(self, amount):
		if not self.environment.wrap:
			self.pos.x = self.pos.x + math.cos(math.radians(self.heading)) * amount;
			self.pos.y = self.pos.y + math.sin(math.radians(self.heading)) * amount;
		else:
			self.pos.x = (self.pos.x + math.cos(math.radians(self.heading)) * amount) % self.environment.width;
			self.pos.y = (self.pos.y + math.sin(math.radians(self.heading)) * amount) % self.environment.height;
		
	def update_shapes(self):
		if self.hidden:
			pass;
		
		self.update_turtle_shape();
		self.update_cone();
		self.environment.canvas.tag_raise(self.shapeTag, self.cone.tag);
		
	def update_cone(self):
		if self.hidden:
			pass;
			
		#Find facing angle by negating heading
		facingAngle = -self.heading;
	
		#Top left, and bottom right coordinate tuples
		topLeft     = (self.pos.x - self.cone.length, self.pos.y - self.cone.length);
		bottomRight = (self.pos.x + self.cone.length, self.pos.y + self.cone.length);
		
		#Set outline to the same colour if we don't want an outline (width=0 doesn't work?)
		outline = self.cone.fill if not self.outline else "black";
		
		#Update starting angle of arc, using facingAngle - (interior / 2)!
		self.environment.canvas.itemconfigure(self.cone.tag, start=(facingAngle - (self.cone.interiorAngle / 2)), extent=self.cone.interiorAngle, outline=outline);
		
		#Relocate arc to this turtle's position
		self.environment.canvas.coords(self.cone.tag, (topLeft[0], topLeft[1], bottomRight[0], bottomRight[1]));
		
	def update_turtle_shape(self):
		if self.hidden:
			pass;
			
		ptFrom = Vector2D(self.pos.x - Agent.turtle_size/2, self.pos.y - Agent.turtle_size/2);
		ptTo   = Vector2D(self.pos.x + Agent.turtle_size/2, self.pos.y + Agent.turtle_size/2);
		
		self.environment.canvas.coords(self.shapeTag, ptFrom.x, ptFrom.y, ptTo.x, ptTo.y);		
		
	def random_heading(self):
		self.heading = random.uniform(0.0, 360.0);
	
