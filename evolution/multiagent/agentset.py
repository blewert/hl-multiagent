## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Agentset class, for groups of agents.
##

import math
from .agent import Agent
from .util  import VisionCone
from .util  import Vector2D

class Agentset:
	def __init__(self, environment, amount, heading=0, coneInteriorAngle=45, coneLength=50, fill="black", coneFill=VisionCone.default_fill, outline=False):
		self.agents = [];
		self.environment = environment;
		
		for i in range(amount):
			newAgent = Agent(environment, heading=heading,
											coneInteriorAngle=coneInteriorAngle,
											coneLength=coneLength,
											fill=fill,
											coneFill=coneFill,
											outline=outline);
											
			self.agents.append(newAgent);
	
	def create_agents(self, amount, x=0, y=0, heading=0, shuffle=False, coneInteriorAngle=45, coneLength=50, fill="black", coneFill=VisionCone.default_fill, outline=False):
		for i in range(amount):
			newAgent = Agent(self.environment, heading=heading,
											coneInteriorAngle=coneInteriorAngle,
											coneLength=coneLength,
											fill=fill,
											coneFill=coneFill,
											outline=outline);
			if shuffle:
				newAgent.randomxy();
											
			self.agents.append(newAgent);
			
	def __iter__(self):
		return iter(self.agents);
		
	def next(self):
		return self.agents.next();

	def setvars(self, var, value):
		for agent in self.agents:
			agent.setvar(var, value);
	
	def order(self, radius, point=None):
		#Set point to origin point if it's not specified
		point = self.environment.origin if point == None else point;
		
		#Find the amount of agents in this set
		amount = len(self.agents);
		
		#The angle offset whilst ordering, start at 0 and increment by 360.0/amount
		currentAngle = 0.0;
		
		for agent in self.agents:
			#Calculate offset x and y
			calcX = point.x + math.cos(math.radians(currentAngle)) * radius;
			calcY = point.y + math.sin(math.radians(currentAngle)) * radius;
		
			#Set this agent's position to the calculated one, and their heading to the current angle
			agent.pos = Vector2D(calcX, calcY)
			agent.set_heading(currentAngle);
			
			#Increment current angle
			currentAngle += (360.0 / amount);
	
	def randomize(self):
		return self.shuffle();
		
	def shuffle(self):
		for agent in self.agents:
			agent.randomxy();
	
	def kill(self, agent):
		self.environment.canvas.delete(agent.shapeTag);
		self.environment.canvas.delete(agent.cone.tag);
		self.agents.remove(agent);
	
	def update_shapes(self):
		for agent in self.agents:
			agent.update_shapes();
	
	def first_in_cone(self, agent):
		relativeAngleStart = agent.heading - (agent.cone.interiorAngle/2);
		relativeAngleEnd   = agent.heading + (agent.cone.interiorAngle/2);
		
		#First point is turtle itself
		p1 = Vector2D(agent.pos.x, agent.pos.y);
		
		#The second point of the triangle is the left end point of the cone
		p2 = Vector2D(
			agent.pos.x + math.cos(math.radians(relativeAngleStart)) * (agent.cone.length) + 5.0,
			agent.pos.y + math.sin(math.radians(relativeAngleStart)) * (agent.cone.length) + 5.0,
		);
		
		#The third point of the triangle is the right end point of the cone
		p3 = Vector2D(
			agent.pos.x + math.cos(math.radians(relativeAngleEnd)) * (agent.cone.length) + 5.0,
			agent.pos.y + math.sin(math.radians(relativeAngleEnd)) * (agent.cone.length) + 5.0
		);
	
		for iagent in self.agents:
			if iagent == agent:
				continue;
		
			p = Vector2D(iagent.pos.x, iagent.pos.y);
			
			#Find barycentric coordinates, solving for a, b and c
			denom = (p1.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y);
			a = ((p2.y - p3.y) * (p.x - p3.x) + (p3.x - p2.x) * (p.y - p3.y)) / denom;
			b = ((p3.y - p1.y) * (p.x - p3.x) + (p1.x - p3.x) * (p.y - p3.y)) / denom;
			c = 1.0 - a - b;
			
			#Check if a, b and c are normalized
			aNormalized = (0 <= a <= 1);
			bNormalized = (0 <= b <= 1);
			cNormalized = (0 <= c <= 1);
			
			#If they're all normalized, then we've found a collision point: append agent to returnAgents
			if aNormalized and bNormalized and cNormalized:
				return iagent;
		
		return None;

		
	def first_in_radius(self, agent, radius):
		for iagent in self.agents:
			if iagent == agent:
				continue;
			
			if iagent.distance(agent) <= radius:
				return iagent;
		
		return None;
	
	def in_radius(self, agent, radius):
		#List for return agents
		returnAgents = [];
		
		for iagent in self.agents:
			#Same agent? If so, skip
			if iagent == agent:
				continue;
		
			#In radius? If so, append 
			if iagent.distance(agent) <= radius:
				returnAgents.append(iagent);

		return returnAgents;
	
	def in_cone(self, agent):
		relativeAngleStart = agent.heading - (agent.cone.interiorAngle/2);
		relativeAngleEnd   = agent.heading + (agent.cone.interiorAngle/2);
		
		#First point is turtle itself
		p1 = Vector2D(agent.pos.x, agent.pos.y);
		
		#The second point of the triangle is the left end point of the cone
		p2 = Vector2D(
			agent.pos.x + math.cos(math.radians(relativeAngleStart)) * (agent.cone.length) + 5.0,
			agent.pos.y + math.sin(math.radians(relativeAngleStart)) * (agent.cone.length) + 5.0,
		);
		
		#The third point of the triangle is the right end point of the cone
		p3 = Vector2D(
			agent.pos.x + math.cos(math.radians(relativeAngleEnd)) * (agent.cone.length) + 5.0,
			agent.pos.y + math.sin(math.radians(relativeAngleEnd)) * (agent.cone.length) + 5.0
		);
		
		returnAgents = [];
		
		for iagent in self.agents:
			if iagent == agent:
				continue;
		
			p = Vector2D(iagent.pos.x, iagent.pos.y);
			
			#Find barycentric coordinates, solving for a, b and c
			denom = (p1.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y);
			a = ((p2.y - p3.y) * (p.x - p3.x) + (p3.x - p2.x) * (p.y - p3.y)) / denom;
			b = ((p3.y - p1.y) * (p.x - p3.x) + (p1.x - p3.x) * (p.y - p3.y)) / denom;
			c = 1.0 - a - b;
			
			#Check if a, b and c are normalized
			aNormalized = (0 <= a <= 1);
			bNormalized = (0 <= b <= 1);
			cNormalized = (0 <= c <= 1);
			
			#If they're all normalized, then we've found a collision point: append agent to returnAgents
			if aNormalized and bNormalized and cNormalized:
				returnAgents.append(iagent);
			
		return returnAgents;