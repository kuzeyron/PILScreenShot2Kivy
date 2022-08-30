from io import BytesIO

from kivy.clock import Clock, mainthread
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty, NumericProperty
from kivy.uix.image import Image
from Xlib.display import Display
from PIL import ImageGrab

__all__ = ('shoot', 'Shoot')

Builder.load_string('''
<Shoot>:
    allow_stretch: True
    keep_ratio: False
    canvas.after:
        Color:
            rgba: 1, 1, 1, int(root.show_cursor)
        Rectangle:
            size:
                root.cursor_size, \
                root.cursor_size
            pos: root.cursor_pos
            source: 'assets/icons/cursor.png'
''')


def shoot(*largs):
    cached_screenshot = BytesIO()
    img = ImageGrab.grab(all_screens=True)
    img.save(cached_screenshot, format='png')
    cached_screenshot.seek(0)

    texture = CoreImage(
        cached_screenshot,
        ext='png'
    ).texture

    return texture


class Shoot(Image):
    cursor_pos = ListProperty((0, 0))
    cursor_size = NumericProperty('20dp')
    show_cursor = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.frame, 0)

    @mainthread
    def frame(self, *largs):
        self.texture = shoot(self.size)

        if self.show_cursor:
            Clock.schedule_once(self.cursor_position, 0)

        Clock.schedule_once(self.frame, 0)

    def cursor_position(self, pos, *largs):
        """ Calculate position from python-xlib
            and translate into Widget size """

        disp = Display()
        screen = disp.screen()

        pos = screen.root.query_pointer()._data
        pos = pos['root_x'], pos['root_y']

        tsize = self.texture_size
        norm = self.norm_image_size
        x = pos[0] / tsize[0] * norm[0]
        y = pos[1] / tsize[1] * norm[1]
        invert_y = self.height - y

        self.cursor_pos = x, invert_y - self.cursor_size


if __name__ == '__main__':
    from kivy.app import App

    class TestApp(App):
        def build(self):
            return Shoot()
    TestApp().run()
