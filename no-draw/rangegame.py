## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Test script for multi-agent system.
##

import random
import time
import sys
import json
from multiagent import *

#Create an environment
environment = Environment(800, 800);

#Create some patches in the environment
environment.create_patches(24, 24, grid=False, fill="black");

agentAmount = 25;
stoppedCount = 0;

radiusToStop = 75.0;
pointToStop  = Vector2D(400, 400);

#Add some agents to this environment
agents = Agentset(environment, agentAmount, outline=False, fill="white", coneFill="#555555");

agents.shuffle();

agents.setvars("stopped", False);

time.clock();

while True:	
	
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

print("Took %f CPU seconds to complete (%d agents to stop in radius %.1f of p = (%.2f, %.2f))" % (time.clock(), agentAmount, radiusToStop, pointToStop.x, pointToStop.y));


agentData = [];

environmentData = {
	"width"  : environment.width,
	"height" : environment.height,
	"originX" : environment.origin.x,
	"originY" : environment.origin.y,
	"wrap" : environment.wrap
};

patchData = [];

print("Taking JSON snapshot for patches...");
for patch in environment.patches:
	patchData.append(
	{
		"posX" : round(patch.pos.x, 5),
		"posY" : round(patch.pos.y, 5),
		"width" : round(patch.width, 5),
		"height" : round(patch.height, 5),
		"fill" : patch.fill,
		"gridOn" : patch.grid
	});
	
print("Snapshot completed.\r\n");

print("Taking JSON snapshot for agents");
for agent in agents:
	agentData.append(
	{
		"hidden" : agent.hidden,
		"heading" : round(agent.heading, 5),
		"posX" : round(agent.pos.x, 5),
		"posY" : round(agent.pos.y, 5),
		"outlined" : agent.outline,
		"fill" : agent.fill,
		"coneLength" : agent.cone.length,
		"coneFill" : agent.cone.fill,
		"coneAngle" : agent.cone.interiorAngle
	});
	
print("Snapshot completed.");
#print(json.JSONEncoder().encode(agentData));

outputData = {
	"environment" : environmentData,
	"patches" : patchData,
	"agents" : agentData
};

fp = open('output.json', 'w+');
fp.write(json.JSONEncoder().encode(outputData));
fp.close();

print("Wrote to output.json.");