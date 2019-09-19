## Introduction to VisIt
- Visualization program
- Developed by Lawrence Livermore National Laboratory
	- User group at ORNL
- OpenSource
- Competing with paraview
- For POST-processing
	- Not for pre-processing: Not mesher!
- Batch job capability
	- Using system python

## Features
- All kinds of plotting
	- 2D bar/line/histogram chart
	- 2D/3D Mesh
		- Mesh data from commercial/open source FEM/FVM
	- Particle Data
		- Good rendering image using molecular dynamics schema
		- But could be very slow compared to Ovito if rendering is used
- Can generation movie/animation

## Command
- visit
- visit -np 6 # Using MPI

## VisIt vs. Paraview
- VisIt
	- Developed by LLNL
	- Main (?) file format: Silo 
	- Legacy VTK format support
	- Load the assigned data only
		- Efficient memory usage
	- batch processing through visit command line
		- No graphics required
	- Can render MD particles
	- But very heavy
	- Distributed parallel visualization using XDMF, Silo
	- Faster than Paraview in unstructured particle drawing
	- Can load FLUENT CAS
	- Static load balancing only (?)
		- allowdynamic may not work well
- Paraview
	- Developed by Kitware
	- Main (?) file format: VTK
	- Some Silo format support
	- Load all the data in the memory
		- You may need big memory
	- pvpython/pvbatch for batch process
		- Still xwindows required
	- No MD but particle plot
	- Distributed parallel visualization using XDMF, VTM, Silo
	- Can load FLUENT CAS
	- D3 filter for dynamic load balancing

## Tracing
- Steps
  - Controls -> Commands
  - Click Record
  - Do some operations in the GUI
  - Click Stop in the commands window
  - Operations are recorded in the Commands window
- Copy and save as a python script
	- Add “import sys” at top and “sys.exit() at bottom
- Run as *visit -cli -nowin -s test.py*
- http://www.visitusers.org/index.php?title=VisIt-tutorial-Python-scripting

## Visualizing processor ID when MPI is running
- How to display procid
- Menu -> Controls -> Launch CLI
	- In the CLI, Enter:
	- `DefineScalarExpression(“procid”, “procid(Mesh)”)`
	- `Addplot(“Pseudocolor”, “procid”)`
	- procid will be shown in Pseudocolor menu

## Distributed visualization of VisIt
- Dynamic load balancing seems NOT working
	- visit -allowdynamic
- Static load balancing works but models must be partitioned in the beginning
- There are two modes to run VisIt as parallel
	- Using Host
		- Local host or other nodes
		- Similar to pvserver of Paraview
	- Locally
		- Assigning NCPUS from the command line
		- Command: visit –np 4
	- mpirun must use the built-in binary of VisIt package
		- visit_install_dir/version/linux-x86_64/bin must be included in the path
		- vist_install_dir/version/linux_x86_bin/lib for LD_LIBRARY_PATH
- Silo files might be used for distributed visualization
	- Sample file: /usr/nic/apps/visit/2.13.2/data/multi_ucd3d.silo
- HDF5 + xdmf might be recommended
  - Ref: http://www.xdmf.org/index.php/XDMF_Model_and_Format
