import random
import math
from itertools import permutations, product
from copy import deepcopy
from colorama import Fore, Back, Style, init

from CamelUpPlayer import CamelUpPlayer

class CamelUpBoard:
    def __init__(self, camel_styles: list[str]):
        self.TRACK_POSITIONS = 16
        self.DICE_VALUES = [1,2,3]
        self.BETTING_TICKET_VALUES = [5, 3, 2, 2]
        
        self.camel_styles = camel_styles
        self.camel_colors= camel_styles.keys()
        self.track = self.starting_camel_positions()
        self.pyramid = set(self.camel_colors)
        self.ticket_tents = {color:self.BETTING_TICKET_VALUES.copy() for color in self.camel_colors}
        self.dice_tents = [] #preserves order

    def starting_camel_positions(self)->list[list[str]]:
        '''Places camels on the board at the beginning of the game
            TODO: randomize these positions

            Return
               list[list[str]] - a 2D list model of the Camel Up race track
        '''
        track = [[] for i in range(self.TRACK_POSITIONS)]
        for i in list(self.camel_colors):
            track[random.choice(self.DICE_VALUES) - 1].append(i)
        return track
    
    def print(self, players: list[CamelUpPlayer]):
        '''Prints the current state of the Camel Up board, including:
            - Race track with current camel positions
            - Betting Tents displaying available betting tickets
            - Dice Tents displaying an ordered collection of rolled dice
            - Player information for both players
                - name
                - coins
                - betting tickets for the current leg of the race
        '''
        board_string = "\n"
         #Ticket Tents
        ticket_string = "Ticket Tents: "
        for ticket_color in self.ticket_tents:
            if len(self.ticket_tents[ticket_color]) > 0:
                next_ticket_value = str(self.ticket_tents[ticket_color][0])
            else:
                next_ticket_value = 'X'
            ticket_string+=self.camel_styles[ticket_color]+next_ticket_value+Style.RESET_ALL+" "
        board_string += ticket_string +"\t\t"

        #Dice Tents
        dice_string = "Dice Tents: "
        for die in self.dice_tents:
            dice_string+=self.camel_styles[die[0]]+str(die[1])+Style.RESET_ALL+" "

        for i in range (5-len(self.dice_tents)):
            dice_string+=Back.WHITE+" "+Style.RESET_ALL+" "
        
        #Camels and Race Track
        board_string += dice_string +"\n"
        for row in range(4, -1, -1):
            row_str = [" "]*16
            for i in range(len(self.track)):
                for camel_place, camel in enumerate(self.track[i]):
                    if camel_place == row:
                        row_str[i]=self.camel_styles[camel]+ camel +  Style.RESET_ALL 
            board_string += "🌴 "+str("   ".join(row_str))+" |🏁\n"
        board_string += "   "+"".join([str(i)+"   " for i in range(1, 10)])
        board_string += "".join([str(i)+"  " for i in range(10, 17)])+"\n"

        #Player Info
        player_string=""
        for player in players:
            player_string+=f"{player.name} has {player.money} coins."
            if len(player.bets)>0:
                bets_string = " ".join([self.camel_styles[bet[0]]+str(bet[1])+Style.RESET_ALL for bet in player.bets])
                player_string += f" Bets: {bets_string}"  
            player_string+="\t\t" 
        
        board_string+=player_string
        print(board_string+"\n")

    def reset_tents(self):
        '''Rests dice tents and ticket tents at the end of a leg
        '''
        self.ticket_tents = {color:self.BETTING_TICKET_VALUES.copy() for color in self.camel_colors}
        self.dice_tents = []

    def place_bet(self, color:str)->tuple[str, int]:
        '''Manages the board perspective when a player places a bet:
            - removes the top betting ticket (with highest value) from the appropriate Ticket Tent
            - returns the ticket

            Args
               color (str) - the color of the ticket on which a player would like to bet: 'r'
           
            Return
                tuple(str, int) - a tuple representation of a betting ticket: ('r', 5)
        '''
        tickets_left = self.ticket_tents[color]
        ticket = ()
        if len(tickets_left)>0:
            ticket =(color, tickets_left[0])
            self.ticket_tents[color] = tickets_left[1:]
        return ticket

    def move_AI(self, positions, color, roll):
        ### BEGIN SOLUTION
        for position in range(len(positions)):
            for i in range(len(positions[position])):
                if positions[position][i] == color:
                    for k in range(i, len(positions[position])):
                        if (position + roll) < 16:
                            positions[position + roll].append(positions[position][k])
                        else:
                            positions[15].append(positions[position][k])
                            
                    positions[position] = positions[position][:i]
                    return positions
        ### END SOLUTION
        return positions
    
    def move_camel(self, die:tuple[str, int], verbose=False):
        '''Updates the track according to the die color and value
           The camel of the appropriate color moves the apporpriate number of spaces, 
           along with all camels riding on top of that camel.

           Args
             die (tuple[str, int]) - A tuple represntation of the die: ('g', 2)

           Return
             list[list[str]] - a 2D list model of the Camel Up race track
        '''
        if verbose: print("Current track state:", self.track)
        ### BEGIN SOLUTION
        for position in range(len(self.track)):
            for i in range(len(self.track[position])):
                if self.track[position][i] == die[0]:
                    for k in range(i, len(self.track[position])):
                        if (position + die[1]) < 16:
                            self.track[position + die[1]].append(self.track[position][k])
                        else:
                            #TODO FINISH GAME
                            pass
                            
                    self.track[position] = self.track[position][:i]
                    if verbose: print("Updated track state:", self.track)
                    return self.track
        ### END SOLUTION
        if verbose: print("Updated track state:", self.track)
        return self.track
    
    def shake_pyramid(self)->tuple[str, int]:
        '''Manages all the steps (from the board persepctive) involved with shaking the pyramid, 
           which includes:
                - selecting a random color and dice value from the dice colors in the pyramid
                - removing the rolled dice from the pyramid
                - placing the rolled dice in the dice tents

            Return
                tuple[str, int] - A tuple representation of the rolled die
        '''
        ### BEGIN SOLUTION
        if len(self.pyramid) == 0: return ("", 0)
        color = random.choice(list(self.pyramid))
        self.pyramid.remove(color)
        roll = random.choice(self.DICE_VALUES)
        rolled_dice = (color, roll)

        self.dice_tents.append(rolled_dice)
        ### END SOLUTION
        return rolled_dice

    def is_leg_finished(self)->bool:
        '''Determines whether the leg of a race is finished

           Return
             bool - True if all dice have been rolled, False otherwise
        '''
        ### BEGIN SOLUTION
        
        if(len(self.dice_tents) == 5):
            return True
        else:
            return False

        ### END SOLUTION

    def get_rankings(self, track = "NOT DEFINED"):
        '''Determines first and second place camels on the track
           
           Returns:
            tuple: a tuple of strings of (1st, 2nd) place camels: ('b', 'y') 
        '''
        if track == "NOT DEFINED":
            track = self.track

        ### BEGIN SOLUTION
        camels_found = []
        for position_index in range(len(track) - 1, -1, -1):
            position = track[position_index]
            for camel_index in range(len(position) - 1, -1,  -1):
                if len(camels_found) < 2:
                    camels_found.append(position[camel_index])
                else:
                    return tuple(camels_found)

        

        ### END SOLUTION
        return 

    def get_all_dice_roll_sequences(self)-> set:
        '''
            Constructs a set of all possible roll sequences for the dice currently in the pyramid
            Note: Use itertools product function

            Return
               set[tuple[tuple[str, int]]] - A set of tuples representing all the ordered dice seqences 
                                             that could result from shaking all dice from the pyramid
        ''' 
        roll_space = set()
        ### BEGIN SOLUTION
        if len(self.pyramid) == 1:
            color = list(self.pyramid)[0]
            return {((color, 1),), ((color, 2),), ((color, 3),)}
        color_orders = list(permutations(list(self.pyramid)))
        rolls = list(product([1,2,3], repeat=len(self.pyramid)))
        for sequence in product(color_orders, rolls):
            path = []
            for i in range(len(sequence[0])):
                path.append((sequence[0][i], sequence[1][i]))
            roll_space.add(tuple(path))
        ### END SOLUTION
        return roll_space
        # return roll_space
    
    def run_enumerative_leg_analysis(self)->dict[str, tuple[float, float]]:
        '''Conducts an enumerative analysis of the probability that each camel will win either 1st or 
           2nd place in this leg of the race. The enumerative analysis counts 1st/2nd place finishes 
           via calculating the entire state space tree

           General Steps:
                1) Precalculate all possible dice sequences for the dice currently in the pyramid
                2) Move through each sequence of possible dice rolls to count the number of 1st/2nd places 
                   finishes for each camel
                3) Calculates the probability that each camel will come in 1st or 2nd based on the total 
                   number of 1st/2nd finishes out of the total number of dice sequences

                TODO: Add notes about using deepcopy to preserve state
           
           Returns: 
              dict[str, tuple[float, float]] - A dictionary representing the probabilities that a camel will 
                                               come in first or second place according to an enumerative analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        win_percents={color:(0, 0) for color in self.camel_colors}
        ### BEGIN SOLUTION
        all_roll_possibilities = self.get_all_dice_roll_sequences()
        roll_counts = len(all_roll_possibilities)
        win_counts = {color: [0,0] for color in self.camel_colors}
        for possible_sequence in all_roll_possibilities:
            copied_position = deepcopy(self.track)
            for roll in possible_sequence:
                copied_position = self.move_AI(copied_position, roll[0], roll[1])
            results = self.get_rankings(copied_position)
            win_counts[results[0]][0] += 1
            win_counts[results[1]][1] += 1
        ### END SOLUTION

        for color, counts in win_counts.items():
            win_percents[color] = (round(counts[0] / roll_counts, 3), round(counts[1] / roll_counts,3))

        return win_percents

    def run_experimental_leg_analysis(self, trials:int)->dict[str, tuple[float, float]]:
        '''Conducts an experimental analysis (ie. a random simulation) of the probability that each camel
            will win either 1st or 2nd place in this leg of the race. The experimenta analysis counts 
            1st/2nd place finishes bycounting outcomes from randomly shaking the pyramid over a given 
            number of trials.
           
           General Steps:
                1) Shake the pyramid enough times to randomly generate a dice sequence to finish the leg
                2) Count a 1st/2nd place finish for each camel
                3) Repeat steps #1 - #2 trials number of times
                3) Calculate the probability that each camel will come in 1st or 2nd based on the total 
                   number of 1st/2nd finishes out of the total number of trials

                TODO: Add notes about using deepcopy to preserve state

           Args
              trials (int): The number of random simulations to conduct

           Returns: 
              dict[str, tuple[float, float]] - A dictionary representing the probabilities that a camel will 
                                               come in first or second place according to an enumerative analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        win_percents={color:(0, 0) for color in self.camel_colors}
        ### BEGIN SOLUTION
        all_roll_possibilities = list(self.get_all_dice_roll_sequences())
        win_counts = {color: [0,0] for color in self.camel_colors}
        for i in range(trials):
            sequence = random.choice(all_roll_possibilities)
            copied_position = deepcopy(self.track)
            for roll in sequence:
                copied_position = self.move_AI(copied_position, roll[0], roll[1])
            results = self.get_rankings(copied_position)
            win_counts[results[0]][0] += 1
            win_counts[results[1]][1] += 1
        ### END SOLUTION

        for color, counts in win_counts.items():
            win_percents[color] = (round(counts[0] / trials, 3), round(counts[1] / trials,3))

        return win_percents


        ### END SOLUTION
        return win_percents
   
if __name__ == "__main__":
    camel_styles= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    board = CamelUpBoard(camel_styles)
    p1 = CamelUpPlayer("p1")
    p2 = CamelUpPlayer("p2")
    board.print([p1, p2])
    die = ('b', 1)
    board.move_camel(die)
    #Roll 3 random dice
    rolled_die = board.shake_pyramid()
    board.move_camel(rolled_die)
    rolled_die = board.shake_pyramid()
    board.move_camel(rolled_die)
    board.print([p1, p2])
    #Probabilites
    all_possible_dice_sequences= board.get_all_dice_roll_sequences()
    print(f"{len(all_possible_dice_sequences)} possible dice sequences for {len(board.pyramid)} dice in the pyramid:") 
    print("Enumerative Probabilities:", board.run_enumerative_leg_analysis())
    print("Experimental Probabilities:", board.run_experimental_leg_analysis(5000))
