import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

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
        
        # Load images as thumbnails
        for img_path in self.image_paths:
            thumbnail = AsyncImage(size_hint_y=None, height=200)
            thumbnail.source = img_path  # Set the source for the image
            thumbnail.bind(on_touch_down=lambda instance, touch, index=self.image_paths.index(img_path): self.show_fullscreen(touch, index))
            self.gallery_layout.add_widget(thumbnail)

        scroll_view.add_widget(self.gallery_layout)
        layout.add_widget(scroll_view)
        self.add_widget(layout)

    def show_fullscreen(self, touch, index):
        if touch.is_double_tap:
            fullscreen_screen = self.manager.get_screen('fullscreen')
            fullscreen_screen.show_image(self.image_paths, index)
            self.manager.current = 'fullscreen'

class FullscreenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()  # Use FloatLayout for flexible positioning
        
        self.image_display = AsyncImage(size_hint=(1, 1))
        layout.add_widget(self.image_display)

        # Create a smaller back button
        back_button = Button(text="Back", size_hint=(None, None), size=(100, 40), pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_release=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def show_image(self, image_paths, index):
        self.image_display.source = image_paths[index]
        self.image_display.reload()

    def go_back(self, instance):
        self.manager.current = 'gallery'  # Switch back to the gallery screen

class GalleryApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GalleryScreen(name='gallery'))
        sm.add_widget(FullscreenScreen(name='fullscreen'))
        return sm

if __name__ == '__main__':
    GalleryApp().run()
