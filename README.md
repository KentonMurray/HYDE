HYDE
====
This is a HYbrid Disk discrete Event simulator (HYDE) for modeling RAID 0, 1, and 5 arrays on a POSIX filesystem. 
The underlying disks in the RAID arrays can be either HDDs or SSDs (aka hybrid disk).
The project allows one to vary the ratio of underlying HDD/SSD disks for a range of simulations.
The goal of this project is to make a simple and lightweight discrete event simulator. So, 
it does not have as much functionality as larger systems, but should instead be useful for scaling up
quick, proof-of-concept experiments in minutes. The aim is to create shorter ramp up and learning requirements
so that someone without any discrete event simulation experience can get going as soon as possible.
One nice aspect of HYDE is that it allows for stochastic generation of experiments
This project is the outcome of a small portion of a group project, for a graduate level university class ...
so we apologize in advance for any issues as this is just student code. The three main contributors are:
https://github.com/antonisa, https://github.com/aargueta2, and https://github.com/KentonMurray

HYDE is split into three main components: Workloads, RAID, and Disks. The workloads are either stochastic or
deterministic POSIX requests for Read, Write, and Delete. The RAID Controller implements three common RAID levels. 
The Disks simulate actual physical HDD and SSD drives (complete with failures).

The filesystem itself is a abstracted away and all commands are sent directly to the RAID controller using POSIX commands.
Look at demo.py and demo2.py in the src/ for examples on how to run experiments.

