from kivy.app import App

from libs.screenshot import Shoot
# from libs.textrequest import message_to_x11


class TestApp(App):

    def build(self):
        return Shoot()


if __name__ == '__main__':
    TestApp().run()
