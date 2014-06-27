## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Test script for multi-agent system.
##

import random
import time
from multiagent import *

#Create an environment
environment = Environment(800, 800);

#Create some patches in the environment
environment.create_patches(12, 12, grid=False);

#Add some agents to this environment
agents = Agentset(environment, 4, outline=False);

while True:	

	#Run through each patch, if it isn't the default color, make it.
	for patch in environment.patches:
		if patch.fill != Patch.default_fill:
			patch.set_fill(Patch.default_fill);
		
	#Run through each agent, apply some form of behaviour
	for agent in agents:
		agent.fd(1);
		agent.random_turn(5);
		
		patch_on = agent.patch_here();
		patch_on.set_fill("#ff0000");
			
	#Update everyones shapes for redraw
	agents.update_shapes();
	
	#And redraw!
	environment.draw();


