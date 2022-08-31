from io import BytesIO

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty, NumericProperty
from kivy.uix.image import Image
from PIL import ImageGrab
from Xlib.display import Display

__all__ = ('Shoot', )

Builder.load_string('''
<Shoot>:
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


class Shoot(Image):
    active = BooleanProperty(True)
    allow_stretch = BooleanProperty(True)
    cursor_pos = ListProperty((0, 0))
    cursor_size = NumericProperty('20dp')
    keep_ratio = BooleanProperty(False)
    show_cursor = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._bytesio = BytesIO()
        Clock.schedule_once(self._frame, 0)

    def get_screenshot(self, *largs):
        img = ImageGrab.grab(all_screens=True)
        img.save(self._bytesio, format='png')
        self._bytesio.seek(0)

        texture = CoreImage(
            self._bytesio,
            ext='png'
        ).texture
        self._bytesio.seek(0)
        self._bytesio.flush()

        return texture

    def _frame(self, *largs):
        if self.active:
            self.texture = self.get_screenshot()

            if self.show_cursor:
                self.cursor_pos = self.cursor_position()

            Clock.schedule_once(self._frame, 0)

    def cursor_position(self, *largs):
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

        cursor_pos = x, invert_y - self.cursor_size

        return cursor_pos


if __name__ == '__main__':
    from kivy.app import App

    class TestApp(App):
        def build(self):
            return Shoot()
    TestApp().run()
