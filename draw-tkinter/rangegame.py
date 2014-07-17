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

agentAmount = 350;
stoppedCount = 0;

radiusToStop = 75.0;
pointToStop  = Vector2D(400, 400);

#Add some agents to this environment
agents = Agentset(environment, agentAmount, outline=False, fill="white", coneFill="#555555");

agents.shuffle();

agents.setvars("stopped", False);

time.clock();

while True:	
	
	for i in range(0, 50):
		#Run through each agent, apply some form of behaviour
		for agent in agents:
			if not agent.getvar("stopped"):
				agent.fd(10);
				agent.random_turn(5);
				
				if agent.distancexy(pointToStop) <= radiusToStop:
					agent.setvar("stopped", True);
					stoppedCount += 1;
					print("[%2d/%2d] Stopped agent %2d at p = (%.3f, %.3f)" % (stoppedCount, agentAmount, agent.id, agent.pos.x, agent.pos.y));
					
				
	if stoppedCount >= agentAmount:
			break;
		
	#Update everyones shapes for redraw
	agents.update_shapes();
	
	#And redraw!
	environment.draw();

print("Took %f CPU seconds to complete (%d agents to stop in radius %.1f of p = (%.2f, %.2f))" % (time.clock(), agentAmount, radiusToStop, pointToStop.x, pointToStop.y));


