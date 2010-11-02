# Ink2canvas

Ink2canvas is an Inkscape extension written in Python that exports SVG files to HTML5 canvas.


## How to Install

If you want a system wide install, copy **canvas.py** and **canvas.inx** to */usr/share/inkscape/extensions* folder (or similar), if you have permission.
If not, put files **canvas.py** and **canvas.inx** in local Inkscape extensions folder:  *$HOME/.config/inkscape/extensions*
You will have to copy these Inkscape Python modules to that folder: **inkex.py**, **simplepath.py** and **simplestyle.py**. They may be found in this project at lib/ folder.


## How to use:
Open Inkscape file and choose HTML5 output option at "Save as" menu.

    
## Project Map

### TODO
* Add text properties support
* Add missing path commands
* Refactor and fix style methods error handling
* Create polylines and polygons methods
* Get clips and masks to work
* Transform matrix data handling (translating, rotating, scaling, etc)

### Working
* Rects, circles, ellipses, paths (partial), text (basic)
* Fill and stroke, gradient (initial)
* Iterating through groups and layers

## Contributors

* PotHix

