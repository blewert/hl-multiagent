## evolution/functions.py
## ======================
## Benjamin Williams <eeu222@bangor.ac.uk>
##

# Note the usage of doxygen style doc comments rather than pydoc here, I
# guess it's a matter of taste. I'm used to javadoc.

import builtins as b

class Vector2D:
	#Like a namedtuple, but mutable (so like recordtype).
	def __init__(self, x, y):
		self.x = x;
		self.y = y;
		
#Thresholds to evolve, the closest distance which is nearby and the hp value which is considered low:
NEARBY_DIST = 100.0;
LOW_HP_THRESHOLD = 50.0;
AGENT_SPEED = 1;
TURN_ANGLE = 5;
HIT_DAMAGE = 0.1;

DIRECTION_LEFT = 0;
DIRECTION_RIGHT = 1;

#Last frame data to check if an agent was seen in the last frame.
lastFrameData = {};

def has_been_signalled(agent):
	return agent.getvar("signalled_agent") != None;

def inside_base(agent, base):
	padding = 10;
	
	if agent.pos.x >= base.x1 + padding and agent.pos.x <= base.x2 - padding:
		if agent.pos.y >= base.y1 + padding and agent.pos.y <= base.y2 - padding:
			return True;
		
	return False;
	
def flee_to_base(agent):
	if not inside_base(agent, b.hpzones[agent.getvar("team")]):
		centreX = (b.hpzones[agent.getvar("team")].x1 + b.hpzones[agent.getvar("team")].x2) / 2;
		centreY = (b.hpzones[agent.getvar("team")].y1 + b.hpzones[agent.getvar("team")].y2) / 2;
		
		agent.facexy(Vector2D(centreX, centreY));
		agent.fd(AGENT_SPEED * 1.5);

def flee(agent):
	#agent.heading = agent.heading - 180;
	agent.fd(AGENT_SPEED * 1.5);
	agent.random_turn(TURN_ANGLE * 2);

## Utility - hits another agent (reduces hp and set flags)
##
def hit_agent(other):
	other.setvar("health", other.getvar("health") - HIT_DAMAGE);
	other.setvar("underfire", True);

	other.setvar("damage_taken", other.getvar("damage_taken") + HIT_DAMAGE);	

def signal(agent, other):
	teammates = [ x for x in b.agents if x != agent and x.getvar("team") == agent.getvar("team") and agent.distance(x) < NEARBY_DIST ];
	
	if len(teammates) > 0:
		for teammate in teammates:
			teammate.setvar("signalled_agent", other);
	
def signal_and_flee(agent):
	other = get_closest_agent(agent);
	
	if other != None:
		signal(agent, other);
		
	flee(agent);

def signal_and_attack(agent):
	other = get_closest_agent(agent);
	
	if other != None:
		signal(agent, other);
		
	attack(agent);

def attack_signalled_agent(agent):
	other = agent.getvar("signalled_agent");
	
	if other == None:
		agent.fd(AGENT_SPEED);
		return;
		
	agent.face(other);
	
	if agent.distance(other) > 5:
		agent.fd(AGENT_SPEED);
	
	agent.setvar("damage_given", other.getvar("damage_given") + HIT_DAMAGE);
	
	for a in b.agents:
		if a.getvar("team") == agent.getvar("team"):
			a.setvar("other_team_damage", a.getvar("other_team_damage") + HIT_DAMAGE);
			
		else:
			a.setvar("team_damage", a.getvar("team_damage") + HIT_DAMAGE);
			
	#print("[agent %d] attack agent %d (%3.1f hp)" % (agent.id, other.id, other.getvar("health")));
	hit_agent(other);
	
## Attacks another agent
##
def attack(agent):
	other = get_closest_agent(agent);
	
	if other == None:
		agent.fd(AGENT_SPEED);
		return;
		
	agent.face(other);
	
	if agent.distance(other) > 5:
		agent.fd(AGENT_SPEED);
	
	agent.setvar("damage_given", agent.getvar("damage_given") + HIT_DAMAGE);	
	
	for a in b.agents:
		if a.getvar("team") == agent.getvar("team"):
			a.setvar("other_team_damage", a.getvar("other_team_damage") + HIT_DAMAGE);
			
		else:
			a.setvar("team_damage", a.getvar("team_damage") + HIT_DAMAGE);
	
	#print("[agent %d] attack agent %d (%3.1f hp)" % (agent.id, other.id, other.getvar("health")));
	hit_agent(other);
	

