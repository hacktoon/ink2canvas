# -*- encoding: utf-8 -#-

"""
This script runs Ink2Canvas without needing to open Inkscape
"""

from ink2canvas.main import Ink2Canvas
import sys

i2c = Ink2Canvas()

#catch first argument
try:
    svg_input = sys.argv[1]
except IndexError:
    print "Provide a SVG file to be parsed.\n"
    print "Usage: python standalone.py INPUT [OUTPUT]\n"
    print "For stdout use dash (-) as OUTPUT."
    sys.exit()

#catch optional second argument for output file
try:
    html_output = sys.argv[2]
except IndexError:
    html_output = "%s.html" % svg_input.replace(".svg", "")

#creates a svg element tree
i2c.parse(svg_input)

#applies the extension effect
i2c.effect()

if html_output != '-':
    output_file = open(html_output, "w")
else:
    output_file = sys.stdout
#get the html code
content = i2c.core.canvas.output()
output_file.write(content.encode("utf-8"))
output_file.close()
