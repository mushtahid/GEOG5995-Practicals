# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 11:20:41 2020
Agent framework module.
@author: Mushtahid
email: mushtahid@gmail.com
"""
import random
# random.seed(10) # Uncomment for debugging.

class Animal:
    """
    The parent animal class.
    
    The parent class contains the follwing methods:
        1. constructor
        2. str
        3. dist_animals
        4. boundary_conditions
        5. move
        6. run_to_closest_animal
        7. breed_cost
    
    Each method is appropriately defined and elaborated within itself.
    
    In summary, there are two species of animals housed in the constructor,
    wolves and sheep. The sheep eats grass from the 2D environment and breeds
    and shares food (store value) with each other. The wolves eats the sheep 
    and breeds and fights with other wolves for stored food (store value). 
    
    Breeding costs energy (store value) which is the same for both sheep and 
    wovles. 
    
    Both animals can run closer to its own species. The sheep can run 
    away from wolves (which is not set up in the Animal class but on a
    seperate child Sheep class) and wolves can chase sheep. 
    
    During movement, boundary conditions are checked so that the animals stay 
    within the limits of the environment. The eating behaviours of the animals 
    are set up in their own respective child classes.
    
    The store value represented by the variable store is defined in the
    constructor. The store value can either mean energy level or food store.
    """
    
    def __init__(self, environment, sheep, wolves, y=None, x=None):
        """
        Constructor method for the parent class Animal

        Parameters
        ----------
        wolves : List
            Contains the wolves.
        sheep : List
            Contains the sheep.
        environment : List
            Contains the 2D raster data of the environment-an Euclidean plane.
            As the environment data changes, the colour of the environment
            will change too.
        y : Integer, optional
            Set the inital y coordinate of animals. Default is None.
            When default value of None is used, the y coordinate is randomly
            assigned. The current set up assigns y to sheep by scraping web
            data but not to wolves.
        x : Integer, optional
            Set the inital x coordinate of animals. Default is None.
            When default value of None is used, the y coordinate is randomly
            assigned. The current set up assigns x to sheep by scraping web
            data but not to wolves.
        
        Constructor also contains the store variable which assigns the initial
        store value (which represents energy/resources) of the animals based  
        on random probability.
        
            The store value represents energy gained when an animal eats, 
            for example wolves eating sheep or sheep eating grass from the 
            environment, or energy lost when animals are attemp breeding.
        
            It also represents resources (best to think as stored food) which
            depending on the animal can be shared or stolen. For example, 
            sheep can share their store with other sheep as their primary 
            concern is surviving from the wolves. While wolves (although in 
            reality are social creatures too) are lower in number and have
            poor access to food(sheep) - unless they are spawned closer to the
            sheep in the beginning. Thus for the wolves, they also fight to 
            steal food from other wolves in this model.
        """
        self.wolves = wolves
        self.sheep = sheep
        self.environment = environment
        if y == None:
            self.y = random.randint(0, len(environment)-2)
        else:
            self.y = y
        if x == None:
            self.x = random.randint(0, len(environment[0])-2)
        else:
            self.x = x   
        # Set initial store value based on probability
        if random.random() < 0.25:
            self.store = 100
        elif 0.25 <= random.random() < 0.50:
            self.store = 200
        elif 0.50 <= random.random() < 0.75:
            self.store = 300
        else:
            self.store = 400
            
    def __str__(self):
        """
        Description of an animal (x and y coordinate and store value)
        
        Returns
        -------
        str
            It returns the animal's current y and x coordinates along with 
            their current store vlue.

        """
        return f"y={self.y}, x={self.x}, store={self.store}"
    
    def dist_animals(self, animal):
        """
        Calculates the Euclidean distance between two animals
        
        Parameters
        ----------
        animal :
            This can be another animal of the same or different species.

        Returns
        -------
        Float
            Calculates the Euclidean distance between two animals whether 
            it be sheep, wolves or both on an Euclidean plane.
            
            Uses the Pythagorean Theorem and Cartesian coordinates (x and y)
            of the animals. 
            
            To learn more about Euclidean distance/plane and Cartesian 
            coordinates visit this Wikipedia page:
            https://en.wikipedia.org/wiki/Euclidean_distance

        """
        return (((self.y - animal.y)**2) + ((self.x - animal.x)**2))**0.5

    def boundary_conditons(self):
        """
        Checks the boundary conditions of the environment.

        The environment here is a 2D Euclidean plane measuring 300X300.
        If the animal's x and y coordinates go beyond the limits of the 
        environment, the the boundary conditions reset their x and y
        coordinates to bring them back.
        """
        if self.y >= len(self.environment):
            self.y = len(self.environment)-2
        elif self.y <= 0:
            self.y = 2
        if self.x >= len(self.environment[0]):
            self.x = len(self.environment[0])-2
        elif self.x <= 0:
            self.x = 2

    def move(self):
        """
        Moves the animals under normal circumstances.

        fs = fast speed and fast speed cost, i.e, reduction in store.
        ms = medium speed and medium speed cost.
        ss = slow speed (no slow speed cost applies)
        
        The animals are moved based on a combination of their store value
        and random probability (p). Boundary conditions are checked via
        the boundary_conditions method.
        
        If store >=600 and p<0.5, the x and y are changed by a fs value,
        either + or - depending on another p of 0.5. At the same time fs 
        amount is deducted from store as energy to travel.
        
        If store between 100 and 600 and p<0.5, the x and y are changed by a 
        ms value, either + or - depending on another p of 0.5. At the same 
        time ms amount is deducted from store as energy to travel.
        
        If store <= 100 p>=0.5 OR when store values are good enough for fs/ms 
        but p >=0.5, the x and y are changed by a ss value, either + or - 
        depending on another p of 0.5. Here no energy/store is deducted. This
        enables an animal with high store to also randomly move slowly and
        not deplete all their energy travelling!
        
        """
        fs = 10 # Fast speed and fast speed cost.
        ms = 5 # Medium speed and medium speed cost.
        ss = 1 # Slow speed and slow speed cost.
        if self.store >= 600 and random.random() <0.5:
            self.store -= fs
            if random.random() < 0.5:
                self.y += fs
            else:
                self.y -= fs
            if random.random() < 0.5:
                self.x += fs
            else:
                self.x -= fs
        elif 100 < self.store < 600 and random.random() <0.5:
            self.store -= ms
            if random.random() < 0.5:
                self.y += ms
            else:
                self.y -= ms
            if random.random() < 0.5:
                self.x += ms
            else:
                self.x -= ms
        else:
            if random.random() < 0.5:
                self.y += ss
            else:
                self.y -= ss
            if random.random() < 0.5:
                self.x += ss
            else:
                self.x -= ss
        # Check boundary conditions            
        self.boundary_conditons()
    
    def run_to_closest_animal(self, closest_animal):
        """
        Animal runs towards its closest animal.

        Parameters
        ----------
        closest_animal :
            This can be another animal of the same or different species.
            For sheep, they can move towards their closest sheep. A wolf
            can move towards its closest sheep or wolf.

        This method can and should be improved. For example, right now 
        no energy/store is utilised by this method. Moreover, assignment of 
        the x and y itself should be improved.
        
        This method also ensures boundary conditons are met by calling the
        boundary_conditions() method to ensure animals don't go beyond the 
        2D environment.

        """
        # This algorithm should be improved!
        # Here no energy is lost while running!
        # So can add some energy loss.
        self.y = (int((self.y + closest_animal.y)/2))
        self.x = (int((self.x + closest_animal.x)/2))
        self.boundary_conditons() # Check boundary conditions.
    
    def breed_cost(self, animal):
        """
        The new store value of animals after their breeding attemp.

        Parameters
        ----------
        animal : 
            Either a sheep or wolf, depends on the currentt animal (either
            a sheep or a wolf).

        Returns
        -------
        float
            Breeding costs energy, and thus the new store value of the 
            animals after they have attempted breeding (whether successful
            or failed) is half the average of both animals.
        """
        # Breeding (successful/failed) costs energy and
        # the new store value of both sheep will be the
        # half of average of both sheep. This is same
        # for wolves.
        return ((self.store + animal.store)/2)/2
    
class Sheep(Animal):
    """
    The child class for sheep. The parent class is Animal.
    
    It has the following methods:
        1. eat
        2. run_from_cw (cw represents closest wolf)
    
    eat method allows the sheep to eat the grass and the run_from_cw allwos
    the sheep to run away from the closest wolf. They are further elaboreatd
    within themselves.
    """

    def eat(self):
        """
        The sheep eating the environment.

        Sheep eating the environment represents eating grass from the 
        environment. With every step, if the environment x and y contains
        >10 value, the sheep consumes only 10 and adds to its store value.
        
        If the environment contains <= 10 value, the sheep eats what is
        left.
        """
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        else:
            self.environment[self.y][self.x] -= self.environment[self.y]\
                                                                [self.x]
            self.store += self.environment[self.y][self.x]
            
    def run_from_cw(self, cw):
        """
        Sheep running away from the closest wolf method.

        Parameters
        ----------
        cw : 
            Represents the closest wolf the sheep is running away from.

        This method also ensures boundary conditions are met via calling the
        boundary_conditions method. 
        
        The algorithm, however, should be improved, for example by adding
        store/energy loss and varying the speed depending on current store
        value.

        """
        # Works but needs improvement!
        self.y = self.y + (self.y - int((self.y + cw.y)/2))
        self.x = self.x + (self.x - int((self.x + cw.x)/2))
        self.boundary_conditons()
            
class Wolf(Animal):
    """
    The child class for wolves. The parent class is Animal.
    
    It has the following methods:
        1. eat
    
    eat method allows the wolves to eat the closest sheep.
    """
    
    def eat(self, cs):
        """
        Wolf eating a sheep method.

        Parameters
        ----------
        cs : 
            Represents the closest sheep a wolf is going to eat.

        A wolf can't eat the entire sheep (for example bones). So some store
        value of the sheep are returned to the environment, which is 1/5th,
        and thus the wolf receives 4/5th of the sheep's store.
        
        The closest sheep is then removed from the sheep list and a printout
        of how much the environment receives is printed.
        """
        # Wolf eats 4/5 of the sheep as can't eat everything!
        # The rest of the 1/5 is returned to the environment.
        self.store += (cs.store*(4/5)) # Wolf eats 4/5
        env_rcv = (cs.store*(1/5)) # Environment received 1/5
        self.environment[self.y][self.x] += env_rcv 
        cs.store = 0 # CS store is 0
        self.sheep.remove(cs)
        print(f"---->Env received ({env_rcv}).")

    # The following represents remnents of a previous version of the eat 
    # method where I incorporated the for loop of sheep inside the method. 
    # While it was successfully, subsequent expansions of the code became too much 
    # work for me to try and incorporate the other algorithms inside this 
    # method and as such I have decided to not put big chunks of code in this 
    # agent-framework and instead created manageable methods.
    
    # def eat(self, proximity, i):
    #     sheep_count = -1
    #     for j in self.sheep[:]:
    #         sheep_count += 1
    #         distance = self.dist_animals(j)
    #         # print(f"wolf{i}: {wolves[i].y},{wolves[i].x}, sheep{j}: {sheep[j].y},{sheep[j].x}, d={distance}")
    #         print(f"Wolf {i} {self.y},{self.x}, sheep: {sheep_count} {j.y},{j.x}, d={distance}")
    #         if distance < proximity:
    #             self.store += j.store
    #             print(f"Sheep {sheep_count} {j} eaten by Wolf {i}")
    #             j.store = 0
    #             self.sheep.remove(j)
    #             break
