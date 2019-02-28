# Hnefatafl AI Project

Project by: Kasen Chaque, Michael Robertson, and Henry Smith.

Project for: UCI CS 178 Intro to Machine Learning Final Project

# About the Game

Hnefatafl translates to "The King's Table" and is an ancient game played by the Vikings. There are many different versions of Hnefatafl and for this project we went with the 7x7 Brandubh variation. The specific ruleset we are using is Variation 1 from this website: http://www.dragonheelslair.com/en/rulesbrandubh.php

# Our Approach to AI

*Unfinished*
Training: Create some number of randomized neural networks that take in the state of the board and output the likelyhood that Black will will (so the likelyhood that White will win is just 1 - P(Black wins)). The AI makes decisions based on a min-max tree with all possible moves as branches and the neural network at the leaf nodes to rate each board state (tree is AB pruned for efficiency). Train these networks by pitting the AIs agaisnt eachother, killing off the least-winningest networks and reproducing the winners with mutations.

Testing: Not Sure Yet
