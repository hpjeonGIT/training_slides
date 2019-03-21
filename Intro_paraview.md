## Introduction to ParaView
- Visualization program
- Developed by Kitware
- OpenSource
- Competing with VisIt (developed by LLNL)
- For POST-processing
	- Not for pre-processing: Not mesher!
- Multiple processor support
	- mpiexec is included in binary distribution
	- But not for multiple nodes
- Batch job capability
	- pvbatch/pvpython

## Feature
- All kinds of plotting
	- 2D bar/line/histogram chart
	- 2D/3D Mesh
		- Mesh data from commercial/open source FEM/FVM
	- Particle Data
		- Not rendered as sphere image
- User customization
	- Paraview must be built from source package
- Can generation movie/animation

## VTK file format
- Standard files for ParaView
- Supported in many other visualization programs as well
- ASCII or binary
- Can define particles, meshes of 2D/3D
- VTM
	- Multi-block version of VTK
		- This is different from legacy VTK
		- XML format
		- Actual data are stored in the linked VTU or other partitioned files
	- VTU
		- XML VTK file format for unstructured grid
- Examples
		- Read some data (xmf or CAS) then save as vtm in Paraview using ASCII format
```bash
$ more ccc.vtm
<VTKFile type="vtkMultiBlockDataSet" version="1.0" byte_order="LittleEndian" header_type="UInt64">
  <vtkMultiBlockDataSet>
    <Piece index="0" name="Grid_2">
      <DataSet index="0" file="ccc/ccc_0_0.vtu">
      </DataSet>
      <DataSet index="1" file="ccc/ccc_0_1.vtu">
      </DataSet>
    </Piece>
  </vtkMultiBlockDataSet>
</VTKFile>
```
```bash
$ more ccc/ccc_0_0.vtu 
<VTKFile type="UnstructuredGrid" version="2.0" byte_order="LittleEndian" header_type="UInt64">
  <UnstructuredGrid>
    <Piece NumberOfPoints="5000" NumberOfCells="5000">
      <PointData Scalars="dmg" GlobalIds="___D3___GlobalNodeIds">
        <DataArray type="Float64" Name="dmg" format="ascii" RangeMin="0" RangeMax="0">
          0 0 0 0 0 0
          0 0
        </DataArray>
        <DataArray type="UInt8" Name="vtkGhostType" format="ascii" RangeMin="0" RangeMax="0">
…
```

## Multi-core visualization
- Settings -> General -> Multi-core support -> Adjust core numbers
- Close paraview and restart
- Load file. Then go to Filters -> D3
- Some file formats might not be supported

## Tracing
- Similar to VB in Excel or journaling in FEM packages
- Edit the script and rerun as *pvbatch --use-offscreen-rendering batch.py*
	- pvbatch is a customized python by ParaView, enclosed in the pre-built package
	- 4.0 has a bug and re-locate “WriteImage()” function to the bottom

## Batch/distributed visualization
- Not recommended but use it at your own risk
	- VisIt would be recommended for batch distributed visualization
- Recompilation of source might be necessary
- Add server/connect allows only one node connection
- For multiple nodes connection, write a pvsc file and “load servers”
- Prepare .pvsc file and “load servers”
```xml
<Servers>
<Server name="case1" resource="cs://server1.aaa.bbb//server2.ccc.ddd">
    <ManualStartup />
 </Server>
</Servers>
```
