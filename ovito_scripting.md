-  Ref: https://ovito.org/manual/python/introduction/running.html
- Command   
  - ovito # GUI
  - ovitos script.py # command line
    - The RHS sample code reads snap000000.xyz, snap0010000.xyz, ... and produces image0000000.png, image0010000.png, ... files

```python
from ovito.io import * 
from ovito.vis import * 
import math

def main():

    for n in range(0,100000,10000):
        fname = 'snap' + '%07d' % n + '.xyz' 
        #  snap00000000.xyz, snap0010000.xyz, ....
        node = import_file(fname, columns =["Particle Type", 
                                            "Position.X", 
                                            "Position.Y", 
                                            "Position.Z", 
                                            "My Property"])

        vp = Viewport() 
        vp.type = Viewport.Type.PERSPECTIVE 
        vp.camera_pos = (-5, -8, 4)
        vp.camera_dir = (2, 3, -3)
    
        vp.fov = math.radians(60.0) 
        settings = RenderSettings()
        settings.filename = 'image' + '%07d'%n +'.png'
        settings.size = (800, 600) 
    
        node.add_to_scene()
        vp.render(settings)

if __name__ == '__main__':    
    main()
```
