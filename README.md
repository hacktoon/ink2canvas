# Ink2canvas

Ink2canvas is an Inkscape extension written in Python that exports SVG to HTML5 Canvas. It aims on providing a way to ease the creation of Canvas graphics by avoiding writing Javascript code by hand through Inkscape drawing interface. It also provides a standalone script to generate Canvas code without Inkscape.

## Project files
* **ink2canvas** - This folder holds the project main files:
    * **main.py** - Reads and parse the SVG file, creating objects and calling the respective methods to handle it.
    * **canvas.py** - A class responsible for producing Canvas code.
    * **svg.py** - Abstracts SVG elements parsed by the main.py file.
    * **lib/** - This folder contains some Python modules provided by Inkscape and useful for building extensions. These are being used just for development and testing, so it is recomended in a production enviroment to use the already provided by the system.
* **ink2canvas.inx** - A XML file that describes the interface between Inkscape and the extension. It must be put in the */extensions* folder to Inkscape be aware of this extension.
* **standalone.py** - This script was created initially to test the extension. It runs the project code without needing to open Inkscape. It must be provided a SVG file path as input and optionally a output file path.

## How to install on Inkscape
If you want a system wide install, put just the file **ink2canvas.inx** and the folder **ink2canvas** at */usr/share/inkscape/extensions* folder (or similar), if you have permission to do this. Alternatively, you can put the files in the local Inkscape extensions folder:  *$HOME/.config/inkscape/extensions* (or similar).

NOTE: the Python modules in the *lib/* folder already exists in the Inkscape system wide extension folder. For now, the *lib/* and *ink2canvas/* folders were created for the sake of the project organization, so if you want to use the system modules, you have to change the import path in the files and/or put all files in the *extensions* folder, which isn't a recomended solution.


## How to use:
**Extension**

Open Inkscape file and choose "HTML5 output" option at "Save as" menu.

**Standalone**

python standalone.py INPUT [OUTPUT]

OUTPUT can be defined as dash (-) for stdout output.

You can find good SVG sample files at [Croczilla](http://croczilla.com/bits_and_pieces/svg/samples).
    
## Project Map

### TODO
* Add missing path sub-commands
* Refactor and fix style methods error handling
* Masks
* Radial Gradient 
* Group style must prevail over grouped objects
* Linear gradient (initial)
* Clones
* Images
* Patterns

### Working
* Lines, rects, circles, ellipses, paths (partial), text (basic)
* Polylines and polygons
* Basic text attributes support
* Fill and stroke
* Clips (needs more tests :-)
* Transformations (translating, rotating, scaling, etc)
* Iterating through groups and layers
