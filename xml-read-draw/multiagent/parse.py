import xml.etree.ElementTree as ET

class Parser:
	
	def __init__(self, file):
		self.file = file;
		self.xmlTree = ET.parse(self.file);
		self.root = self.xmlTree.getroot();
	
	def parse(self):
			
		if self.root.tag != "Environment":
			return False;
			
		agents    = [];
		agentsets = [];
		
		for child in self.root:
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
	
	def parseAgentset(self, agentsetNode):
		returnAgentset = {};
		
		for child in agentsetNode:
			if child.tag == "Properties":
				returnAgentset["properties"] = self.parseAgentsetProps(child);
		
		return returnAgentset;

	