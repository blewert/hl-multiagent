## ./behaviourtree.py
## ======================
## Benjamin Williams <eeu222@bangor.ac.uk>
##

import math
import random
import time
import sys
import os
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



if "--help" in sys.argv:
	print("[required flags]");
	print("{");
	
	print("\t--amount [uint]\t\tThe population size");
	print("\t--gens [uint]\t\tThe amount of generations to run for");
	print("\t--max-ticks [uint]\tThe max number of epochs to run for each simulation");
	print("\t--split [uint]\t\tThe two-fold split in each chromosome during crossover");
	print("\t--mutation [uint]\tThe mutation chance (0 .. 1)");
	print("\t--team-size [uint]\tThe team size");
	
	print("}");
	
	exit(1);

extract_cmd_args();

TEAM_SIZE             = int(args["team-size"]);
AMOUNT_OF_AGENTS      = int(args["amount"]);
NUMBER_OF_GENERATIONS = int(args["gens"]);
MAX_TICKS             = int(args["max-ticks"]);
SPLIT_POS             = int(args["split"]);
MUTATION_CHANCE       = float(args["mutation"]);

if AMOUNT_OF_AGENTS % TEAM_SIZE != 0:
	print("[error] Invalid amount of agents: " + AMOUNT_OF_AGENTS + " not divisible by " + TEAM_SIZE);
	exit(1);

population = [ ]; #index = agent id, data = actions
fitness    = [ ];

actions = [ 
	e.attack, e.signal_and_attack, e.attack_signalled_agent,
	e.flee, e.signal_and_flee, e.flee_to_base,
	e.move_to_last_position, 
	e.wander 
];

attack_actions = [
	e.attack, e.signal_and_attack, e.attack_signalled_agent
];

resultFolder = "";

def runSimulation(numberOfGenerations):

	# Run through each number of specified generations.
	for i in range(0, numberOfGenerations):
	
		print("Running generation [%d/%d]" % (i+1, numberOfGenerations));
		print("{");
		
		# Then, run through every pair of agents in the population. Execute
		# a simulation involving just these two agents.
		for j in range(0, len(population), TEAM_SIZE):
			agents = list(range(j, j + TEAM_SIZE));
			print("\t[selection] Running simulation for agents %s." % agents);
			executeIndividualSimulation(agents);
			
		print("\n\tEvolving this generation...");
		evolution(i+1);
		
		print("}\n");

def makeDirectories():
	global resultFolder

	if not os.path.exists("results"):
		os.makedirs("results");

	dirs = [ x[0] for x in os.walk("results") ];
	dirs  = [ x.replace("results\\", "") for x in dirs ];
	idirs = [ int(x) for x in dirs if x.isdigit() ];
	idirs.sort();

	print(dirs);
	print(len(idirs));
	
	if len(idirs) > 0:
		resultFolder = ("results/%d/" % (idirs[-1] + 1));
	else:
		resultFolder = "results/1/";
		
	os.makedirs(resultFolder);
	
def init():

	#Initialise the list of actions for each agent
	#..
	
	makeDirectories();
	
	#Run through each agent in the population
	for agent in range(0, AMOUNT_OF_AGENTS):
	
		#Set their actions to be random initially
		randActions = [actions[random.randrange(0, len(actions))] for i in range(0, len(actions))];
		population.append(randActions)
		fitness.append(0);
			
	with open("%sgenerations.txt" % resultFolder, "a+") as f:
		f.write("[generation 0]\n");		
		for (i, agent) in enumerate(population):
			f.write("agent_%d = %s\n" % (i, str([actions.index(x) for x in agent]).replace("[", "").replace("]", "") ));
			
		f.write("\n");
		
	print("Running simulation with %d agents for %d generations..." % (AMOUNT_OF_AGENTS, NUMBER_OF_GENERATIONS));
	
	#And run the simulation
	runSimulation(NUMBER_OF_GENERATIONS);
	

def setupEnvironment(passedAgents):
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
		
def behaviourTree():
	
	ticks = 0;
	
	while True:	
		
		ticks += 1;
		
		if ticks >= MAX_TICKS:
			print("\tTicks have exceeded limit (%d).. aborting." % MAX_TICKS);
			break;
			
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
	setupEnvironment(passedAgents);
	
	#Add some agents to this environment. We need to set up the amount of passed agents.
	e.agents = Agentset(e.environment, len(passedAgents), coneLength=120, outline=False, fill="white", coneFill="#555555");
	
	#Then, call agents_init() - set up team, health, cone and situate randomly in the environment.
	e.agents_init(e.agents);
	builtins.agents = e.agents;
	
	#Set up actions for every agent with the actions spawned for the population
	for (i, agentID) in enumerate(passedAgents):
		e.agents.get(i).setvar("actions", population[agentID]);

	# for agent in e.agents:
		# #nactions = sorted(actions, key=lambda k: random.random())
		# agent.setvar("actions", actions);
		
		# nactions = attack_actions;#sorted(attack_actions, key=lambda k: random.random())
		# agent.setvar("attacks", nactions);

	#Call behaviour tree for each agent continously
	behaviourTree();
	
	#Evaluate the fitnesses for these two agents.
	evaluateFitnesses(e.agents, passedAgents);

