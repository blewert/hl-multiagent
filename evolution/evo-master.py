## ./evo-master.py
## ======================
## Benjamin Williams <eeu222@bangor.ac.uk>
##

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
		