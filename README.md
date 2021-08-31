# fourchem
Spatial artificial chemistry

This project is about artificial life and artificial chemistry. Among the questions that arise in the artificial life community is the question: can systems exhibiting the characteristics of living systems exist in any medium other than the biochemistry that we find on our planet? Are there some specific features of real chemistry that are essential for life?  How far can we abstract away from real chemistry and still have a system in which life of some kind can exist?

Many artificial chemistries have been designed which abstract away some features of real chemistry. I’m interested in spatial artificial chemistries. Can we find a system of rules for interacting particles in space which is rich enough to support life-like systems, yet simple enough to be computationally tractable?

The system that I’m working on has the following properties, arrived at from experience of working on other similar systems (see www.srm.org.uk), and from working on so-called unconventional computing systems in which space and geometry are important.

- 4 atom types
- Atoms are symmetrical - no preferred direction
- Simple Repel-attract-repel interaction based on distance between particles, so that: atoms don’t overlap (repel), nearby atoms stick to each other (attract), molecules tend to avoid sticking to each other (repel)

I’m working with 2D space initially, in order to get a feel for how the system behaves and what kinds of structures can be built with it. I think that a 3D system will be needed in order to build more complex machines.

The 4 atom types are:
- Insulator : does nothing
- Exciter : outputs a signal
- Wire : allows signals to propagate
- Thruster : exerts force if signal received

Wires are designed so that signals propagate in one direction along a joined up string of wire particles. Wires work by having 3 states: quiescent, excited, depleted. A quiescent wire becomes excited if an excited wire, or an Exciter, is within a distance of 3R. An excited wire becomes depleted after 1 time step. A depleted wire becomes quiescent after 1 time step.

I believe that this system can be used to implement any logical function using a combination of wires and ‘mechanical logic’ - this hasn’t been demonstrated yet.

Running some simulations with random initial states shows some of the behaviours that I’m looking for:

- Structures form from aggregations of particles
- Structures tend to avoid each other usually, but sometimes they coalesce
- Sometimes a structure will break up into smaller structures

