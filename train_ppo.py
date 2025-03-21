import gym
from stable_baselines3 import PPO
from gym_alien_invasion import AlienInvasionEnv


env = AlienInvasionEnv()


model = PPO(
    "MlpPolicy", env, verbose=1,
    learning_rate=0.0003,
    gamma=0.99,
    n_steps=2048,
    ent_coef=0.01,  # Encourages exploration
)


model.learn(total_timesteps=200000)


model.save("ppo_alien_invasion")


env.close()