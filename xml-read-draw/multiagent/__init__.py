## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Package inclusion script
##

#Debug bitflag constants
DEBUG_LOG       = 0b001;
DEBUG_SHOW_PATH = DEBUG_LOG << 1;
DEBUG_NONE      = DEBUG_LOG << 2;

#Debug bitflag variable
DEBUG_PACKAGE_BITS = (DEBUG_LOG | DEBUG_SHOW_PATH);

def debug_package_inclusion(package, __class):
	if not (DEBUG_NONE & DEBUG_PACKAGE_BITS):
		if not (DEBUG_SHOW_PATH & DEBUG_PACKAGE_BITS):
			print("Including %s from %s..." % (__class, package));
		else:
			print("Including %s from %s (./%s.py)..." % (__class, package, package));

#Include modules
#..

debug_package_inclusion("util", "VisionCone");
from multiagent.util import VisionCone

debug_package_inclusion("util", "Vector2D");
from multiagent.util import Vector2D

debug_package_inclusion("environment", "Environment");
from multiagent.environment import Environment

debug_package_inclusion("agentset", "Agentset");
from multiagent.agentset import Agentset

debug_package_inclusion("agentset", "AgentsetFromProperties");
from multiagent.agentset import AgentsetFromProperties

debug_package_inclusion("agent", "Agent");
from multiagent.agent import Agent

debug_package_inclusion("patch", "Patch");
from multiagent.patch import Patch

debug_package_inclusion("parse", "Parse");
from multiagent.parse import Parser
