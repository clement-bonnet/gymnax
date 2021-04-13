import jax
import jax.numpy as jnp
import gym
import gymnax
import unittest, math
import numpy as np


class TestCartPole(unittest.TestCase):
    num_episodes, num_steps = 100, 150
    tolerance = 1e-04

    def test_cartpole_step(self):
        """ Test a step transition for the env. """
        env = gym.make("CartPole-v0")
        rng, reset, step, env_params = gymnax.make("CartPole-v0")

        # Loop over test episodes
        for ep in range(TestCartPole.num_episodes):
            obs_gym = env.reset()
            done_gym = 0
            # Loop over test episode steps
            for s in range(TestCartPole.num_steps):
                action = env.action_space.sample()
                state_gym = jnp.hstack([obs_gym, done_gym, 0])
                obs_gym, reward_gym, done_gym, _ = env.step(action)
                rng, rng_input = jax.random.split(rng)
                obs_jax, state_jax, reward_jax, done_jax, _ = step(rng_input,
                                                                   env_params, state_gym,
                                                                   action)

                # Check for correctness of transitions
                self.assertEqual(done_gym, done_jax)
                assert math.isclose(reward_gym, reward_jax,
                                    rel_tol=TestCartPole.tolerance)
                assert np.allclose(obs_gym, obs_jax,
                                   atol=TestCartPole.tolerance)
                if done_jax:
                    break

    def test_cartpole_reset(self):
        """ Test reset obs/state is in space of OpenAI version. """
        env = gym.make("CartPole-v0")
        rng, reset, step, env_params = gymnax.make("CartPole-v0")
        for ep in range(TestCartPole.num_episodes):
            rng, rng_input = jax.random.split(rng)
            obs, state = reset(rng_input, env_params)
            # Check observation space
            self.assertTrue(env.observation_space.low[0]
                            <= obs[0]
                            <= env.observation_space.high[0])
            self.assertTrue(env.observation_space.low[1]
                            <= obs[1]
                            <= env.observation_space.high[1])
            self.assertTrue(env.observation_space.low[2]
                            <= obs[2]
                            <= env.observation_space.high[2])
            self.assertTrue(env.observation_space.low[3]
                            <= obs[3]
                            <= env.observation_space.high[3])