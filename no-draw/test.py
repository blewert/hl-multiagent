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
environment.create_patches(24, 24, grid=False);

#Add some agents to this environment
agents = Agentset(environment, 1);

agents.shuffle();

iter = 0;
while True:	
	for agent in agents:
		agent.fd(1);
		
		iter += 1;
		
		if iter >= 1000:
			print("Agent %d: p = (%f, %f)" % (agent.id, agent.pos.x, agent.pos.y));
			iter = 0;
		

