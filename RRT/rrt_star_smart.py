#!/usr/bin/env python

import pygame
import sys

from constants import GREEN, RED, BLACK, WHITE, YELLOW, PURPLE
from tree import Tree
from helper_functions import dist
from node import Node

from obstacles import Obstacles

RADIUS = 50.0


class RRTStarSmart:
	""" Class for RRT* Path Planning."""
	def __init__(self,
				 start_point, goal_point,
				 max_num_nodes, min_num_nodes,
				 goal_tolerance, epsilon_min, epsilon_max, screen,
				 obstacles, obs_resolution):
		self.screen = screen
		self.obstacles = obstacles
		self.obs_resolution = obs_resolution
		self.nodes = list()
		self.start_point = start_point
		self.goal_point = goal_point

		self.max_num_nodes = max_num_nodes
		self.min_num_nodes = min_num_nodes
		self.epsilon_min = epsilon_min
		self.epsilon_max = epsilon_max

		self.goal_tolerance = goal_tolerance
		self.goal_found = False

		self.tree = Tree(True,
						 start_point,
						 node_color=GREEN,
						 connection_color=GREEN,
						 goal_node_color=BLACK,
						 path_color=RED,
						 goal_tolerance=goal_tolerance,
						 epsilon_min=epsilon_min,
						 epsilon_max=epsilon_max,
						 max_num_nodes=max_num_nodes,
						 screen=self.screen,
						 obstacles=self.obstacles, obs_resolution=self.obs_resolution,
						 biasing_radius=20.0)

		self.tree.set_goal(Node(goal_point, None))
		self.goal_node = self.tree.get_goal()
		self.n = None

	def constant_draw(self):
		""" . """
		# GOAL POINT --> GRAY CIRCLE
		pygame.draw.circle(self.screen, PURPLE, self.goal_point, self.goal_tolerance)

	def planning(self):
		""" ."""
		i = 0
		b = 100
		j = 1
		while self.keep_searching():
			self.constant_draw()
			pygame.display.update()

			# Intelligent Sampling
			if self.n != None and i == (self.n + j*b):
				self.tree.grow_tree(random_sample=False)
				j = j + 1
			else:
				# Tree grows
				self.tree.grow_tree()
				
				new_node = self.tree.get_new_node()

				if not self.goal_found:
					if self.is_goal_reached(new_node, self.goal_node):
						self.goal_found = True
						self.n = i

						# new node is the final goal
						self.tree.set_goal(new_node)
						path = self.tree.compute_path()
				else:
					path = self.tree.path_optimization()

			i = i + 1
		return []

	def keep_searching(self):
		""" ."""
		# TODO ???
		if not self.goal_found:
			return True
		else:
			tree_size = self.tree.get_nodes_length()
			if tree_size > self.max_num_nodes:
				return False
			else:
				return True

	def is_goal_reached(self, n1, n2):
		distance = dist(n1.point, n2.point)
		if (distance <= self.goal_tolerance):
			return True
		return False


def main():
	XDIM = 500
	YDIM = 500
	WINSIZE = (XDIM, YDIM)
	MAX_NUM_NODES = 800
	MIN_NUM_NODES = 400
	pygame.init()
	# set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0)
	screen = pygame.display.set_mode(WINSIZE, pygame.RESIZABLE, 32)
	pygame.display.set_caption('RRT*-Smart Path Planning')
	screen.fill(WHITE)

	# Obstacles
	obs = Obstacles(screen, BLACK)
	obs.make_circle(150, 150, 50)
	obs.make_rect(250, 100, 50, 300)
	obs.draw()

	start_point = (50, 50)
	goal_point = (450, 450)
	goal_tolerance = 20
	obs_resolution = 5
	rrt_star_smart = RRTStarSmart(start_point, goal_point,
	                              MAX_NUM_NODES, MIN_NUM_NODES,
				                goal_tolerance, 0, 30, screen,
								obs, obs_resolution)

	path = rrt_star_smart.planning()
	pause = True
    # for e in pygame.event.get():
    #     if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
    #         sys.exit("Leaving because you requested it.")
    # pygame.display.update()

	while pause:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				quit()


if __name__ == '__main__':
    main()