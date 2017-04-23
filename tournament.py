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

        self.moves += [move]
            
        return self
        

        
class Bot:

    def addHist(self, opponent, moves):
        if not hasattr(self, 'history'):
            self.history = {}
            
        if opponent in self.history:
            self.history[type(opponent)] += [moves]
        else:
            self.history[type(opponent)] = [moves]

        print ("New history for " + str(type(opponent)) + ": " + str(self.history[type(opponent)]))

        return self
            

    def decision(self, opponent, match): #match is ( [(myMove, otherMove), (myMove, otherMove), ...] , roundsLeft )
        pass

    def simulate(self, opponent, match):
        return self.decision(opponent, match)   #For now... eventually will include time-boxing


class CooperateBot(Bot):
    name = "CooperateBot"
    
    def decision(self, opponent, match):
        return True


class DefectBot(Bot):
    name = "DefectBot"
    def decision(self, opponent, match):
        return False

    
class RandomBot(Bot):
    name = "RandomBot"
    def decision(self, opponent, match):
        if random.randint(0,1) == 0:
            return True
        else:
            return False
    

class TitForTat(Bot):
    name = "TitForTat"
    def decision(self, opponent, match):
        if len(match.moves) == 0:
            return True
        else:
            if match.moves[len(match.moves)-1](1) == Moves.c: #Do what they did last time
                return True
            else:
                return False
            
        
class PredictBot(Bot):
    name = "PredictBot"
    def decision(self, opponent, match):
        
        dSelf = deepcopy(self).addHist(opponent, (Moves.d,Moves.d))
        dOpponent = deepcopy(opponent).addHist(self, (Moves.d,Moves.d))
        dMatch = deepcopy(match).add( (Moves.d,Moves.d) ).flip()
        rD = dOpponent.simulate(dSelf, dMatch)
        
        if rD == Moves.c:
            return False #Defect if it's not punished -- don't bother simulating cooperation
        else:

            cSelf = deepcopy(self).addHist(opponent, (Moves.c,Moves.c))
            cOpponent = deepcopy(opponent).addHist(self, (Moves.c,Moves.c))
            cMatch = deepcopy(match).add( (Moves.c,Moves.c) ).flip()
            rC = dOpponent.simulate(cSelf, cMatch)
            
            if rC == Moves.d: #If they don't care / will defect either way
                return False
            else:
                return True #Iff they cooperate iff I do
                




def runRound(bot1, bot2, match):
    move1 = bot1.simulate(bot2, match)
    move2 = bot2.simulate(bot1, deepcopy(match).flip())

    bot1.addHist(bot2, (move1, move2))
    bot2.addHist(bot1, (move2, move1))

    match.add((move1, move2))

    
def runMatch(bot1, bot2, rounds):

    match = Match(rounds)

    for i in range(rounds):
        runRound(bot1, bot2, match)


    
bot1 = PredictBot()
bot2 = DefectBot()

runMatch(bot1, bot2, 10)
print(bot1.history)

#print(type(bot1))
