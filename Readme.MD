# Purpose
- Slides or documentation of various topics


- Please check each page shown in the left for the details of each SW. This page describes common steps of running main applications.

<hr>

# Sample Linux command for industrial applications

## Ansys workbench
- `runwb2`
- `runwb2 -oglmesa` # using mesa as SW rendering
  - Or check: https://studentcommunity.ansys.com/thread/runtime-errors-on-centos-7-system/)
	- `export LD_LIBRARY_PATH+=/ansys_inc/v192/Framework/bin/Linux64/Mesa`
	- `export LIBGL_ALWAYS_INDIRECT=1`
	- `export LIBGL_ALWAYS_SOFTWARE=1`

## Ansys APDL/Launcher
- Classical Ansys MECHANICAL APDL
	- copy /ansys_inc/v192/ansys/data/models/CrankSlot_Flexible.inp 
	- Command: `ansys192 -np 2 -i CrankSlot_Flexible.inp > log.out`
		- file.rst, file.db will be produced
	- Command: launcher -> Select PrepPost from License -> Click run
		- In the menu, General Postproc -> Results Viewer -> Select file.rst

## Fluent
- Find Fluent\tutorials\Introductory\Modeling Flow Through porous.zip and unzip
- Steps
	- `fluent 3d -g`                                                       # run fluent 3d  without grahics
		- file/read-case-data catalytic_converter.cas.gz # read input
		- it 10                                                                  # do 10 iterations
		- wcd "aaa.cas"                                               # save as aaa.cas
		- exit                                                                   # exit fluent terminal
	- `fluent 3d`                                                          # open as GUI
		- File-> Read -> Case & Datat -> select aaa.cas
		- Click Postprocessing tab -> Graphics zone -> Contours -> Select velocity or Pressure
		- If OpenGL graphics crashes, use software rending as `fluent 3d -driver x11`

## HFSS
- GUI command: ansysedt
		- It may take > 1 min for the first run
	- Steps
		- copy /ansoft/AnsysEM19.1/Linux64/Examples/HFSS/RF\ Microwave/coaxial_resonator.aedt
		- `ansysedt -distributed -machinelist numcores=2 -auto -monitor -ng -batchsolve -batchoptions "HFSS/HPCLicenseType=pool tempdirectory=/tmp" coaxial_resonator.aedt`
		- `ansysedt`  # GUI, open coaxial_resondator and Check Filed Overlays

## Abaqus
- CAE command: `abaqus cae`
- When HW rendering fails, use SW rendering: abaqus cae -mesa
- Steps
	- `abaqus fetch job=lap*.inp` # extracting a sample input
	- `abaqus j=lap_joint inter cpus=2` (or 4, 8, 16, 32)
		- Using htop, check if cpus are used as many as requested
		- Took 86 sec in 2 CPUs of Broadwell
	- `abaqus cae`
		- Open lap_joint.odb and visualize

## COMSOL
- Copy /comsol/comsol54/applications/Heat_Transfer_Module/Heat_Exchangers/heat_exchanger_iso.mph
- Steps
	- `comsol batch -nn 1 -np 1 -inputfile heat_exchanger_iso.mph -outputfile aaa.mph`
		- Batch command using 1 cpu
	- `comsol`
		- GUI. Open aaa.mph and check Results -> Temperature

## MATLAB
- Run `matlab` and check the GUI opens or not
	- Run `bench` in the MATLAB comand interface
    - This will test CPU speed and 3d graphics
- Possible issues
	- Compatibility with JAVA
		- Try JDK from OS or JAVA engine from SUN
	- Graphics issue
		- When HW rendering fails, run matlab as *matlab -softwareopengl* with SW rendering

## TECPLOT
- Command:
	- `tec360`
- If HW rendering fails, SW rendering can be used with -mesa
	- `tec360 -mesa`
	- Note that SW rendering is much slower than HW rendering
