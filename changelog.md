Changelog
=========
Managed by Benjamin Williams (**<eeu222@bangor.ac.uk>**)



### pre-build 1 (21/06/2014)
* Started creating initial programs to delve into the extension of the native turtle module for python
* Creation of programs to move turtles around environment, and perform basic tasks within
* Multi-agent implementation of turtles, along with automative behaviour (wandering).

### build 1 (pre 21/06/2014)

###### Initial creation of alternative to native python turtle module, providing very basic (and fast) turtle functionality:
* An environment, with a fixed width and height.
* Functionality to wrap around environment.
* Fixed origin point: `(0,0)` relative to window.
* Single turtle shape (ellipse) accompanied by turtle position, heading and speed.
* Ability to move turtles throughout environment, at varying speed.
* Ability to toggle on/off tkinter drawing to help computation speed, as well as shape updates.
* Vision cone drawing, using native tkinter `create_arc()` at facing angle offset.
* Introduction of `Agent`, `Agentset` and `Environment` classes.

###### Agentset:
* Primitive collision detection using Euclidean distance.
* Primitive collision detection with vision cone using barycentric coordinate method of checking whether points lie in a triangle (bug-prone, will fix in successor builds).

###### Environment:
* Now handles canvas object and drawing.

###### Agent:
* Now contains all methods previously defined without a class, for a single agent object.


### build 2.1 (23/06/2014)

* Modularized classes into package hierachy, for easier inclusion with scripts

###### Agent:
* Implemented `forward()`, and it's alias `fd()`.
* Implemented `back()`, and it's alias `bk()`.
* Implemented `rt()` and `lt()`, as well as `random_turn()` (random lt/rt amount).
* Implemented `distancexy()` and `distance()` (distance between other agents and coordinates).
* Added `setxy()` and `randomxy()`
* Added primitive per-agent variable system using dictionaries:
	* `agent.getvar(var)` returns a value from the dictionary if it exists, null otherwise.
	* `agent.varexists(var)` returns true/false depending on whether the variable exists.
	* `agent.setvar(var, value)` sets/adds a value into the dictionary.

###### Agentset:
* Added `agentset.setvars(var, value)`, which sets a value for each agent in the `Agentset`.
* Figured out issue with barycentric triangle collision algorithm - was updating position before rechecking, causing loss of precision.
* Updated constructor for `Agentset` - you can now supply an amount of turtles to create along with parameters to be passed to `Agent()`.
* Added `shuffle()` and it's alias, `randomize()` to randomly set each turtle's position in the environment via `Agentset`.
* Made `Agentset.agents` (internal list of agents) iterable by default (e.g, `for agent in Agentset(50)` works fine)
* Added `update_shapes()` in `Agentset` context.


### build 2.2 (24/06/2014 to 26/06/2014)

###### Agentset:
* Added `order(radius, point)` to order turtles around a point (like NetLogo's `create-ordered-turtles`).

###### Agent:
* Added `randomx()` and `randomy()`, and changed `randomxy()` to call these methods.
* Added `hide()` and `ht()`, using `itemconfigure()` along with `state=tkinter.HIDDEN`.
* Added `show()` and `st()`, using `itemconfigure()` along with `state=tkinter.NORMAL`.
* Added `hidden` instance variable, to tell whether or not the turtle is hidden.
* Added `move_to()` which moves the agent to the position of another agent.
* Added `facexy()`, to face a specified coordinate.
* Added `face()`, using `facexy()` to face a specified agent.

###### Added primitive patch class using tkinter rectangles:
* Patches belong to an environment: `Environment.patches`.
* Patches have a width, height, position and tag for shape (for tkinter's canvas).


### build 2.3 (27/06/2014)

###### Patches/Agent/Environment:
* Added `patch_at()` and `patch_at_idx()` to `Agent` class, to determine which patch a specified set of coordinates lies on.
* Added optional `situate` argument to `create_patches()` for `Environment`, to cancel drawing of patches.
* Fixed bug with `Patch` class, where patches were created without a tag if situated.
* Added `patch_here()` and `patch_here_idx()` to `Agent` class, to determine which patch this agent is currently on.
* Added `patch_ahead()` and `patch_ahead_idx()` to `Agent` class, to determine a patch from a relative distance and offset angle of an agent.
* Added the ability to toggle outlines of vision cones in `Agent` constructor, using `outline=False` or `outline=True` (also, in agentset constructor).
* Added the ability to toggle grid of patches in `Patch` constructor, using `grid=True` or `grid=False` (also, in `Environment.create_patches()`).

### build 2.3 (29/06/2014)

###### Agent/Agentset:
* Fixed issue with cone fill colour not setting in constructor.
* Added `fill` as parameter for agent fill colour, and `coneFill` as the colour for the agent's cone.
* Added `set_fill()` to `Agent`, to colour the agent's shape a specified colour.
* Added `create_agents()`, which appends a specific amount of agents into the agentset, with specific parameters.
* Simplified `get_agents_in_radius()` of `Agentset` to use `distance()` of `Agent` class, rather than manually calculating euclidean distance.
* Changed `get_agents_in_radius()` and `get_agents_in_cone()` to `in_radius()` and `in_cone()` for `Agentset`, to avoid confusion.

###### VisionCone:
* Added `set_fill()` to change vision cone colour.
