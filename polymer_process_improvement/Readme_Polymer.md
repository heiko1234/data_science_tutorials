
# Szenario

You work as Data Scientist in a chemical compony that produces white plastic granulate and supplies it to a molding plant, where it is made into white plastic die castings.

However, the molding proess goes through intermittent phases when its product quality drops, leading to yield losses at both the polymer and the molding plant.

When a crisis occurs, teams are formed to tackle the problem, but the problem usually disappears for no apparent reasons.

**You** are selected to solve another mysterious crisis. 

**You** and your small proect team decided to concentrate on two characterists (Ys) that are of special importance:

- **MFI**: melt flow index
- **CI**: color index


## What are we going to learn?

We will go through the odyssey of this project, with its highs and lows step by step.

We will have a look into the cost savings of the project.


## Szenario Details

All effots to find the root cause of low yields in both plants have been failed so far. Now, a new crises happens and need a fast solution.


### Manufacturing Process

Producing white plastic die castings is not easy and needs the right balance of whiteness and flow. As the ratio of additives in the mixing process is increased to mke the plastic granulate white, the flow of the plastic is impaired (decreased).

The process can be devided into 3 steps:

- Filler preparation
- Polymerization
- Granulation + Packaging

![process](./schema/manufacturing_process.jpg)

### Filler preparation

A white filler, which is an inert powder. It is mixed with unpurified river water in a stirred tank. 
The filler preparation tank is steady mixed and held at target concentration.
The content gets refilled / appendixed each day with filler and water, as well as small amounts of a ciscosity modifier if the iscosity gets to high.


### Polymerizatin

The polymierization process is a batch process, while the plant is running 24h every day with 3 batches a day.
Clear polymere can be done by heating and stirring a monomer until it polymerizes. The white polymer is created by adding filler slurry to the reaction start into the polymerization reaction vessel.


### Granulation of Polymer
When the polymerization reaction is complete, the molten polymer is granulated and packed.


### Analytics

The process is very well quality controlled. For each batch of polymer a sample is taken and tested:

- **color** (whiteness), CI
- **MFI**, the MFI is offline measured and will indicate how well the polymer will be processed in the down-stream plant
- **filler content** of the polymer


## Project Team

You have contact to:

- polymer plant quality manager
- polymer technical support chemist
- process engineer at the down-stream plant


## Crisis


