import pickle
import os

class Agent:
    def __init__(self):
        self.last_steer = 0.0
        self.data_file = "mydata.pkl"

    def chooseAction(self, obs, actions, myData=None):
        # Initialize myData if None
        if myData is None:
            myData = {}

        # Load previously saved data (only once)
        if not myData.get("loaded", False):
            if os.path.exists(self.data_file):
                with open(self.data_file, "rb") as f:
                    saved = pickle.load(f)
                    myData.update(saved)
                    print("✅ Loaded previous MyData")
            else:
                print("ℹ️ No previous data found. Starting fresh.")

            myData["loaded"] = True
            myData.setdefault("step_count", 0)
            myData.setdefault("history", [])

        # Update step count
        myData["step_count"] += 1

        # Read sensors
        lidar = obs["lidar"]  # [left, fleft, front, fright, right]
        velocity = obs["velocity"]
        left, fleft, front, fright, right = lidar

        # --- Steering logic ---
        if front < 0.3:
            steer = -1.0 if left > right else 1.0
        elif fleft < 0.4:
            steer = 0.6
        elif fright < 0.4:
            steer = -0.6
        else:
            steer = 0.0

        # Smooth steering
        steer = 0.7 * self.last_steer + 0.3 * steer
        steer = max(-1.0, min(1.0, steer))
        self.last_steer = steer

        if steer < -0.3:
            direction = "left"
        elif steer > 0.3:
            direction = "right"
        else:
            direction = "straight"

        # --- Speed control ---
        if front < 0.25:
            throttle = -1.0
        elif velocity < 2.2:
            throttle = 1.0
        elif velocity > 3.0:
            throttle = -0.5
        else:
            throttle = 0.0

        if throttle > 0.2:
            speed = "accelerate"
        elif throttle < -0.2:
            speed = "brake"
        else:
            speed = "coast"

        # Store in history
        myData["history"].append({
            "step": myData["step_count"],
            "velocity": velocity,
            "front": front,
            "steer": steer,
            "direction": direction,
            "speed": speed
        })

        return (direction, speed)

    def end(self, myData):
        """Save data at the end of simulation"""
        keys_to_save = {k: v for k, v in myData.items() if k not in ("loaded",)}
        with open(self.data_file, "wb") as f:
            pickle.dump(keys_to_save, f)
        print(f"💾 MyData saved with {keys_to_save.get('step_count', 0)} steps.")
