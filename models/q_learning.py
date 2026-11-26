import numpy as np

class TabularQLearner:
    """
    Small tabular Q-learning policy for choosing a target channel count.
    State: (traffic band, neighboring-load pressure band).
    Action: target channel count from 1 through max_channels.
    This is a teaching-scale policy, not a production RAN controller.
    """
    def __init__(self, max_channels=8, seed=7):
        self.max_channels = max_channels
        self.actions = np.arange(1, max_channels + 1)
        self.q = np.zeros((3, 3, len(self.actions)), dtype=float)
        self.rng = np.random.default_rng(seed)

    @staticmethod
    def state(load, neighbor_pressure):
        traffic_band = 0 if load < 35 else (1 if load < 75 else 2)
        pressure_band = 0 if neighbor_pressure < 35 else (1 if neighbor_pressure < 70 else 2)
        return traffic_band, pressure_band

    def train(self, episodes=5000, alpha=0.12, gamma=0.85, epsilon=0.18):
        # A compact simulated environment: reward balances served demand,
        # spectrum cost, and a penalty for aggressive allocation under pressure.
        for _ in range(episodes):
            load = self.rng.uniform(5, 130)
            pressure = self.rng.uniform(5, 110)
            state = self.state(load, pressure)
            if self.rng.random() < epsilon:
                action_idx = self.rng.integers(len(self.actions))
            else:
                action_idx = int(np.argmax(self.q[state]))
            channels = int(self.actions[action_idx])
            capacity = channels * 13.0
            served = min(load, capacity)
            blocked = max(0.0, load - capacity)
            reward = (served / 10.0) - (channels * 0.85) - (blocked / 7.0)
            reward -= max(0, channels - 5) * pressure / 90.0
            # One-step terminal update; this is a contextual bandit-like Q update.
            old = self.q[state][action_idx]
            self.q[state][action_idx] = old + alpha * (reward - old)
        return self

    def choose_channels(self, load, neighbor_pressure):
        state = self.state(load, neighbor_pressure)
        return int(self.actions[int(np.argmax(self.q[state]))])
