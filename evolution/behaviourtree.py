## ./behaviourtree.py
## ======================
## Benjamin Williams <eeu222@bangor.ac.uk>
##

import math
import random
import time
import sys
import builtins

#Import utility functions for evolution and multiagent library
from multiagent import *
import evolution as e;


import sys;

args = {};

def extract_cmd_args():
	if len(sys.argv) > 1:

		i = 0;
		
		for arg in sys.argv:
			if arg.startswith("--"):
				
				if i+1 > len(sys.argv) - 1:
					print("[invalid arg] I expected a value for key '%s'." % arg);
					exit(1);
				
				elif not sys.argv[i+1].startswith("--"):
					args[arg[2:]] = sys.argv[i+1];
				
			i += 1;
	else:
		print("[error] I expected > 1 arguments.");
		exit(1);

extract_cmd_args();

print(args);

AMOUNT_OF_AGENTS = int(args["team-size"]) * 2;


def play_attack(num, agent):
	acts = agent.getvar("attacks");

	acts[num](agent);
	
def play_action(num, agent):
	#0,      1        2           3     4      5       6       7
	#0,      1        2        3      4
	#flee, sflee, flee2b, moveto, wander
	
	#shuffle here
	acts = agent.getvar("actions");
	
	acts[num](agent);
		
