from enum import Enum
import signal
from contextlib import contextmanager
import random
from copy import deepcopy

class Moves(Enum):
    c = True
    d = False
    timeout = True


    
class Match:

    def __init__(self, iterations, moves = []):
        self.roundsLeft = iterations
        self.moves = moves


    def flip(self):
        self.moves = [(move[1],move[0]) for move in self.moves]
        return self
        

    def add(self, move):    
        if self.roundsLeft <= 0:
            raise Exception("Tried to run a round with none left in the match!")
        else:
            self.roundsLeft -= 1

        if self.moves == []:
            self.moves = [move] #When the list is empty, adding a tuple will instead add the tuple's elements in order, creating a list of Moves objects instead
        else:
            self.moves += move
            
        return self
        

        
class Bot:

    history = [] #Format: (opponent, [(myMove, otherMove), (myMove, otherMove), ... ])

    def decision(self, opponent, match): #match is ( [(myMove, otherMove), (myMove, otherMove), ...] , roundsLeft )
        return True

    def simulate(self, opponent, match):
        return self.decision(opponent, match)   #For now... eventually will include time-boxing


class CooperateBot(Bot):
    def decisiono(self, opponent, match):
        return True


class DefectBot(Bot):
    def decision(self, opponent, match):
        return False

    
class RandomBot(Bot):
    def decision(self, opponent, match):
        if random.randint(0,1) == 0:
            return True
        else:
            return False
    

class TitForTat(Bot):
    def decision(self, opponent, match):
        if len(match.moves) == 0:
            return True
        else:
            if match.moves[len(match.moves)-1](1) == Moves.c: #Do what they did last time
                return True
            else:
                return False
            
        
class PredictBot(Bot):
    def decision(self, opponent, match):
        rD = opponent.simulate(self, deepcopy(match).add( (Moves.d,Moves.d) ).flip() ) #Should add to virtual PredictBot's history
        if rD == Moves.c:
            return False #Defect if it's not punished -- don't bother simulating cooperation
        else:
            rC = opponent.simulate(self, deepcopy(match).add( (Moves.c,Moves.c) ).flip() )
            if rC == Moves.d: #If they don't care / will defect either way
                return False
            else:
                return True #Iff they cooperate iff I do
                



bot1 = PredictBot()
bot2 = DefectBot()
thisMatch = Match(100)
print (bot1.simulate(bot2, thisMatch))
