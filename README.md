# Ink2canvas

Ink2canvas is an Inkscape extension written in Python that exports SVG files to HTML5 canvas.


## How to Install

If you want a system wide install, copy **ink2canvas.py**, **ink2canvas.inx** and */lib* directory to */usr/share/inkscape/extensions* folder (or similar), if you have permission.
If not, put files **ink2canvas.py**, **ink2canvas.inx**  and */lib* directory in local Inkscape extensions folder:  *$HOME/.config/inkscape/extensions*.

In the seconde case, you will have to copy from */usr/share/inkscape/extensions/* the following Python modules to your folder: **inkex.py**, **simplepath.py**, **simpletransform.py** and **simplestyle.py**.


## How to use:
Open Inkscape file and choose HTML5 output option at "Save as" menu.

    
## Project Map

### TODO
* Add missing path commands
* Refactor and fix style methods error handling
* Get clip paths (initial) and masks to work
* Radial Gradient 
* Group style must prevail over grouped objects
* Linear gradient (initial)
* Clones

### Working
* Lines, rects, circles, ellipses, paths (partial), texts (basic)
* Polylines and polygons
* Basic text attributes support
* Fill and stroke
* Transformation matrix (translating, rotating, scaling, etc)
* Iterating through groups and layers
