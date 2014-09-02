## Benjamin Williams <eeu222@bangor.ac.uk>
## Horde Labs
## ---
## Parsing class, for use of parsing XML files.
##

import xml.etree.ElementTree as ET

class Parser:
	
	def __init__(self, file):
		self.file = file;
		self.xmlTree = ET.parse(self.file);
		self.root = self.xmlTree.getroot();
	
	def parse(self):
			
		#If our root element isn't an environment, die!
		if self.root.tag != "Environment":
			return False;
		
		#Return agents and agentsets
		agents    = [];
		agentsets = [];
		
		for child in self.root:
		
			#We've found an agentset. Parsey parsey!
			if child.tag == "Agentset":
				agentsets.append(self.parseAgentset(child));
		
		return agentsets;
		
	def parseAgentsetProps(self, propertiesNode):
		returnProps = {};
		
		for property in propertiesNode:
			if property.tag != "Property":
				continue;
				
			for attribute in property.attrib:
				if attribute == "tag":
					returnProps[property.attrib[attribute]] = property.text;
		
		return returnProps;
	
	def parseAgentsetBehaviour(self, behaviourNode):
		returnBehaviourData = {};
		
		returnBehaviourData["type"] = "none" if not "type" in behaviourNode.attrib.keys() else behaviourNode.attrib["type"];
		
		return returnBehaviourData;
		
	def parseAgentset(self, agentsetNode):
		returnAgentset = {};
		
		for child in agentsetNode:

			if child.tag == "Properties":
				returnAgentset["properties"] = self.parseAgentsetProps(child);
			elif child.tag == "Behaviour":
				returnAgentset["behaviour"] = self.parseAgentsetBehaviour(child);
		
		return returnAgentset;

	