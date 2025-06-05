from agents.Agent import Agent

class MyAgent(Agent):
    def __init__(self):
        self.name = "MyRuleAgent"

    def chooseAction(self, obs):
        # Read lidar and velocity from observation
        lidar = obs['lidar']  # [left, front-left, front, front-right, right]
        velocity = obs['velocity']

        left = lidar[0]
        center = lidar[2]
        right = lidar[4]

        # Steering decision
        if right > left and right > center:
            direction = 'right'
        elif left > right and left > center:
            direction = 'left'
        else:
            direction = 'straight'

        # Speed decision
        min_lidar = min(lidar)
        if min_lidar < 0.5:
            speed = 'brake'
        elif velocity < 0.5 and center > 1.0:
            speed = 'accelerate'
        else:
            speed = 'coast'

        return (direction, speed)