def evaluateFitnesses(agents, passedIDs):

	global fitness
	
	i = 0;
		
	for agent in agents:
		
		#fitness[passedIDs[i]] = (agent.getvar("damage_given") + 1) / (agent.getvar("damage_taken") + 1) - 1;
		#fitness[passedIDs[i]] = agent.getvar("other_team_damage");
		#(given_damage / own_damage) + (other_team_damage / team_damage)
		damage_given = agent.getvar("damage_given") + 1;
		damage_taken = agent.getvar("damage_taken") + 1;
		team_damage  = agent.getvar("team_damage") + 1;
		other_team_damage = agent.getvar("other_team_damage") + 1;
		
		fitness[passedIDs[i]] = (damage_given / damage_taken) + (other_team_damage / team_damage) - 2.0;
		
		i += 1;
		
	#Normalize fitnesses (for negative values)
	minValue = min(fitness);
	
	if minValue < 0:
		fitness = [x + -minValue for x in fitness];
		
def breed(parentA, parentB, split = -1):
    # Given 2 inputs (parents), we need 4 (2 ^ 2) children with traits:
    # AB, AA, BA, BB
    # but to promote diversity only use where AB or BA
    
    # Parents must be the same size or no split can occur
    assert len(parentA) == len(parentB);
    
    # Is the split-point (the pivot) out of range?
    assert split > 0 and split < len(parentA);
    
    # Return first half of A with second half of B, and first half of B with 
    # second half of B
    return [
        parentA[:split] + parentB[split:],
        parentB[:split] + parentA[split:]
    ];	
    
def roulette_select(population, fitnesses, num):

    #Sum the individual fitnesses
	total_fitness = float(sum(fitnesses));
    
	if total_fitness == 0:
		total_fitness = len(fitnesses);
		
    #Calculate relative fitness for each fitness
	rel_fitness = [f / total_fitness for f in fitnesses];
	
    #Generate probability intervals for each individual
	probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))];
    
    #Draw new population
	new_population = [];
    
	for n in range(num):
        
        #Generate a random number
		r = random.random();
        
		for (i, individual) in enumerate(population):
            
            #Run through each member in the population. If the random
            #number is less than the probability interval at this point, add this member to the population
			if r <= probs[i]:
				new_population.append(individual)
				break
           
	#New children (for crossover)
	new_children = [];
    
	for i in range(0, len(new_population), 2):
	
		#Run through every pair of members of the population. Breed these two and produce children.
		children = breed(new_population[0], new_population[1], SPLIT_POS);
		
		#Append these children to the list of new children
		new_children.append(children[0]);
		new_children.append(children[1]);
    
	#And return the children
	return new_children
	
def evolution(epoch):

	global population
	global fitness
		
	offspring = [];
	
	fitnessSum     = 0;
	probabilitySum = 0;
	
	for i in range(0, len(fitness)):
		print("\t[fitness] Agent %d: %f" % (i, fitness[i]));
	
	with open("%sfitnesses.txt" % resultFolder, "a+") as f:
		f.write("[generation %d]\n" % (epoch-1));		
		for i in range(0, len(fitness)):
			f.write("agent_%d = %f\n" % (i, fitness[i]));
			
		f.write("\n");
		
	population = roulette_select(population, fitness, len(population));

	#Run through each member in the population
	for (j, agent) in enumerate(population):
	
		#Run through every action for this member
		for (i, action) in enumerate(agent):
		
			#If this gene gets randomly selected for mutation, then:
			if random.random() <= MUTATION_CHANCE:
			
				#Just select a random action and set this gene to this random action
				choice = random.choice(actions);
				print("\tGene #%d of agent #%d mutated: %s to %s" % (i, j, agent[i].__name__, choice.__name__));
				population[j][i] = random.choice(actions);
	
	with open("%sgenerations.txt" % resultFolder, "a+") as f:
		f.write("[generation %d]\n" % epoch);		
		for (i, agent) in enumerate(population):
			f.write("agent_%d = %s\n" % (i, str([actions.index(x) for x in agent]).replace("[", "").replace("]", "") ));
			
		f.write("\n");
			
	#Print out the new population
	print("\n\tNew population");
	for (i, agent) in enumerate(population):
		print("\t[agent #%d] %s" % (i, [actions.index(x) for x in agent]));
				
	
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

#Call init()
init();

