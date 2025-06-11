import random

class Agent:
    def __init__(self):
        
        self.exploration_rate = 0.05

    def chooseAction(self, observations, possibleActions):
        
        distance_sensors = observations['lidar']
        speed = observations['velocity']

        
        outer_left, mid_left, straight_ahead, mid_right, outer_right = distance_sensors

    
        total_left = outer_left + mid_left
        total_right = outer_right + mid_right

        def determine_action():
            
            if min(distance_sensors) < 0.1:
                if ('straight', 'brake') in possibleActions:
                    return ('straight', 'brake')
                return random.choice(possibleActions)

            
            if total_right + 0.2 < total_left:
                direction = 'left'
            elif total_left + 0.2 < total_right:
                direction = 'right'
            else:
                direction = 'straight'

            
            if straight_ahead < 0.6 or mid_left < 0.5 or mid_right < 0.5:
                if (direction, 'brake') in possibleActions:
                    return (direction, 'brake')

            
            if speed > 0.19:
                if (direction, 'brake') in possibleActions:
                    return (direction, 'brake')
                elif (direction, 'coast') in possibleActions:
                    return (direction, 'coast')

        
            if speed <= 0.3 and straight_ahead > 0.8 and mid_left > 0.8 and mid_right > 0.8:
                if (direction, 'accelerate') in possibleActions:
                    return (direction, 'accelerate')

            
            if (direction, 'coast') in possibleActions:
                return (direction, 'coast')

            
            return random.choice(possibleActions)

        
        if random.random() < self.exploration_rate:
            return random.choice(possibleActions)
        else:
            return determine_action()

    def load(self, data=None):
    
        pass
