from base64 import encodebytes
from IPython.lib.latextools import latex_to_png
import sys
import subprocess

color = 'White'

def set_latex_color(new_color):
    global color
    color = new_color
def mathcat(data, meta):
    global color
    png = latex_to_png(f'$${data}$$'.replace('\\displaystyle', '').replace('$$$', '$$'), color=color)
    imcat(png, meta)

def imcat(image_data, metadata):
    icat = subprocess.Popen(
            ['kitty', 'icat'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
    icat.stdin.write(image_data);
    icat.stdin.close()

    image_kgp_command = icat.stdout.read()
    sys.stdout.buffer.write(image_kgp_command)

def register_mimerenderer(ipython, mime, handler):
    ipython.display_formatter.active_types.append(mime)
    ipython.display_formatter.formatters[mime].enabled = True
    ipython.mime_renderers[mime] = handler

def load_ipython_extension(ipython):
    register_mimerenderer(ipython, 'image/png', imcat)
    register_mimerenderer(ipython, 'text/latex', mathcat)
