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

environment.create_patches(10, 10);

agents = Agentset(environment, 3);

while True:	
	agents.update_shapes();

	for patch in environment.patches:
		if patch.fill != Patch.default_fill:
			patch.set_fill(Patch.default_fill);
		
	for agent in agents:
		agent.fd(1);
		agent.random_turn(5);
		
		patch_on = agent.patch_at();
		patch_on.set_fill("#ff0000");
		
		#print("Agent %d is on patch %d" % (agent.id, patchNumber));
		
	
	#And redraw!
	environment.draw();


