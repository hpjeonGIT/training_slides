# Changing license server from the client
- In windows laptop
- Edit c:\Program files \Abaqus\6.8.x\site\abaqus_v6.env
- abaquslm_license_file="XXXX@YYY.abc.org" into new one

# N. of license tokens
- http://optimaldevice.com/blog/abaqus-licensing/
- 1cpu core takes 5 tokens
- 2cpu core job takes 6 tokens
- T = INT (5*N^0.422)
  - CLI for license check in Linux: abaqus licensing ru

# When scratch space is required
- Run from /tmp to /work/$account
  - In CAE, Analysis-> Jobs-> Create, then edit “General” tab
  - in CLI, abaqus scratch=/work/$USER j=aaa int

# Abaqus runs background, and this could be a problem in PBS batch queue
- Use “interactive” command to prevent this: abaqus j=aaa int

# When GUI looks weird (or message are becomes gray)
- Delete ~/abaqus_v6.14.gpr then reload abaqus CAE

# Plug-in installation
- Users may ask to install 3rd party plugins
  - Just unzip them at abaqus/6.xxx/code/python2.7/lib/abaqus_plugins
  - Double-check if the plugin appears in the GUI menu
  - The menu may change per functionality wise
  - CAE -> VIEW or only at analysis mode etc.

# User subroutine in Linux
- Make sure that you have fortran compiler enabled: default is ifort
- abaqus j=inp_name user=myForSub
- Read *.log file, and check: Begin Compiling Abaqus/Standard User Subroutines
- Sample file: $ abaqus fetch j=boltpipeflange_3d_usr_umat

# Fortran compiler options
- Check SimulationServices/V6R2017x/linux_a64/SMA/site/lnx86_64.env
- License is registered in custom_v6.env:abaquslm_license_file="port@server"
  - In windows, check C:\Program Files\Dassault Systemes\SimulationServices\V6R2017x\win_b64\SMA\site\win86_64.env

# Using intel compiler 2017 and vs2013 at abaqus 2017 on windows
- Edit Abaqus Command icon: "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2017\windows\bin\ifortvars.bat" intel64 vs2013 & C:\windows\system32\cmd.exe /k
- Edit Abaqus CAE icon: "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2017\windows\bin\ifortvars.bat" intel64 vs2013 & C:\SIMULIA\CAE\2017\win_b64\resources\install\cae\launcher.bat cae || pause

# Using abaqus in windows
- abaqus verify -all # verify installed abaqus
- Linux command:  abaqus j=aaa inp=bbb user=ccc cpus=12
- Windows command: abaqus –j aaa –inp bbb –user ccc –cpus 12

# Parallel computing in abaqus
- abaqus j=input cpus=4 mp_mode=threads (or MPI)
  - MPI runs only on iterative solver. Edit #step as #step, solver=iterative

# GPU run
- abaqus j=test gpus=1
  - To monitor GPU usage, nvidia-smi -l

# Running double precision
- abaqus j=aaa double cpus=...

# Installing scipy 
- Download Linux binary wheel of scipy 0.9 (0.10.1 works as well) from PyPi
- Unzip
- Copy scipy folder to SIMULIA/CAE/2017/linux_a64/tools/SMApy/python2.7/lib/python2.7/site-packages
- Copy or make a static link the same scipy into SimulationServices/V6R2019x/linux_a64/tools/SMApy/python2.7/lib/python2.7/site-packages SIMULIA/Tosca/2019/linux_a64/tools/SMApy/python2.7/lib/python2.7/site-packages
  - match the version of scipy with built-in numpy of abaqus. Find the version made in similar time
  - EX: in abaqus 2019, numpy.__version__ = 1.6.2 => May 2012 => scipy 0.10.1 as of Feb 2012

# In Python scripting
## Face vs FaceArray
- A=mdb.models['Case_1'].parts['Monarch_Pipette'].faces.getSequenceFromMask(('[#1200 ]', ), ) 
- B = A[0:1]
- mdb.models[Model_Name].parts[Part_Name].Surface(name='Load_Contact',side1Faces= B)
  - There might NOT be a constructor of FaceArray
  - Instead of A[0], use A[0:1], keeping the sequence
