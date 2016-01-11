## replay-evolution.py/pyc
## -- 
## Benjamin Williams <eeu222@bangor.ac.uk>
##

import os;
import configparser;

print("\n[Listing available runs...]");

def getTrait(generation, agent_number):
	config = configparser.ConfigParser();
	config.read("results/%d/generations.txt" % runNumber);
		
	return [int(x) for x in config["generation %d" % generation]["agent_%d" % agent_number].split(",")];

def listTraits(generation, verbose):

	actions = [ 
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
			print("%s" % ([actions[x] for x in indices]));
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

runFlag = False;
numberOfPlayers = 0;

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
		runFlag = True;
		break;
		
if not runFlag:
	exit(0);
	
print("Starting simulation. Players need to be picked.\n");

tempPopulation = [];
currentPlayers = 0;

while currentPlayers < numberOfPlayers:
	strInput = input("Player #%d [generation, agent]: " % (currentPlayers + 1)).replace(" ", "");

	data = [int(x) for x in strInput.split(",")];
	
	tempPopulation.append(getTrait(data[0], data[1]));
	
	currentPlayers += 1;
	
print(tempPopulation);