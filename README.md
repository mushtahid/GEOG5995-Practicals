# Agent-Based Model - GEOG5995 Assessment 1
This repository contains the practicals done as part of the [Programming for Social Science (GEOG5995) Course](https://www.geog.leeds.ac.uk/courses/computing/study/core-python-phd) under the [MSc/PhD CDAS programme](https://datacdt.org) under the School of Geography at the University of Leeds between September and October 2020.

The aim of the GEOG5995 was to introduce students to the world of programming, especially with Python.

## What does the code do?
This is a simple ABM model containing a herd of sheep and a pack of wolves! The main idea behind this project was to create a model where agents (representing the animals) can interact with each other and the environment in which they are in. The code will run the model in a GUI. It is recommended to read [this page on my website](https://mushtahid.github.io/projects/uol/pss/abm.html) as well to better understand the model. You can also use the python `help()` function.

### Core components of the ABM
The model consists of the following core components:
1. The Environment
2. The Animals (Sheep and Wolves)

### The Environment
Essentially a 300x300 Euclidean plane (Fig 1) generated from reading the raster data present in the csv file `in.txt`. Reading the data produces a 2D plane. After the model has run, the model writes the altered environment data in another csv file named `out.txt`. This file is overwritten every time the model is run.

![The Environment Image](https://mushtahid.github.io/projects/uol/pss/images/the_environment.png)  
*Fig. 1: The Environment*

### The Animals
Animals consist of sheep and wolves (Fig. 2). An object-oriented approach was taken in which the `Animal` class is defined in the `final_agent_framework.py`. The `Animal` class defines the behaviours of the animals, namely: moving around the environment, checking the distance between themselves, running towards the closest animal, not going beyond the limits of the environment by checking the boundary conditions.

![The Animals in the Environment Image](https://mushtahid.github.io/projects/uol/pss/images/the_animals.gif)  
*Fig. 2: The Animals (White = Sheep, Black = Wolves)*

The `Animal` class also sets the initial x and y coordinates of the animals. For the sheep, the values are obtained by [scraping web data](http://bit.ly/GeogLeedsAFData), and for the wolves they are randomly assigned.

The `Animal` class also sets the initial `store` values of the animals randomly. The represents an animal's energy level or stored food resources depending on the context. For example, The store value represents energy gained when an animal eats (wolves eating sheep or sheep eating grass from the environment), or energy lost when animals attempt to breed. It also represents resources (best to think of as stored food) which depending on the animal can be shared or stolen. For example, sheep can share their store with other sheep as their primary concern is surviving from the wolves. While wolves (although in reality are social creatures too) are lower in number and have poor access to food (sheep) - unless they are spawned randomly closer to the sheep in the beginning. Thus for the wolves, they also fight to steal food from other wolves in this model.

There are two child classes to `Animal`: `Sheep` and `Wolf`. These define the behaviours unique to each animal. The `Sheep` child class includes behaviours such as eating grass from the environment (thus altering the environment data) and running away from the closest wolf. The `Wolf` child class defines the wolves eating the sheep and gaining 4/5 of the eaten sheep's energy. The rest of the 1/5 of the eaten sheep's energy is returned to the environment (thus again altering the environment data).

The order of initialisation of each animal is randomly shuffled at each iteration so that everyone gets a fair shot at whatever their action is (eating/breeding/running away/fighting etc.) 

Detailed descriptions of each animal's behaviours can be found on my [github website](https://mushtahid.github.io/projects/uol/pss/abm.html). Moreover, the code is extensively commented so that you understand what every code does. You can also use the python `help()` function.

## How to run the model?
The model requires python 3.6+ to run as f-strings are extensively used. The file `final_model.py` contains the main model while the file `final_agent_framework.py` contains the `Animal`, `Sheep`, and `Wolf` class.

The model can be run via command/terminal prompt by running: `python final_model.py`

You will be asked if you want to modify certain initial settings to alter the conditions of the model. If you want to modify, input `y` (lowercase) and press enter. This will then ask 11 questions one for each modifiable variable. A description of what each variable does will be provided so that you understand what it will do once you modify it. You will also have the option to run with the default values of individual variables if you want to.

If you do not want to modify any variables, then input any character and press enter. This will run the model with the default setup. 

Once the model runs, a GUI will pop open where you will see a `Menu`. Click the `Run ABM Model` button from the `Menu` which will initiate the model. You should be able to see the animals in the environment interacting with each other and the environment. The sheep are the white ones, and the wolves are the black ones!

In the cmd/terminal, a printout of the details of each iteration will be presented. The details will include statements such as the action of each sheep, followed by the actions of each wolf and many more! You will also see the time to process each iteration.

The model will run until all sheep are eaten by the wolves or until the number of iterations have been completed.

### What happens when the model finishes running?
The modified environment data is saved as a csv file in `out.txt`. The total store value of the sheep and wolves are also stored separately in `total_sheep_store.txt` and `total_wolves_store.txt` files respectively. Note, for the total store values, the new values from additional runs of the model are added to the files instead of overwriting the previous values, while for the environment `out.txt`, the previous data is overwritten.

## The debugging process
Random seed was enabled. Random shuffle was commented out.

Extensive details of the actions of each sheep and wolf are printed as output. This allows me to easily debug the model by searching for keywords and ensure the model is working as intended. 

To aid with the debugging, I also diverted the output from the console to a text file which allowed me to quickly search for keywords using Notepad++. 

Diverting the output also enabled me to compare output from an earlier stable version to the latest one, for example, when I was moving some of the functions from `final_model.py` to the `final_agent_framework.py` module (to take an object-oriented approach). Outputs were compared by both importing the outputs of the stable version and the new code in two lists and by comparing if the contents of the lists are the same using the Equality `==` operator and also by the cmd file compare command `fc /lb2`. 

The codes to divert are commented out in the `final_model.py` because if these are active, the model will not run from cmd. However, if you wish to enable and divert the output, please use an IDE such as Spyder, which will ensure you are presented with the prompts and run the model while diverting the output to the text file.

## Known issues
1. When the sheep are running away from the wolves in a north/north-east direction, the wolves chasing the sheep do not seem to be able to catch up with the sheep until the sheep reaches the edge of the environment (Fig.3 ). This is not observed when the sheep flee in other directions.  
![Wolves unable to catch the sheep!](https://mushtahid.github.io/projects/uol/pss/images/unable_to_catch.gif)  
*Fig. 3: Wolves Unable to Catch the Sheep!*
2. The final statements such as (the final number of sheep and wolves and their total store values and the total time it took to run the model for the specified number of iterations), do not appear until the GUI is closed. Moreover, the statements appear only when the code is run from Spyder and not in cmd.

## Files/folder in the repository
1. `Previous_Practicals` folder contains the practicals based on which the `final_model.py` is built. These are based on the practicals present on the [course website](https://www.geog.leeds.ac.uk/courses/computing/study/core-python-phd/). Each file is named according to the respective course practical. 
2. `in.txt` - contains the 2d environment data.
3. `logo.ico` - the logo for GUI
4. `out.txt` - contains the altered 2d environment data. Old values are overwritten with new ones.
5. `total_sheep_store.txt` - a list of total sheep store values. New values are added instead of overwriting the previous one.
6. `total_wolves_store.txt` - a list of total wolf store values. New values are added instead of overwriting the previous one.
7. `final_agent_framwork.py` - agent framework module for the model.
8. `final_model.py` - the main codes for the model.

## Any issues/comments regarding the model?
You can reach me via [my website](https://mushtahid.github.io/) or [email](mailto:mushtahid@gmail.com).
