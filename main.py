# main.py
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage, Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scatter import Scatter
import os

class GalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        scroll_view = ScrollView()
        self.gallery_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        self.gallery_layout.bind(minimum_height=self.gallery_layout.setter('height'))
        
        self.images_folder = "images/"
        self.image_paths = [os.path.join(self.images_folder, img_file)
                            for img_file in os.listdir(self.images_folder)
                            if img_file.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        # Load images and create thumbnails with click events
        for idx, img_path in enumerate(self.image_paths):
            thumbnail = AsyncImage(source=img_path, size_hint_y=None, height=200)
            thumbnail.bind(on_touch_down=lambda instance, touch, idx=idx: self.show_fullscreen(touch, idx))
            self.gallery_layout.add_widget(thumbnail)

        scroll_view.add_widget(self.gallery_layout)
        layout.add_widget(scroll_view)
        self.add_widget(layout)

    def show_fullscreen(self, touch, index):
        if touch.is_double_tap:
            fullscreen_screen = self.manager.get_screen('fullscreen')
            fullscreen_screen.show_image(self.image_paths, index)
            self.manager.current = 'fullscreen'

class FullScreenImageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = BoxLayout(orientation='vertical')
        self.back_button = Button(text="Back", size_hint_y=None, height=50)
        self.back_button.bind(on_release=self.go_back)
        self.layout.add_widget(self.back_button)
        
        # Scatter widget for zooming and panning
        self.scatter = Scatter(do_rotation=False, do_translation=True, do_scale=True)
        self.full_image = Image()
        self.scatter.add_widget(self.full_image)
        
        # Add the scatter widget to layout
        self.layout.add_widget(self.scatter)
        self.add_widget(self.layout)
        
        self.image_paths = []
        self.current_index = 0

    def show_image(self, image_paths, index):
        self.image_paths = image_paths
        self.current_index = index
        self.full_image.source = self.image_paths[self.current_index]
        
        # Reset scale and center the scatter to center the image
        self.scatter.scale = 1
        self.scatter.center = self.center  # Center the scatter widget on screen

    def go_back(self, instance):
        self.manager.current = 'gallery'

    def on_touch_move(self, touch):
        # Detect swipe and handle accordingly
        if touch.dx > 50:
            self.show_previous_image()
        elif touch.dx < -50:
            self.show_next_image()

    def show_next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.show_image(self.image_paths, self.current_index)

    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image(self.image_paths, self.current_index)

class GalleryApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GalleryScreen(name='gallery'))
        sm.add_widget(FullScreenImageScreen(name='fullscreen'))
        return sm

if __name__ == "__main__":
    GalleryApp().run()