for i in range(1, 3):
	#Create an environment
	e.environment = Environment(600, 600);

	wallWidth = 20;
	hpZoneHeight = 100;
	hpZoneWidth = 100;

	e.obstacles = [];

	e.obstacles.append(Obstacle(e.environment.width / 2 - (wallWidth/2), 0, wallWidth, 250));
	e.obstacles.append(Obstacle(e.environment.width / 2 - (wallWidth/2), e.environment.height - 150, wallWidth, 250));

	e.hpzones = [];

	e.hpzones.append(Obstacle(50, e.environment.height / 2 - hpZoneHeight / 2, hpZoneWidth, hpZoneHeight));
	e.hpzones.append(Obstacle(e.environment.width - 50 - hpZoneWidth, e.environment.height / 2 - hpZoneHeight / 2, hpZoneWidth, hpZoneHeight));

	[ x.situate(e.environment) for x in e.obstacles ];
	[ x.set_fill("#009900") for x in e.hpzones ];
	[ x.situate(e.environment) for x in e.hpzones ];

	#Add some agents to this environment
	e.agents = Agentset(e.environment, AMOUNT_OF_AGENTS, coneLength=120, outline=False, fill="white", coneFill="#555555");
	e.agents_init(e.agents);

	builtins.environment = e.environment;
	builtins.agents = e.agents;
	builtins.hpzones = e.hpzones;
	builtins.obstacles = e.obstacles;

	actions = [ 
		#e.attack, e.signal_and_attack, e.attack_signalled_agent,
		e.flee, e.signal_and_flee, e.flee_to_base,
		e.move_to_last_position, 
		e.wander 
	];

	attack_actions = [
		e.attack, e.signal_and_attack, e.attack_signalled_agent
	];

	for agent in e.agents:
		#nactions = sorted(actions, key=lambda k: random.random())
		agent.setvar("actions", actions);
		
		nactions = attack_actions;#sorted(attack_actions, key=lambda k: random.random())
		agent.setvar("attacks", nactions);

	while True:	
		
		next_generation_flag = False;
		
		for agent in e.agents:
		
			#Global behaviour, death:
			if agent.getvar("health") <= 0:
				teamCount = len([ x for x in e.agents if x.getvar("team") == agent.getvar("team")]) - 1;
				
				print("*** agent %d was killed." % (agent.id));
				
				if teamCount == 0:
					teamId = agent.getvar("team");
					teamColour = ["red", "blue"][teamId];
					
					print("*** Team ID %d (%s) with agent %d lost." % (teamId, teamColour, agent.id));
					
					#exit(0);
					next_generation_flag = True;
					break;
				
				for a in agents:
					if a.getvar("signalled_agent") == agent:
						a.setvar("signalled_agent", None);
				
				e.agents.kill(agent);
			
			#Global behaviour, healing:
			if e.inside_base(agent, e.hpzones[agent.getvar("team")]):
				newHealth = agent.getvar("health") + e.HIT_DAMAGE / 2;
				
				if newHealth > 100:
					agent.setvar("health", 100);
				else:
					agent.setvar("health", newHealth);
					print("[agent %d] refilled hp (%.1f)" % (agent.id, agent.getvar("health")));
			
			#Global behaviour, avoidance:
			if agent.raycast_obstacles(e.obstacles, 100):
				if agent.getvar("direction") == None:
					agent.setvar("direction", e.DIRECTION_RIGHT);
					agent.setvar("signalled_agent", None);
				else:
					agent.rt(2);
				
				#continue;
			else:
				#agent.setvar("avoid_attempts", 0);
				agent.setvar("direction", None);
				
			
			if e.under_fire(agent):
			
				if not e.opponent_seen(agent):
					#We've not seen some enemies.
					
					if e.seen_in_last_frame(agent) != None:
						#An agent was seen in the last frame. Move to that position:					
						print("[agent %d] move to last position" % (agent.id));
						
						if e.health_is_low(agent):
							play_action(2, agent);
							#e.flee_to_base(agent);
						else:
							play_action(3, agent);
							#e.move_to_last_position(agent);
		
					else:
						e.lastFrameData[hash(agent)] = {};
						
						if e.health_is_low(agent):
							print("[agent %d] flee to base" % (agent.id));
							play_action(2, agent);
							#e.flee_to_base(agent);
						else:
							#print("wander");
							play_action(4, agent);
							#e.wander(agent);
						
					agent.setvar("underfire", False);
					
				else:

					#We have found some agents. Collect last frame data.
					closestAgent = e.closest_agent(e.get_seen_opponents(agent), agent.pos);
				
					e.lastFrameData[hash(agent)] = {
						"oldClosest" : closestAgent,
						"closest" : closestAgent,
						"closestPos" : closestAgent.pos
					};		

					if e.teammates_nearby(agent):

						#There are teammates near to this agent. So:
						
						if e.health_is_low(agent):
							play_action(1, agent);
							#e.signal_and_flee(agent);
							pass;
						else:
							play_attack(1, agent);
							#e.signal_and_attack(agent);
							pass;
							
					else:
						#There are no teammates nearby.
						if e.health_is_low(agent):
							play_action(0, agent);
							#e.flee(agent);
							pass;
						else:
							if e.enemy_teammates_nearby(agent):
								print("[agent %d] flee" % (agent.id));
								play_action(0, agent);
								#e.flee(agent);
								pass;
							else:
								play_attack(0, agent);
								#e.attack(agent);
								pass;
			else:
				#Not under fire
				
				#closeAgents = e.opponent_seen(agent, e.agents);
				
				if not e.opponent_seen(agent):
					#Opponents not seen
					if e.has_been_signalled(agent):
						if e.health_is_low(agent):
							play_action(0, agent);
							#e.flee(agent);
						else:
							play_attack(2, agent);
							#e.attack_signalled_agent(agent);
					else:
						if e.health_is_low(agent):
							play_action(2, agent);
							#e.flee_to_base(agent);
						else:
							play_action(4, agent);
							#e.wander(agent);
				else:
					#Opponents seen
					#closestAgent = e.closest_agent(closeAgents, agent.pos);
					
					#print("agents have been seen");
					
					if e.teammates_nearby(agent):
						#Teammates nearby
						if e.health_is_low(agent):
							play_action(1, agent);
							#e.signal_and_flee(agent);
						else:
							play_attack(1, agent);
							#e.signal_and_attack(agent);
					else:
						if e.health_is_low(agent):
							play_action(0, agent);
							#e.flee(agent);
						else:
							if e.enemy_teammates_nearby(agent):
								#print("teammates are not nearby, health is not low, flee");	
								play_action(0, agent);
								#e.flee(agent);
							else:
								#print("teammates are not nearby, health is not low, attack");	
								play_attack(0, agent);
								#e.attack(agent);
						
						
						
						
		#lastFrameData = {};
					
		
		#Update everyones shapes for redraw
		e.agents.update_shapes();
		
		#And redraw!
		e.environment.draw();

		if next_generation_flag:
			e.environment.destroy();
			break;