## Find nearby edges
- tmp = instance.edges.findAt(((ix,iy,0),)) # id = tmp[0].index
- next = tmp[0].getAdjacentEdges() # find nearby edges of edge "tmp"
```python
for x in next:
	p1 = x.getVertices()[0]  # 1st point of nearby edge
	p2 = x.getVertices()[1]  # 2nd point of nearby edge
	x1 =  instance.vertices[p1].pointOn[0][0] #x coord of 1st point
	y1 = instance.vertices[p1].pointOn[0][1]

tmp = instance.vertices.findAt(((ix,iy,0),))
next = tmp[0].getEdges()
for seg in next:
    if not (seg in indices_seam_edges):
        edges += instance.edges[seg:seg+1]
```

## Find a crack seam
```python
seam_edges = seam_edges + assembly.sets['Crack Seam ' + str(i)].edges;
indices_seam_edges = []
for seg in seam_edges:
    indices_seam_edges.append(seg.index)

tmp = instance.edges.findAt(((ix,iy,0),)) # id = tmp[0].index
next = tmp[0].getAdjacentEdges()
for seg, n in zip(next,range(len(next))):
    if not (seg.index in indices_seam_edges):
        edges += next[n:n+1]
```

# Installing Abaqus 2019
- only ksh: bash/sh not working
- The SIMUIA Established product installers aborts with an error message both in GUI and Command line (TUI) mode with the following error message:
- ERROR: Cannot wait for process "/<Abaqus_Installer_directory_path>/AM_SIM_Abaqus_Extend.AllOS/1/inst/linux_a64/code/bin /DSYInsAppliGUI" "-CDpath" "/<Abaqus_Installer_directory_path>/AM_SIM_Abaqus_Extend.AllOS/1/"
- Workaround: The workaround is to set the size of stack limit from unlimited to "10240".
- sh/ksh/bash shell: $ ulimit -s 10240
- csh/tcsh shell: $ limit stacksize 10m (where 10m=10240 KB)
- ksh rpm must be installed
- On a serial file system. Unpacking on Lustre could be an issue - media check fails.

# Section defintion for 2D
- Do not use generalized plane strain. This may yield an error of node set assembly not defined
- Use Homogeneous and select 2D in the option
	- Thickness can be adjusted in the option
 
 # Environmental variables
 - abaqus information=environment # displays current configuration
 - Ex) export ABA_SINT_CAP=65536

# Feeding hostnames
- In Abaqus 2017 or newer, $PBS_NODEFILE seems to be recognized while 6.14-* may have issues.
- Ref: https://hpc.utm.my/index.php/services/available-software/abaqus/
- Prepare abaqus_v6.env in the CWD, containing "mp_host_list=[['aaa.server.com',8],['bbb.server.com',8]]
```bash
for n in $(sort -u $PBS_NODEFILE); do
mp_host_list="${mp_host_list}['$n',$(grep -c $n $PBS_NODEFILE)],"
done
mp_host_list=$(echo ${mp_host_list} | sed -e "s/,$/]/")
echo "mp_host_list=[${mp_host_list}" > abaqus_v6.env
```

# Python scripting
- abaqus cae nogui=script.py
- Doing re-partitions may decrease the performance. Draw segment-wise in CAD or sketch steps

# RDMA error 
- Error message: multiple pkey found in partition key table, please choose one via MPI_IB_PKEY
- Or: MPI_Init: Can't initialize RDMA device
- or: Cannot initialize RDMA protocol
- Solution
	- export MPI_IB_PKEY=0xffff
	- For multiple nodes, hardcode *export MPI_IB_PKEY=0xffff* into .bashrc and .bash_profile
	
# Plotting data along path
- Extracting nodal number in sequene of 5,3,2 ... might not be easy
- Draw a line segment in advance, and pick up points, which exist already
```python
key_list = output.rootAssembly.nodeSets.keys()
if 'Some Edges' in key_list:
    path1 = session.Path(name='Path-1', type=POINT_LIST,
                 expression=((0,1.1,0), (0,-1.1,0)))
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='S', outputPosition=INTEGRATION_POINT, 
        refinement=(INVARIANT, 'Pressure'))
    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1) # first step is 0, second step is 1
    v1 = (('S', INTEGRATION_POINT, ((INVARIANT, 'Pressure' ), )),) 
    newXYData=session.XYDataFromPath(name='sectiondata',
                                     path=path1,\
                                     includeIntersections=TRUE,\
                                     shape=UNDEFORMED,\
                                     labelType=Y_COORDINATE,
                                     pathStyle=UNIFORM_SPACING,
                                     numIntervals=200,
                                     variable=v1)
    session.writeXYReport(fileName="section_pressure.txt", xyData=(newXYData,))
```
