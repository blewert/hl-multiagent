## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Test script for multi-agent system.
##

import math
import random
import time
import sys
from multiagent import *

BEHAVIOUR_WANDER = 0;
BEHAVIOUR_AVOID  = 1;
BEHAVIOUR_SPIRAL = 2;

behaviour = 1;#random.randrange(0, 3);

print("Selected behaviour: %d" % (behaviour));

#Create an environment
environment = Environment(800, 800);

#Create some patches in the environment
environment.create_patches(24, 24, grid=False, fill="black");

#Add some agents to this environment
agents = Agentset(environment, 25, outline=False, fill="white", coneFill="#555555");

def col2int(colour):
	return int(colour[1:], 16);

def int2col(colour):
	strhex = str(hex(colour))[2:];
	
	if len(strhex) < 6:
		for i in range(0, 7 - len(strhex)-1):
			strhex = "0" + strhex;
			
	return ("#%s" % strhex);
    
def decrease(colour):
	color = col2int(colour);
	color -= 0x010101;
    
	return int2col(color);

#agents.order(10, Vector2D(300,300));
agents.shuffle();

while True:	

	for patch in environment.patches:
		if patch.fill != "#000000" and patch.fill != "black":
			patch.set_fill(decrease(patch.fill));		
			
		
	#Run through each agent, apply some form of behaviour
	for agent in agents:
		if agent.cone.fill != "#555555":
			agent.cone.set_fill("#555555");
		
		patch_here = agent.patch_here();
		patch_here.set_fill("#252525");
		
		if behaviour == BEHAVIOUR_WANDER:
			agent.fd(10);
			agent.random_turn(5);
			
		elif behaviour == BEHAVIOUR_AVOID:
			agent.fd(10);
			agent.random_turn(5);
			
			closeAgent = agents.first_in_radius(agent, 150.0);
			
			if closeAgent != None:
				agent.bk(3);
				closeAgent.bk(3);
				
		elif behaviour == BEHAVIOUR_SPIRAL:
			agent.fd(5);
			agent.rt(math.sin(agent.pos.x * 0.01) * 5);
			
	#Update everyones shapes for redraw
	agents.update_shapes();
	
	#And redraw!
	environment.draw();


