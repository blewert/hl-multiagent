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

environment.create_patches(16, 16);

agents = Agentset(environment, 30);
agents.shuffle();


while True:	
	agents.update_shapes();
	
	for patch in environment.patches:
		patch.set_fill("#ff0000");
		
	for agent in agents:
		agent.random_turn(5);
		agent.fd(3);
		
	#And redraw!
	environment.draw();


