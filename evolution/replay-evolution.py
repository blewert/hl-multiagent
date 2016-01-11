## replay-evolution.py/pyc
## -- 
## Benjamin Williams <eeu222@bangor.ac.uk>
##

import os;
import configparser;

print("\n[Listing available runs...]");


import math
import random
import time
import sys
import os
import builtins

#Import utility functions for evolution and multiagent library
from multiagent import *
import evolution as e;

def setupEnvironment():
	#Set up an environment to simulate the agents
	e.environment = Environment(600, 600);
	
	#Some other environmental details such as walls
	wallWidth = 20;
	hpZoneHeight = 100;
	hpZoneWidth = 100;

	#A list of obstacles within the environment. Append two walls in the middle of the environment.
	e.obstacles = [];
	e.obstacles.append(Obstacle(e.environment.width / 2 - (wallWidth/2), 0, wallWidth, 250));
	e.obstacles.append(Obstacle(e.environment.width / 2 - (wallWidth/2), e.environment.height - 150, wallWidth, 250));

	#A list of "bases" for each team of agents
	e.hpzones = [];
	e.hpzones.append(Obstacle(50, e.environment.height / 2 - hpZoneHeight / 2, hpZoneWidth, hpZoneHeight));
	e.hpzones.append(Obstacle(e.environment.width - 50 - hpZoneWidth, e.environment.height / 2 - hpZoneHeight / 2, hpZoneWidth, hpZoneHeight));

	#Situate and set up all of the things we just set up.
	[ x.situate(e.environment) for x in e.obstacles ];
	[ x.set_fill("#009900") for x in e.hpzones ];
	[ x.situate(e.environment) for x in e.hpzones ];
	
	#Global variables for environment, agents, hpzones and obstacles (so everyone can access it).
	builtins.environment = e.environment;
	#builtins.agents = e.agents;
	builtins.hpzones = e.hpzones;
	builtins.obstacles = e.obstacles;

def play_attack(num, agent):
	#acts = agent.getvar("attacks");
	#acts[num](agent);
	play_action(num, agent);
	
def play_action(num, agent):
	#0,      1        2           3     4      5       6       7
	#0,      1        2        3      4
	#flee, sflee, flee2b, moveto, wander
	
	#shuffle here
	acts = agent.getvar("actions");
	
	acts[num](agent);

	
def behaviourTree():
	
	while True:	

		next_generation_flag = False;
		
		for agent in e.agents:

			#Global behaviour, death:
			if agent.getvar("health") <= 0:
				teamCount = len([ x for x in e.agents if x.getvar("team") == agent.getvar("team")]) - 1;
				
				#print("*** agent %d was killed." % (agent.id));
				
				if teamCount == 0:
					teamId = agent.getvar("team");
					teamColour = ["red", "blue"][teamId];
					
					#print("*** Team ID %d (%s) with agent %d lost." % (teamId, teamColour, agent.id));
					
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
					#print("[agent %d] refilled hp (%.1f)" % (agent.id, agent.getvar("health")));
			
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
						#print("[agent %d] move to last position" % (agent.id));
						
						if e.health_is_low(agent):
							play_action(2, agent);
							#e.flee_to_base(agent);
						else:
							play_action(3, agent);
							#e.move_to_last_position(agent);
		
					else:
						e.lastFrameData[hash(agent)] = {};
						
						if e.health_is_low(agent):
							#print("[agent %d] flee to base" % (agent.id));
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
								#print("[agent %d] flee" % (agent.id));
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

	#Destroy environment after simulation
	e.environment.destroy();
			
def executeIndividualSimulation(passedAgents):

	#passedAgents just contains the ids for agents in the agents array.
	#..
	
	#Call to setup environment + agents
	setupEnvironment();
	
	#Add some agents to this environment. We need to set up the amount of passed agents.
	e.agents = Agentset(e.environment, len(passedAgents), coneLength=120, outline=False, fill="white", coneFill="#555555");
	
	#Then, call agents_init() - set up team, health, cone and situate randomly in the environment.
	e.agents_init(e.agents);
	builtins.agents = e.agents;
	
	#Set up actions for every agent with the actions spawned for the population
	for (i, agentID) in enumerate(passedAgents):
		e.agents.get(i).setvar("actions", tempPopulation[agentID]);

	# for agent in e.agents:
		# #nactions = sorted(actions, key=lambda k: random.random())
		# agent.setvar("actions", actions);
		
		# nactions = attack_actions;#sorted(attack_actions, key=lambda k: random.random())
		# agent.setvar("attacks", nactions);

	#Call behaviour tree for each agent continously
	behaviourTree();


	
