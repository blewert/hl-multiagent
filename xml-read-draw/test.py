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
environment.create_patches(24, 24, grid=False, fill="#333333");

#Parse test.xml, and parse all agent sets in there
parsedFile = Parser("test.xml");
parsedAgentsets = parsedFile.parse();

#Agentsets list, for agentsets to update.
agentsets = [];

for agentset in parsedAgentsets:	
	#Run through each agentset that was parsed, and create an agentset object from the properties of this agentset (and append!)
	newAgentset = AgentsetFromProperties(environment, agentset["properties"], agentset["behaviour"] if "behaviour" in agentset.keys() else None);
	agentsets.append(newAgentset);


for agentset in agentsets:
	if agentset.shuffle:
		agentset.shuffle();

while True:	

	for agentset in agentsets:
		for agent in agentset:
			if agentset.get_behaviour_type() == "wander":
				agent.random_turn(15);
				
			agent.fd(2);
		
		agentset.update_shapes();
	
	environment.draw();