## Moves an agent to the last position of a seen enemy.
##
def move_to_last_position(agent):
	lastFramePos = seen_in_last_frame(agent);
	
	if lastFramePos != None:
		agent.facexy(lastFramePos);
		agent.fd(AGENT_SPEED);
		
	lastFrameData[hash(agent)] = {};
	
## Initializes all the agents in an agent set.
##
def agents_init(agents):

	#Used for deciding which teamid the agent gets.
	i = 0;

	for agent in agents:
		
		#Set up the initial per-agent vars
		agent.setvar("team", i % 2);
		agent.setvar("health", 100.0);
		agent.setvar("underfire", False);
		agent.setvar("signalled_agent", None);
		
		agent.setvar("damage_given", 0.0);
		agent.setvar("damage_taken", 0.0);
		
		agent.setvar("team_damage", 0.0);
		agent.setvar("other_team_damage", 0.0);
		
		if i % 2 == 0:
			agent.cone.set_fill("#ff0000");
		else:
			agent.cone.set_fill("#0000ff");
			
		#Situate randomly and increase teamid by 1
		agent.randomxy();
		agent.random_heading();
		i += 1;


		
## Checks if any agents were seen in the last frame for a particular agent.
##
def seen_in_last_frame(agent):

	#If the agent is in the last frame data object:
	if hash(agent) in lastFrameData:
	
		#And the closest position has been registered (its not blank), then return the pos
		if "closestPos" in lastFrameData[hash(agent)]:
			return lastFrameData[hash(agent)]["closestPos"];
	
	#Otherwise return none.
	return None;

def get_closest_agent(agent):
	nagents = get_seen_opponents(agent);
	
	if nagents != None:
		return closest_agent(nagents, agent.pos);
	else:
		return None;

## Gets the closest agent to a particular point. This is a utility method.
##
def closest_agent(agents, point):

	#Set the distance as something huge so the first agent satisfies this constantly
	closestDist = 99999;
	closest = None;
	
	#Run through each agent:
	for agent in agents:
		
		#If the distance from this agent to the point is closer, set it to the new closest:
		if agent.distancexy(point) < closestDist:
			closestDist = agent.distancexy(point);
			closest = agent;
	
	#And finally return the closest. None if not found.
	return closest;
	
## Checks if an agent has seen an opponent in it's vision cone.
##
def get_seen_opponents(agent):

	#Find some agents inside the agent's vision cone
	closeAgents = b.agents.in_cone(agent);
	
	#If there agents in the cone:
	if closeAgents != None:
		
		#Get the agents which are not in the same team as this agent.
		closeAgents = [ a for a in closeAgents if a.getvar("team") != agent.getvar("team") ];
		
		#If there are still agents here then return them:
		if len(closeAgents) > 0:
			return closeAgents;
		else:
			return None;
	
	#Otherwise there were no agents in the cone
	return None;
	
## Checks if an agent has seen an opponent in it's vision cone.
##
def opponent_seen(agent):

	#Find some agents inside the agent's vision cone
	return get_seen_opponents(agent) != None;
	
	
## Checks whether or not an agent is currently under fire.
##
def under_fire(agent):
	return agent.getvar("underfire") != False;
	

## Allows the agent to wander.
##
def wander(agent):
	agent.random_turn(TURN_ANGLE);
	agent.fd(AGENT_SPEED);

	
## Gets whether or not there are teammates nearby to an agent.
##
def teammates_nearby(agent):

	#Get all agents nearby, with the same team which is the same as this agent.
	nagents = [ x for x in b.agents if x.distancexy(agent.pos) < NEARBY_DIST and x.getvar("team") == agent.getvar("team") and agent != x ];
	
	#Return the agents, otherwise just return false.
	return len(nagents) > 0;

## Gets whether or not there are enemies nearby to an agent.
##		
def enemy_teammates_nearby(agent):

	#Get all agents nearby, with the same team which is not the same as this agent.
	nagents = [ x for x in b.agents if x.distancexy(agent.pos) < NEARBY_DIST and x.getvar("team") != agent.getvar("team") and agent != x ];
	
	#Return the agents, otherwise just return false.
	return len(nagents) > 0;

## Checks whether or not the health is low for a specific agent.
##
def health_is_low(agent):
	return agent.getvar("health") < LOW_HP_THRESHOLD;