actions = [ 
	e.attack, e.signal_and_attack, e.attack_signalled_agent,
	e.flee, e.signal_and_flee, e.flee_to_base,
	e.move_to_last_position, 
	e.wander 
];

def getTrait(generation, agent_number):
	config = configparser.ConfigParser();
	config.read("results/%d/generations.txt" % runNumber);
		
	return [int(x) for x in config["generation %d" % generation]["agent_%d" % agent_number].split(",")];

def listTraits(generation, verbose):

	sactions = [ 
		"attack", "sig_attack", "attack_sig_agent",
		"flee", "sig_flee", "flee_to_base",
		"move_last_pos", "wander"
	];

	config = configparser.ConfigParser();
	config.read("results/%d/generations.txt" % runNumber);
		
	for v in config["generation %d" % generation]:
		genes = config["generation %d" % generation][v];
		
		if verbose:
			indices = [int(x) for x in genes.split(",")];
			
			print(v);
			print("%s" % ([sactions[x] for x in indices]));
			print("");
			
		else:
			print("Genes of %s\t->\t%s" % (v, config["generation %d" % generation][v]));
					
def listFitness(generation):
	config = configparser.ConfigParser();
	config.read("results/%d/fitnesses.txt" % runNumber);
	
	
	for v in config["generation %d" % generation]:
		print("Fitness of %s\t->\t%s" % (v, config["generation %d" % generation][v]));
	
def printCommands():
	print("\nCommands:");
	print("nagents\t\t\t\t\t- Prints the number of agents used in evolution.");
	print("list fitness <generation>\t\t- Lists all fitnesses for a particular generation.");
	print("list traits <generation>\t\t- Lists all traits/genes for a particular generation.");
	print("list traitsv <generation>\t\t- Same as above, but verbose.");
	print("run <number of players>\t\t\t- Starts a simulation with a number of players.");
	print("gens\t\t\t\t\t- Prints available generations");
	print("cmds\t\t\t\t\t- Prints these commands");
	print("exit\t\t\t\t\t- Quits the application");

def printAvailableGenerations():
	config = configparser.ConfigParser();
	config.read("results/%d/generations.txt" % runNumber);
	print([int(x.replace("generation ", "")) for x in config.sections()]);

runs = [ x[0] for x in os.walk("results") ];
runs = [ x.replace("results\\", "") for x in runs ];

runs = [int(x) for x in runs if x.isdigit()];

if len(runs) == 0:
	print(".. no runs available yet!");
	exit(0);
else:
	print(str(runs).replace("[", "").replace("]", ""));

print("");
runNumber = int(input("Enter a run to use: "));

if runNumber not in runs:
	print("[error] Invalid run number. Exiting..");
	exit(1);


print("\nListing available generations to pick from...");

printAvailableGenerations();

printCommands();


def cmdLoop():
	while True:
		strInput = input("\n> ");
		
		splitStr = strInput.split(" ");
		
		if splitStr[0] == "cmds":
			printCommands();
		
		elif splitStr[0] == "exit":
			exit(0);
		
		elif splitStr[0] == "gens":
			printAvailableGenerations();
			
		elif splitStr[0] == "list":
			if splitStr[1] == "fitness":
				value = int(splitStr[2]);
			
				listFitness(value);
				
			elif splitStr[1] == "traits" or splitStr[1] == "genes":
				value = int(splitStr[2]);
				
				listTraits(value, False);
				
			elif splitStr[1] == "traitsv" or splitStr[1] == "genesv":
				value = int(splitStr[2]);
				
				listTraits(value, True);
				
		elif splitStr[0] == "run":
			numberOfPlayers = int(splitStr[1]);
			return [numberOfPlayers, True];

while True:
	result = cmdLoop();
			
	numberOfPlayers = result[0];
	
	if not result[1]:
		exit(0);

	print("Starting simulation. Players need to be picked.\n");

	tempPopulation = [];
	currentPlayers = 0;

	while currentPlayers < numberOfPlayers:
		team = "red" if currentPlayers % 2 == 0 else "blue";
		
		strInput = input("Player #%d [generation, agent] [%4s]: " % ((currentPlayers + 1), team)).replace(" ", "");

		data = [int(x) for x in strInput.split(",")];
		
		tempPopulation.append(getTrait(data[0], data[1]));
		
		currentPlayers += 1;
		

	tempPopulation = [ list(map(lambda x: actions[x], x)) for x in tempPopulation ];
	
	try:
		executeIndividualSimulation(list(range(0, len(tempPopulation))));
		
	except:
	
		try:
			e.environment.destroy();
			
		except:
			pass;
			
		continue;



