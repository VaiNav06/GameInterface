import gym
from stable_baselines3 import PPO
from gym_alien_invasion import AlienInvasionEnv


env = AlienInvasionEnv()
model = PPO.load("ppo_alien_invasion")

obs = env.reset()
done = False

while not done:
    action, _ = model.predict(obs)
    obs, reward, done, _ = env.step(action)
    env.render()
    
env.close()