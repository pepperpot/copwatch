from cairo import Context, SVGSurface
from math import pi

# Create a GTK+ widget on which we will draw using Cairo
class CairoWidget:

    def __init__(self, Surface = None):
        if Surface == None:
            Surface = SVGSurface
        
        self.Surface = Surface
    
    def draw(self, cr, width, height, **kwargs):
        # Fill the background with gray
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.rectangle(0, 0, width, height)
        cr.fill()


def draw_widget(dest, Widget, Surface = SVGSurface, width = 100, height = 100, **kwargs):
    """
    Convenience function to output CairoWidget to a buffer
    """
    widget = Widget(Surface)
    surface = widget.Surface(dest, width, height)
    widget.draw(My_Context(surface), width, height, **kwargs)
    surface.finish()

class My_Context(Context):

  def rounded_rect(self, x, y, width, height, rnd):
        self.move_to(x + rnd, y)
        self.arc(x + width-rnd, y + rnd, rnd, 1.5*pi, 2*pi)
        self.arc(x + width-rnd, y + height-rnd, rnd, 0, 0.5*pi)
        self.arc(x + rnd, y + height-rnd, rnd, 0.5*pi, pi)
        self.arc(x + rnd, y + rnd, rnd, pi, 0.5*pi)
        self.fill()
