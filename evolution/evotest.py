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
environment = Environment(600, 600);

#Add some agents to this environment
agents = Agentset(environment, 2, coneLength=150, outline=False, fill="white", coneFill="#555555");

i = 0;

teamA = [];
teamB = [];

STATE_IDLE = 0;
STATE_SEEK = 1;
STATE_FLEE = 2;

for agent in agents:

	agent.setvar("state", STATE_IDLE);
	agent.setvar("health", 100.0);
	agent.setvar("target", None);

	agent.fd(environment.width / 2);
	agent.rt(90);
	agent.fd(environment.height / 2);
	
	if i % 2 == 0:
		agent.lt(90);
		teamA.append(agent);
		agent.setvar("team", "a");
	else:
		agent.rt(90);
		teamB.append(agent);
		agent.setvar("team", "b");
	
	agent.fd(environment.width / 2 - 50);
	agent.rt(180);
		
	i += 1;

t = 0;

def shoot_agent(shooter, target):
	target.setvar("health", target.getvar("health") - (100.0 / 200));
	print("[shot] agent #%2d (%6f.2 hp) -> agent #%2d (%6f.2 hp)" % (shooter.id, shooter.getvar("health"), target.id, target.getvar("health")));
	
speed = 3.0;
	
def wander(agent):
	agent.random_turn(5);
	agent.fd(speed);
	
while True:	
		
	if len(teamA) == 0 or len(teamB) == 0:
		print("Team A count: %d" % (len(teamA)));
		print("Team B count: %d" % (len(teamB)));
		
		if len(teamA) > len(teamB):
			print("Team A wins");
		else:
			print("Team B wins");
		
		break;
	
	#Run through each agent, apply some form of behaviour 
	for agent in agents:
	
		if agent.getvar("health") < 0.0:
			agents.kill(agent);
			
			if agent in teamA:
				teamA.remove(agent);
				
			elif agent in teamB:
				teamB.remove(agent);
	
		if agent.getvar("state") == STATE_IDLE:
			wander(agent);
			foundAgent = agents.first_in_cone(agent);
			
			if foundAgent != None and foundAgent.getvar("team") != agent.getvar("team"):
				#Swap to SEEK
				if foundAgent.getvar("state") == STATE_SEEK:
					agent.setvar("state", STATE_FLEE);
					agent.setvar("target", foundAgent); 
				else:
					agent.setvar("state", STATE_SEEK);
					agent.setvar("target", foundAgent); 
					agent.heading = foundAgent.heading;
					
				
		
		elif agent.getvar("state") == STATE_FLEE:
			#flee
			agent.random_turn(1);
			agent.fd(speed * 2);
			
			
			if agent.getvar("target") == None or agent.getvar("target").getvar("target") != agent:
				#Out of range, swap to idle:
				agent.setvar("state", STATE_IDLE);
				agent.setvar("target", None);
			
			pass;
		
		elif agent.getvar("state") == STATE_SEEK:
		
			if agent.getvar("target") != None and agent.getvar("target") in agents.in_radius(agent, 250):
				agent.face(agent.getvar("target"));
				agent.fd(speed);
				agent.setvar("timeout", 0);
				
				if agent.getvar("target") in agents.in_radius(agent, 100):
					shoot_agent(agent, agent.getvar("target"));
			else:
				#Out of range, swap to idle
				agent.setvar("state", STATE_IDLE);
				agent.setvar("target", None);
				
	
	#Update everyones shapes for redraw
	agents.update_shapes();
	
	#And redraw!
	environment.draw();



