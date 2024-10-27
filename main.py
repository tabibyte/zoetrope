# main.py
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
import os

class GalleryApp(App):
    def build(self):
        # Main layout
        layout = BoxLayout(orientation='vertical')
        
        # Add scrollable gallery layout
        scroll_view = ScrollView()
        gallery_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        gallery_layout.bind(minimum_height=gallery_layout.setter('height'))
        
        # Load images
        images_folder = "images/"
        for img_file in os.listdir(images_folder):
            if img_file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img_path = os.path.join(images_folder, img_file)
                thumbnail = AsyncImage(source=img_path, size_hint_y=None, height=200)
                gallery_layout.add_widget(thumbnail)

        # Add the grid layout to the scroll view and scroll view to the main layout
        scroll_view.add_widget(gallery_layout)
        layout.add_widget(scroll_view)
        
        return layout

if __name__ == "__main__":
    GalleryApp().run()
