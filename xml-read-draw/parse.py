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


#Create an environment
environment = Environment(800, 800);

#Create some patches in the environment
environment.create_patches(24, 24, grid=False, fill="black");

#Add some agents to this environment
agents = Agentset(environment, 25, outline=False, fill="white", coneFill="#555555", coneLength=30);

#agents.order(10, Vector2D(300,300));
agents.shuffle();

def get_average_heading(agent, radius):
	closeAgents = agents.in_radius(agent, radius);
	
	average_heading = 0.0;
	
	for agent in closeAgents:
		average_heading += agent.heading;
	
	if len(closeAgents) != 0:
		return average_heading / len(closeAgents);
	else:
		return -1;

def align(agent):
	average_heading = get_average_heading(agent, 50.0);

	if average_heading == -1:
		agent.random_turn(5);
	else:
		agent.set_heading(average_heading);
	
while True:	

	for i in range(0, 2):
		for agent in agents:
			agent.fd(5);
			align(agent);
		
	#Update everyones shapes for redraw
	agents.update_shapes();
	
	#And redraw!
	environment.draw();


