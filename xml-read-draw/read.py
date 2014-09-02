import xml.etree.ElementTree as ET

DATA_FILE = "test.xml";

#Parse xml file and grab root of document
xmlTree        = ET.parse(DATA_FILE);
simulationRoot = xmlTree.getroot();

#Agents and agentsets to be read into
agents    = [];
agentsets = [];

if simulationRoot.tag == "Environment":
	print("Found an environment to parse.");
	
def parseAgentsetProps(propertiesNode):
	returnProperties = {};
	
	for property in propertiesNode:
	
		if property.tag != "Property":
			continue;
		
		for attribute in property.attrib:
			if attribute == "tag":
				returnProperties[property.attrib[attribute]] = property.text;
		
	return returnProperties;		
	
def parseAgentset(agentNode):
	returnAgentset = {};
	
	for child in agentNode:
		if child.tag == "Properties":
			returnAgentset["properties"] = parseAgentsetProps(child);
		
	return returnAgentset;
	
for child in simulationRoot:

	#A child (agentset) is inside the simulation tag.
	if child.tag == "Agentset":
		agentsets.append(parseAgentset(child))
		

print("Agent sets:");
print(agentsets);
		
	#print("tag: %s, attribute: %s" % (child.tag, child.attrib));
	
	