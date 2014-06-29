## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Test script for multi-agent system.
##

import random
import time
import sys
from multiagent import *

#Create an environment
environment = Environment(800, 800);

#Create some patches in the environment
environment.create_patches(24, 24, grid=False, fill="black");

#Add some agents to this environment
agents = Agentset(environment, 15, outline=False, fill="#555555");

for agent in agents:
	agent.set_fill("white");

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

agents.order(10, Vector2D(300,300));

while True:	

	for patch in environment.patches:
		if patch.fill != "#000000" and patch.fill != "black":
			patch.set_fill(decrease(patch.fill));		
			
		
	#Run through each agent, apply some form of behaviour
	for agent in agents:
		agent.fd(10);
		agent.random_turn(5);
		
		patch_here = agent.patch_here();
		patch_here.set_fill("#252525");
			
	#Update everyones shapes for redraw
	agents.update_shapes();
	
	#And redraw!
	environment.draw();


