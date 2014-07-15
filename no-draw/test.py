## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Test script for multi-agent system.
##

from mpi4py import MPI
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

size = MPI.COMM_WORLD.Get_size();
rank = MPI.COMM_WORLD.Get_rank();

iter = 0;
iiter = 0;

while True:	
	for agent in agents:
		agent.random_turn(15);
		agent.fd(1);
		
		iter += 1;
		
		if iter >= 1000:
			print("[rank: %d, iter: %d] Agent %d: p = (%f, %f), r = (%f)" % (rank, iiter*iter, agent.id, agent.pos.x, agent.pos.y, agent.heading));
			iter = 0;
			iiter += 1;

		if iiter >= 20:
			exit(0);
		

