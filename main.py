from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
import random  # For generating a verification code
from kivymd.uix.scrollview import MDScrollView
import os
import sqlite3
from datetime import datetime
import pandas as pd
from kivymd.uix.toolbar import MDTopAppBar
from kivy.utils import get_color_from_hex
from kivy.uix.image import AsyncImage  # Pour charger une image depuis une URL
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField
from geopy.geocoders import Nominatim
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.uix.switch import Switch
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
import shutil
from kivy.clock import Clock
from kivy.uix.label import Label
from kivymd.uix.filemanager import MDFileManager


class ConfirmationPage(Screen):
    def go_back(self):
        self.manager.current = "main_screen"
        print("Retour à l'écran principal.")
    pass


class ServiceSelectionScreen(Screen):
    # Définition de la classe ici
    pass


class ContentNavigationDrawer(MDBoxLayout):
    """Contenu du tiroir latéral."""


# Setting up the window size (optional)
Window.size = (400, 600)
# File to store the last used order number
ORDER_FILE = 'order_counter.txt'

KV = '''
ScreenManager:
    MainScreen:
    ProfileScreen:
    SettingsScreen:

<MainScreen>:
    name: "main"
    name: "home"
    BoxLayout:
        orientation: "vertical"

        MDBottomNavigation:
            MDBottomNavigationItem:
                name: "home"
                text: "Accueil"
                icon: "home"
                on_tab_press: app.switch_screen("home")
            MDBottomNavigationItem:
                name: "profile"
                text: "Profil"
                icon: "account"
                on_tab_press: app.switch_screen("profile")
            MDBottomNavigationItem:
                name: "settings"
                text: "Paramètres"
                icon: "cog"
                on_tab_press: app.switch_screen("settings")

<ProfileScreen>:
    name: "profile"
    BoxLayout:
        orientation: "vertical"
        MDLabel:
            text: "Écran Profil"
            halign: "center"
        MDBottomNavigation:
            MDBottomNavigationItem:
                name: "home"
                text: "Accueil"
                icon: "home"
                on_tab_press: app.switch_screen("home")
            MDBottomNavigationItem:
                name: "profile"
                text: "Profil"
                icon: "account"
                on_tab_press: app.switch_screen("profile")
            MDBottomNavigationItem:
                name: "settings"
                text: "Paramètres"
                icon: "cog"
                on_tab_press: app.switch_screen("settings")

<SettingsScreen>:
    name: "settings"
    BoxLayout:
        orientation: "vertical"
        MDLabel:
            text: "Écran Paramètres"
            halign: "center"
        MDBottomNavigation:
            MDBottomNavigationItem:
                name: "home"
                text: "Accueil"
                icon: "home"
                on_tab_press: app.switch_screen("home")
            MDBottomNavigationItem:
                name: "profile"
                text: "Profil"
                icon: "account"
                on_tab_press: app.switch_screen("profile")
            MDBottomNavigationItem:
                name: "settings"
                text: "Paramètres"
                icon: "cog"
                on_tab_press: app.switch_screen("settings")

MDScreen:
    MDNavigationLayout:
        ScreenManager:
            MDScreen:
                name: "main_screen"

                MDBoxLayout:
                    orientation: "vertical"

                    MDTopAppBar:
                        title: "Localisation & Services"
                        elevation: 10
                        md_bg_color: "blue"
                        left_action_items: [["menu", lambda x: app.toggle_navigation_drawer()]]
                        right_action_items: [["dots-vertical", lambda x: app.open_menu(x)]]

                    BoxLayout:
                        orientation: 'vertical'

                        MapView:
                            id: map_view
                            lat: 33.5897
                            lon: -7.6039
                            zoom: 6

                        MDBoxLayout:
                            id: form_box
                            orientation: 'vertical'
                            adaptive_height: True
                            padding: 10
                            spacing: 10

                            MDDropDownItem:
                                id: dropdown_item
                                text: "Select Service"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.menu.open()

                            MDTextField:
                                id: address_input
                                hint_text: "Address"
                                size_hint_x: 0.9
                                pos_hint: {"center_x": 0.5}
                                mode: "rectangle"

                            MDTextField:
                                id: price_input
                                hint_text: "Proposez votre prix"
                                size_hint_x: 0.9
                                pos_hint: {"center_x": 0.5}
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "Trouver un technicien"
                                size_hint: 0.8, None
                                height: "48dp"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.submit_form()

        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
'''


def get_next_order_number():
    """Fetches the next order number based on the previous number."""
    # Check if the file exists
    if os.path.exists(ORDER_FILE):
        with open(ORDER_FILE, 'r') as file:
            # Read the current order number
            current_order = int(file.read())
    else:
        # If file doesn't exist, start from 1
        current_order = 0

    # Increment the order number
    next_order = current_order + 1

    # Save the new order number back to the file
    #with open(ORDER_FILE, 'w') as file:
        #file.write(str(next_order))

    return next_order


class CommandeScreen(Screen):
    def __init__(self, numero_commande, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Logo
        self.logo = Image(source='1732469987007.jpeg', size_hint=(1, 0.3), allow_stretch=True)
        self.add_widget(self.logo)

        # Texte principal
        self.add_widget(Label(
            text='Votre commande a bien été enregistrée !',
            font_size='20sp',
            halign='center',
            size_hint=(1, 0.2),
            bold=True,
            color=(0, 0.5, 0.8, 1)
        ))

        # Icône avec texte explicatif
        self.thumb_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.thumb_layout.add_widget(Label(
            text='👍', font_size='30sp', size_hint=(0.2, 1),
        ))
        self.thumb_layout.add_widget(Label(
            text="Nous vous remercions pour votre confiance\net pour avoir choisi Materiel.net.",
            halign='left',
            font_size='16sp',
            valign='middle',
        ))
        self.add_widget(self.thumb_layout)

        # Numéro de commande
        self.add_widget(Label(
            text=f'Le numéro de votre commande : {numero_commande}',
            font_size='18sp',
            halign='center',
            size_hint=(1, 0.1),
        ))

        # Bouton de retour
        self.back_button = Button(
            text='Retour à l\'accueil',
            size_hint=(1, 0.1),
            background_color=(0, 0.5, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        self.back_button.bind(on_press=self.on_back_button_pressed)
        self.add_widget(self.back_button)
        #return numero_commande
    def on_back_button_pressed(self, instance):
        print("Retour à l'accueil ou action supplémentaire.")


class TechnicianCard(BoxLayout):
    def __init__(self, name, métier, price, image_url=None, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=120, padding=10, spacing=10, **kwargs)

        # Stocker les paramètres comme attributs d'instance
        self.name = name
        self.métier = métier
        self.price = price

        # Add the image to the left of the name
        if image_url:
            image = AsyncImage(
                source=image_url,
                size_hint=(0.2, 1),  # Adjust the image size
                allow_stretch=True
            )
        else:
            image = AsyncImage(
                source="default_profile.png",  # Use a default image if none provided
                size_hint=(0.2, 1),
                allow_stretch=True
            )
        self.add_widget(image)

        # Content for name and métier
        name_label = Label(
            text=f"[b]{name}[/b]\n{métier}",
            markup=True,
            color=get_color_from_hex("#333333"),
            size_hint=(0.4, 1)
        )
        self.add_widget(name_label)

        # Distance and price details
        details_label = Label(
            text=f"[b]{price}",
            markup=True,
            color=get_color_from_hex("#666666"),
            size_hint=(0.3, 1)
        )
        self.add_widget(details_label)

        # Add Accept and Reject buttons
        button_layout = BoxLayout(orientation="vertical", size_hint=(0.3, 1))
        accept_button = MDRaisedButton(text="Accepter", md_bg_color=(0, 0.8, 0, 1), pos_hint={"center_x": 0.5},
                                       on_release=self.accept_technician)

        button_layout.add_widget(accept_button)
        self.add_widget(button_layout)

    def accept_technician(self, *args):
        print(f"Technicien accepté: {self.name}, Métier: {self.métier}, Prix: {self.price}")
        # Fetch the next order number
        order_number = get_next_order_number()

        # Trigger screen transition to ConfirmationPage and pass the order number
        app = MDApp.get_running_app()
        confirmation_screen = app.screen_manager.get_screen("confirmation")
        confirmation_screen.update_order_number(order_number)
        app.screen_manager.current = "confirmation"



class TechnicianListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_service = None  # Attribute to store the selected service

        # Main layout
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # ScrollView for technician list
        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.technician_list = BoxLayout(orientation="vertical", size_hint_y=None, padding=10, spacing=10)
        self.technician_list.bind(minimum_height=self.technician_list.setter("height"))
        self.scroll_view.add_widget(self.technician_list)
        layout.add_widget(self.scroll_view)

        # Back button
        back_button = MDRaisedButton(
            text="Retour", size_hint=(0.3, None), height="48dp", pos_hint={"center_x": 0.5}, on_release=self.go_back
        )
        layout.add_widget(back_button)

        self.add_widget(layout)

        # Complete list of technicians
        self.technicians = [
            {"name": "Said", "métier": "Plombier", "price": "300 MAD",
             "image_url": "https://example.com/said.jpg"},
            {"name": "Mohamed", "métier": "Électricien", "price": "250 MAD",
             "image_url": "https://example.com/mohamed.jpg"},
            {"name": "Khalid", "métier": "Réparateur d'électroménager", "price": "280 MAD",
             "image_url": "https://example.com/khalid.jpg"},
            {"name": "Ali", "métier": "Plombier", "price": "320 MAD",
             "image_url": "https://example.com/ali.jpg"},
            {"name": "Sara", "métier": "Électricien", "price": "270 MAD",
             "image_url": "https://example.com/sara.jpg"},
        ]
        self.selected_service = None

        # Display technicians by default
        self.update_technician_list()

    def update_with_selected_service(self, service):
        """
        Updates the technician list based on the selected service.
        """
        self.selected_service = service
        print(f"Technician list updated for service: {self.selected_service}")
        self.update_technician_list()  # Update the list of technicians

    def update_technician_list(self):
        """Updates the technician list based on the selected service."""
        self.technician_list.clear_widgets()

        for tech in self.technicians:
            if self.selected_service is None or tech["métier"] == self.selected_service:
                card = TechnicianCard(
                    name=tech["name"],
                    métier=tech["métier"],
                    price=tech["price"],
                    image_url=tech.get("image_url")
                )
                self.technician_list.add_widget(card)
        return card.name, card.métier, card.price
    def go_back(self, instance):
        """Go back to the main screen."""
        self.manager.current = "main_screen"


class ContentNavigationDrawer(MDBoxLayout):
    """Contenu du tiroir latéral."""


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geolocator = Nominatim(user_agent="map_app")
        self.selected_service = None

        # Layout principal
        layout = BoxLayout(orientation="vertical", padding=1, spacing=1)

        # Barre supérieure
        self.toolbar = MDTopAppBar(title="TechniPro", elevation=4)
        layout.add_widget(self.toolbar)

        # Vue de la carte
        self.map_view = MapView(lat=33.5897, lon=-7.6039, zoom=7, size=(150, 150))
        self.map_view.bind(on_touch_up=self.on_map_touch)
        layout.add_widget(self.map_view)

        # Formulaire
        form_layout = BoxLayout(orientation="vertical", padding=5, spacing=5)

        # Utilisation de MDCard pour le style du spinner
        spinner_layout = MDCard(
            size_hint=(0.9, None),  # Largeur et hauteur
            height="60dp",
            padding=[10, 10, 10, 10],
            radius=[15, 15, 15, 15],  # Coins arrondis
            elevation=4,  # Ombre
            md_bg_color=(0.9, 0.9, 0.98, 1),  # Bleu clair
            pos_hint={"center_x": 0.5},  # Centrer
            orientation="horizontal",
        )
        self.service_spinner = Spinner(
            text="Sélectionner un service",
            values=["Plombier", "Électricien", "Réparateur d'électroménager"],
            background_color=(0.39, 0.12, 0.93, 1),  # Primary color
            color=(1, 1, 1, 1),  # White text color
        )
        self.service_spinner.bind(text=self.on_service_selected)
        spinner_layout.add_widget(self.service_spinner)
        form_layout.add_widget(spinner_layout)

        # Ajouter une icône
        icon_button = MDIconButton(
            icon="wrench",  # Icône pour les services
            theme_text_color="Custom",
            text_color=(0.1, 0.5, 0.8, 1),  # Bleu foncé
            size_hint=(None, None),
            size=(40, 40),  # Taille
        )


        # Champ d'adresse
        self.address_input = MDTextField(hint_text="Adresse", size_hint=(0.9, None), pos_hint={"center_x": 0.5})
        form_layout.add_widget(self.address_input)

        # Champ de prix
        self.price_input = MDTextField(hint_text="Proposez votre prix", size_hint=(0.9, None), pos_hint={"center_x": 0.5})
        form_layout.add_widget(self.price_input)

        # Bouton pour voir les techniciens
        go_to_technician_button = MDRaisedButton(
            text="Voir les techniciens",
            size_hint=(0.8, None),
            height="45dp",
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_technician_list,
        )
        form_layout.add_widget(go_to_technician_button)

        # Footer contenant les icônes
        footer_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(0.8, None),
            height="50dp",
            spacing=20,
            pos_hint={"center_x": 0.6}
        )

        # Ajouter les icônes en bas avec des couleurs personnalisées
        footer_layout.add_widget(MDIconButton(
            icon="home",
            #on_press=self.go_to_home,
            size_hint=(None, None),
            size=(45, 45),
            theme_text_color="Custom",  # Permet d'utiliser une couleur personnalisée
            text_color=(0.2, 0.6, 0.8, 1)  # Couleur bleu clair
        ))

        footer_layout.add_widget(MDIconButton(
            icon="cog",  # Icône de paramètres (gear)
            on_press=self.go_to_settings,
            size_hint=(None, None),
            size=(45, 45),
            theme_text_color="Custom",
            text_color=(0.8, 0.5, 0.2, 1)  # Couleur orange
        ))

        footer_layout.add_widget(MDIconButton(
            icon="information",
            on_press=self.go_to_about,
            size_hint=(None, None),
            size=(45, 45),
            theme_text_color="Custom",
            text_color=(0.3, 0.7, 0.3, 1)  # Couleur vert
        ))

        footer_layout.add_widget(MDIconButton(
            icon="account",
            on_press=self.go_to_profile,
            size_hint=(None, None),
            size=(45, 45),
            theme_text_color="Custom",
            text_color=(0.7, 0.2, 0.5, 1)  # Couleur violet
        ))

        # Ajouter le footer sous le bouton
        form_layout.add_widget(footer_layout)
        layout.add_widget(form_layout)

        # Ajouter tout au layout principal
        self.add_widget(layout)


    def go_to_home(self, instance):
        self.manager.current = "home"  # Stay on the home screen

    def go_to_settings(self, instance):
        self.manager.current = "settings"

    def go_to_about(self, instance):
        self.manager.current = "about"

    def go_to_profile(self, instance):
        self.manager.current = "profile"

    def on_service_selected(self, spinner, text):
        """
        Updates the selected service when the user selects one from the spinner.
        """
        self.selected_service = text if text != "Sélectionner un service" else None
        print(f"Service sélectionné : {self.selected_service}")

    def go_to_technician_list(self, instance):
        """
        Navigate to the technician list screen and pass the selected service.
        """
        if self.selected_service:
            technician_screen = self.manager.get_screen("technician_list_screen")
            technician_screen.update_with_selected_service(self.selected_service)
            self.manager.current = "technician_list_screen"
        else:
            print("No service selected.")

    def on_map_touch(self, instance, touch):
        """
        Handle map touch to get lat/lon and update the address field.
        """
        if instance.collide_point(touch.x, touch.y):
            lat, lon = self.convert_to_latlon(instance, touch.x, touch.y)
            marker = MapMarker(lat=lat, lon=lon)
            instance.add_marker(marker)
            self.update_address_input(lat, lon)

    def convert_to_latlon(self, mapview, touch_x, touch_y):
        lat = mapview.lat + (touch_y / mapview.height) * (mapview.zoom * 0.0001)
        lon = mapview.lon + (touch_x / mapview.width) * (mapview.zoom * 0.0001)
        return lat, lon

    def update_address_input(self, lat, lon):
        location = self.geolocator.reverse((lat, lon), language='en')
        if location:
            self.address_input.text = location.address
            print(f"Updated address input: {location.address}")
        else:
            self.address_input.text = "Address not found"
            print("Address not found")

    def update_map_from_address(self, address):
        try:
            location = self.geolocator.geocode(address)
            if location:
                self.map_view.lat = location.latitude
                self.map_view.lon = location.longitude
                self.map_view.zoom = 14
                self.update_address_input(location.latitude, location.longitude)
            else:
                print("Address not found")
        except Exception as e:
            print(f"Error updating map: {e}")

    def show_about_dialog(self):
        """
        Show about dialog with application details.
        """
        from kivymd.uix.dialog import MDDialog
        dialog = MDDialog(
            title="À propos",
            text="Application Map App v1.0\nDéveloppée par [Votre Nom].",
            size_hint=(0.8, None),
            buttons=[],
        )
        dialog.open()

class HomeScreen(Screen):
    pass
# Autres écrans (Paramètres, À propos, Profil)
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Title
        layout.add_widget(MDLabel(text="Settings", font_size=24, size_hint=(1, 0.1)))

        # Notifications Section
        notif_card = MDCard(size_hint=(0.9, None), height="100dp", pos_hint={"center_x": 0.5})
        notif_card.add_widget(MDLabel(text="Notifications", size_hint=(1, 0.4), halign="left"))
        notif_switch = Switch(active=True)  # Default to 'On'
        notif_card.add_widget(notif_switch)
        layout.add_widget(notif_card)

        # Language Selection
        language_card = MDCard(size_hint=(0.9, None), height="100dp", pos_hint={"center_x": 0.5})
        language_card.add_widget(MDLabel(text="Language", size_hint=(1, 0.4), halign="left"))
        language_spinner = Spinner(text="English", values=["English", "Arabic", "French"], size_hint=(1, 0.4))
        language_card.add_widget(language_spinner)
        layout.add_widget(language_card)

        # Dark Mode Section
        dark_mode_card = MDCard(size_hint=(0.9, None), height="100dp", pos_hint={"center_x": 0.5})
        dark_mode_card.add_widget(MDLabel(text="Dark Mode", size_hint=(1, 0.4), halign="left"))
        dark_mode_switch = Switch(active=False)  # Default to 'Off'
        dark_mode_card.add_widget(dark_mode_switch)
        layout.add_widget(dark_mode_card)

        # Save Button with Confirmation
        save_button = MDRaisedButton(text="Save Settings", size_hint=(1, 0.2))
        save_button.bind(on_press=self.save_settings)
        layout.add_widget(save_button)

        # Back to Home Button
        back_button = MDRaisedButton(text="Back to Home", size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_home)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def save_settings(self, instance):
        Snackbar(text="Settings Saved!", duration=2).open()

    def go_home(self, instance):
        self.manager.current = "main_screen"

class AccountScreen(Screen):
    def __init__(self, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)

        # Définir les champs pour le nom d'utilisateur et le numéro de téléphone
        self.username = ""  # Initialisez avec une valeur par défaut
        self.phone_number = ""  # Initialisez avec une valeur par défaut

        # Assurez-vous d'avoir un TextInput pour collecter ces données
        self.username_field = TextInput()  # Exemple de champ de texte pour le nom d'utilisateur
        self.phone_field = TextInput()  # Exemple de champ de texte pour le téléphone

        # Main layout
        self.layout = MDBoxLayout(orientation="vertical", padding=dp(20), spacing=dp(20))

        # Header section
        header = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(300), spacing=dp(10))
        header.padding = [dp(20), dp(20), dp(20), dp(20)]

        # Avatar Image
        avatar = Image(
            source="/chemin/vers/mon/image/avatar.png",  # Replace with your avatar image path
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            pos_hint={"center_x": 0.5},
        )
        header.add_widget(avatar)

        # Username field
        self.username_field = MDTextField(
            hint_text="Nom",
            text="John Doe",  # Default value
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
        )
        header.add_widget(self.username_field)

        # Phone number field
        self.phone_field = MDTextField(
            hint_text="Téléphone",
            text="+1234567890",  # Default value
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
        )
        header.add_widget(self.phone_field)

        # Add header to the main layout
        self.layout.add_widget(header)

        # Spacer to push content to the top
        spacer = MDBoxLayout(size_hint_y=1)  # Empty space
        self.layout.add_widget(spacer)

        # Buttons section
        buttons = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(150), spacing=dp(20))

        # Back button
        back_button = MDRaisedButton(
            text="Back to Home",
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={"center_x": 0.5},
        )
        back_button.bind(on_press=self.go_home)
        buttons.add_widget(back_button)

        # Save button
        save_button = MDRaisedButton(
            text="Save Changes",
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={"center_x": 0.5},
        )
        save_button.bind(on_press=self.save_changes)
        buttons.add_widget(save_button)

        # Add buttons section to the main layout
        self.layout.add_widget(buttons)

        # Add the main layout to the screen
        self.add_widget(self.layout)

    def update_profile(self, username, phone_number):
        """Update the username and phone number fields dynamically."""
        print(f"Updating profile: username={username}, phone_number={phone_number}")
        self.username = username
        self.phone_number = phone_number
        self.username_field.text = username
        self.phone_field.text = phone_number
        return {"username": self.username, "phone_number": self.phone_number}

    def save_changes(self, instance):
        """Save the changes made in the text fields."""
        username = self.username_field.text
        phone_number = self.phone_field.text
        print(f"Updated Profile - Name: {username}, Phone: {phone_number}")
        return username, phone_number

    def get_user_data(self):
        """Retourne le nom d'utilisateur et le téléphone saisis."""
        username = self.username_field.text
        phone_number = self.phone_field.text
        print(f"Données utilisateur récupérées - Nom: {username}, Téléphone: {phone_number}")
        return username, phone_number

    def on_user_data_change(self, username, phone_number):
        """Handle the user data change event."""
        print(f"Données modifiées : {username}, {phone_number}")
        # Bouton pour uploader l'image
        upload_button = MDRaisedButton(text="Upload Image", size_hint=(0.8, None), size=(200, 50),
                                       pos_hint={"center_x": 0.5})
        upload_button.bind(on_press=self.open_file_manager)
        self.layout.add_widget(upload_button)

        # Bouton pour enregistrer
        save_button = MDRaisedButton(text="Register", size_hint=(0.8, None), size=(200, 50), pos_hint={"center_x": 0.5})
        save_button.bind(on_press=self.register)
        self.layout.add_widget(save_button)

        # Ajout du layout à l'écran
        self.add_widget(self.layout)

        # Initialiser le gestionnaire de fichiers
        self.file_manager = MDFileManager(select_path=self.select_path, exit_manager=self.exit_file_manager,
                                          preview=True)


    def open_file_manager(self, instance):
        """Ouvrir le gestionnaire de fichiers pour choisir une image"""
        self.file_manager.show("/")  # Répertoire où ouvrir le gestionnaire


    def select_path(self, path):
        """Gérer le fichier sélectionné"""
        self.avatar.source = path  # Mettre à jour l'image de l'avatar avec le chemin de l'image choisie
        self.avatar.reload()  # Recharger l'image pour afficher la nouvelle image
        self.show_toast(f"Image selected: {path}")  # Afficher un message avec le chemin de l'image
        self.exit_file_manager()


    def exit_file_manager(self, *args):
       """Fermer le gestionnaire de fichiers"""
       self.file_manager.close()

    def go_home(self, instance):
        """Navigate back to the main screen."""
        self.manager.current = "main_screen"

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Title
        layout.add_widget(MDLabel(text="About TechniPro", font_size=24, halign="center"))

        # Description
        description_text = """TechniPro is a platform that connects users with qualified technicians in various technical fields. 
        We ensure reliable and secure services, focusing on user comfort and satisfaction."""
        layout.add_widget(MDLabel(text=description_text, font_size=16, halign="center", size_hint=(1, 0.4)))

        # Team Section
        layout.add_widget(MDLabel(text="Meet the Team", font_size=20, halign="center"))
        team_section = BoxLayout(orientation="horizontal", spacing=20, size_hint_y=None, height="120dp")
        team_section.add_widget(
            AsyncImage(source="https://example.com/team_member1.jpg", size_hint=(None, None), size=(80, 80)))
        team_section.add_widget(
            AsyncImage(source="https://example.com/team_member2.jpg", size_hint=(None, None), size=(80, 80)))
        layout.add_widget(team_section)
        # Credits Section
        credits_text = """Developed by:
- TechniPro Team
- Special thanks to contributors and open-source libraries."""
        layout.add_widget(MDLabel(text=credits_text, font_size=14, halign="center", size_hint=(1, 0.3)))

        # Version
        layout.add_widget(MDLabel(text="Version: 1.0.0", font_size=16, halign="center"))

        # Back Button
        back_button = MDRaisedButton(text="Back to Home", size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_home)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_home(self, instance):
        self.manager.current = "main_screen"

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.background = Rectangle(source="Photoroom-20241124_180513.png", size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.background.size = self.size
        self.background.pos = self.pos

    def on_enter(self):
        # Automatically switch to the WelcomeScreen after 4 seconds
        Clock.schedule_once(self.switch_to_welcome_screen, 3)

    def switch_to_welcome_screen(self, dt):
        self.manager.current = "welcome"


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)


        # Continue button with custom style like "Trouver un technicien"
        continue_button = MDRaisedButton(
            text="Continuer par téléphone",
            size_hint=(0.8, None),
            height="48dp",
            pos_hint={"center_x": 0.5},
            on_release=self.goto_next_screen,
            md_bg_color=(0, 0.749, 1, 1)  # Same color style as "Trouver un technicien"
        )
        layout.add_widget(continue_button)

        self.add_widget(layout)

    def goto_next_screen(self, instance):
        self.manager.current = "phone"


class PhoneScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.verification_code = None
        self.dialog = None  # Dialog instance for showing popups
        self.main_layout = BoxLayout(orientation="vertical")
        self.setup_phone_ui()
        self.add_widget(self.main_layout)

    def setup_phone_ui(self):
        self.top_layout = BoxLayout(orientation="vertical", padding=20, spacing=20, size_hint=(1, 0.8))

        # Add label "Enter your name"
        name_label = MDLabel(text="Entrer votre nom", font_size="20sp", halign="center", size_hint=(1, None), height=50)
        self.top_layout.add_widget(name_label)

        # Add text input for name
        self.name_input = MDTextField(
            hint_text="Nom complet",
            mode="rectangle",
            size_hint=(1, None),
            height="48dp",
            font_size="18sp"
        )
        self.top_layout.add_widget(self.name_input)

        # Add phone number label and input
        phone_label = MDLabel(text="Indiquez votre numéro", font_size="20sp", halign="center", size_hint=(1, None),
                              height=50)
        self.top_layout.add_widget(phone_label)

        self.phone_input = MDTextField(
            hint_text="Votre numéro",
            multiline=False,
            input_type="number",
            mode="rectangle",
            size_hint=(1, None),
            height="48dp",
            font_size="18sp"
        )
        self.top_layout.add_widget(self.phone_input)

        # Send code button
        send_button = MDRaisedButton(
            text="Envoyer le code",
            size_hint=(0.8, None),
            height="48dp",
            pos_hint={"center_x": 0.5},
            on_release=lambda _: self.send_verification_code(self.phone_input.text)
        )
        self.top_layout.add_widget(send_button)

        self.main_layout.add_widget(self.top_layout)

    def send_verification_code(self, phone_number):
        if len(phone_number) >= 9:
            self.verification_code = random.randint(1000, 9999)
            print(f"Code envoyé: {self.verification_code}")
            self.show_verification_ui()
        else:
            self.show_popup("Erreur", "Numéro de téléphone invalide.")

    def show_verification_ui(self):
        self.top_layout.clear_widgets()

        code_label = MDLabel(text="Code de vérification", font_size="20sp", halign="center", size_hint=(1, None), height=50)
        self.top_layout.add_widget(code_label)

        self.code_input = MDTextField(
            hint_text="Code",
            multiline=False,
            input_type="number",
            mode="rectangle",
            size_hint=(1, None),
            height="48dp",
            font_size="18sp"
        )
        self.top_layout.add_widget(self.code_input)

        verify_button = MDRaisedButton(
            text="Vérifier",
            size_hint=(0.8, None),
            height="48dp",
            pos_hint={"center_x": 0.5},
            on_release=lambda _: self.verify_code(self.code_input.text)
        )
        self.top_layout.add_widget(verify_button)

    def verify_code(self, input_code):
        if input_code.isdigit() and int(input_code) == self.verification_code:
            print("Vérification réussie")
            self.create_account()
        else:
            self.show_popup("Erreur", "Code incorrect.")

    def create_account(self):
        name = self.name_input.text
        phone = self.phone_input.text

        if name and phone:
            print(f"Compte créé pour {name} avec le numéro {phone}")

            # Mettre à jour l'écran de profil avec les infos utilisateur
            account_screen = self.manager.get_screen("profile")
            account_screen.update_profile(name, phone)

            # Passer à l'écran de profile
            self.manager.current = "profile"
        else:
            self.show_popup("Erreur", "Veuillez remplir tous les champs.")

    def show_popup(self, title, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title=title,
            text=message,
            size_hint=(0.8, 0.3),
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda _: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

class ConfirmationPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text="Confirmation Screen"))
        self.add_widget(layout)


class ConfirmationPage(Screen):
    def __init__(self, **kwargs):
        super(ConfirmationPage, self).__init__(**kwargs)
        self.name = "confirmation"  # Give the screen a name for navigation


        # ScrollView to allow scrolling if content exceeds screen size
        scroll_view = ScrollView()

        # Main container BoxLayout to hold the widgets
        main_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=Window.height)

        # Logo Image
        logo = Image(source='1732469987007.jpeg', size_hint=(1, 0.5))  # Replace with the correct logo path
        main_layout.add_widget(logo)

        # Confirmation Message
        confirmation_message = Label(
            text="Votre commande est enregistrée !",
            font_size='20sp',
            size_hint=(1, None),
            height=300,
            halign='center',
            color=(0, 0, 0, 1)
        )
        main_layout.add_widget(confirmation_message)

        # Thank You Message
        thanks_message = Label(
            text="Merci pour votre confiance.",
            font_size='18sp',
            size_hint=(1, None),
            height=40,
            halign='center',
            color=(0, 0, 0, 1)
        )
        main_layout.add_widget(thanks_message)

        # Automatically generated Order Number (sequential)
        self.order_number_input = TextInput(
            multiline=False,
            readonly=True,
            font_size='16sp',
            size_hint=(1, None),
            height=40,
            halign='center',
            background_color=(1, 1, 1, 0.7)
        )
        main_layout.add_widget(self.order_number_input)

        # MDRaisedButton for confirmation
        confirm_button = MDRaisedButton(
            text="Confirmer",
            size_hint=(1, None),
            height=50,
            on_press=self.on_confirm,
            md_bg_color=(0, 0.5, 1, 1),  # Button color (RGB + alpha)
            size_hint_min=(None, None),  # Ensures the button doesn't stretch
            font_size='16sp',
            pos_hint={"center_x": 0.5}  # Center the button horizontally
        )
        main_layout.add_widget(confirm_button)

        # Add the main layout to the scroll view and to the screen
        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)

        # Create database table if not exists
        self.create_table()

    def create_table(self):
        """Creates the commandes table if it doesn't exist."""
        conn = sqlite3.connect('commandes.db')
        cursor = conn.cursor()

        # Création ou mise à jour de la table
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS commandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_commande TEXT,
            client_nom TEXT,
            service_choisi TEXT,
            technicien TEXT,
            telephone TEXT,
            date_commande TEXT,
            total REAL
        )
        ''')
        conn.commit()
        conn.close()

    def update_order_number(self, order_number):
        """Updates the order number displayed on the screen."""
        self.order_number_input.text = str(order_number)

    def add_order_to_db(self, numero_commande, client_nom, service_choisi, technicien, telephone, total):
        """Adds a new order to the database."""
        conn = sqlite3.connect('commandes.db')
        cursor = conn.cursor()

        # Date et heure actuelles
        date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insertion des données dans la table
        cursor.execute('''
        INSERT INTO commandes (numero_commande, client_nom, service_choisi, technicien, telephone, date_commande, total)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (numero_commande, client_nom, service_choisi, technicien, telephone, date_commande, total))

        conn.commit()
        conn.close()

    def exporter_vers_excel(self):
        """Exporte toutes les commandes de la base de données vers un fichier Excel."""
        try:
            conn = sqlite3.connect('commandes.db')
            cursor = conn.cursor()

            # Récupérer toutes les données de la table commandes
            cursor.execute('SELECT * FROM commandes')
            rows = cursor.fetchall()

            # Colonnes pour le fichier Excel
            colonnes = ['ID', 'Numéro Commande', 'Nom Client', 'Service Choisi', 'Technicien', 'Téléphone',
                        'Date Commande', 'Total']

            # Convertir les données en DataFrame pandas
            df = pd.DataFrame(rows, columns=colonnes)

            # Exporter les données dans un fichier Excel
            df.to_excel('TechniPro.xlsx', index=False, engine='openpyxl')
            print("Données exportées dans TechniPro.xlsx")

        except PermissionError:
            print("Erreur : Impossible d'écrire dans le fichier 'TechniPro.xlsx'. Assurez-vous qu'il n'est pas ouvert.")

        except Exception as e:
            print(f"Une erreur inattendue s'est produite : {e}")
    def on_confirm(self, instance):
        """Handles the confirmation of the order."""

        account_screen=AccountScreen()
        phone_screen = PhoneScreen()


        # Récupération des données utilisateur
        username, phone_number = account_screen.get_user_data()  # Appel à la méthode get_user_data

        # Vérification que les données ont bien été saisies
        if username and phone_number:  # Vérifie que les deux champs ne sont pas vides
            # Assignation aux variables client_nom et telephone
            client_nom = username
            telephone = phone_number

            # Affichage des résultats
            print("Nom du client :", client_nom)
            print("Numéro de téléphone :", telephone)
        else:
            print("Les données utilisateur sont incomplètes.")

        # Example of order details (these would be dynamically set from user input)
        service_choisi = "Plombier"
        technicien = "Ali"
        total = 300.0
        numero_commande = "123456"  # This would be dynamically generated

        # Save the order to the database
        self.add_order_to_db(numero_commande, client_nom, service_choisi, technicien, telephone, total)

        # Update the order number in the confirmation screen
        self.update_order_number(numero_commande)

        # Export to Excel
        self.export_to_excel()

    def add_order_to_db(self, numero_commande, client_nom, service_choisi, technicien, telephone, total):
        """Add order to the database."""
        conn = sqlite3.connect('commandes.db')
        cursor = conn.cursor()

        # Get the current date and time
        date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert the order into the database
        cursor.execute('''
        INSERT INTO commandes (numero_commande, client_nom, service_choisi, technicien, telephone, date_commande, total)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (numero_commande, client_nom, service_choisi, technicien, telephone, date_commande, total))

        conn.commit()
        conn.close()

    def export_to_excel(self):
        """Exports orders from the database to an Excel file."""
        try:
            conn = sqlite3.connect('commandes.db')
            cursor = conn.cursor()

            # Fetch all orders from the database
            cursor.execute('SELECT * FROM commandes')
            rows = cursor.fetchall()

            # Define the columns for the Excel file
            columns = ['ID', 'Numéro Commande', 'Nom Client', 'Service Choisi', 'Technicien', 'Téléphone', 'Date Commande', 'Total']

            # Convert the data to a pandas DataFrame
            df = pd.DataFrame(rows, columns=columns)

            # Export the data to Excel
            df.to_excel('TechniPro_Orders.xlsx', index=False, engine='openpyxl')
            print("Data successfully exported to TechniPro_Orders.xlsx")

        except Exception as e:
            print(f"Error exporting to Excel: {e}")


        print("Commande confirmée et exportée avec succès !")
        self.manager.current = "main_screen"


class TechniProApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()


        # Configuration des écrans
        self.sm = ScreenManager()
        self.sm.add_widget(ServiceSelectionScreen(name="service_selection_screen"))
        # Add the screens to the manager
        self.screen_manager.add_widget(SplashScreen(name="splash_screen"))
        self.screen_manager.add_widget(WelcomeScreen(name="welcome"))
        self.screen_manager.add_widget(PhoneScreen(name="phone"))
        #self.screen_manager.add_widget(RegistrationScreen(name="RegistrationScreen"))
        self.screen_manager.add_widget(MainScreen(name="main_screen"))

        self.screen_manager.add_widget(SettingsScreen(name="settings"))
        self.screen_manager.add_widget(AboutScreen(name="about"))
        self.screen_manager.add_widget(AccountScreen(name="profile"))  # Add AccountScreen here
        self.screen_manager.add_widget(AccountScreen(name="account_screen"))
        self.screen_manager.add_widget(TechnicianListScreen(name="technician_list_screen"))
        # In your MyApp class:
        self.commande_screen = CommandeScreen(numero_commande="123456789")
        self.screen_manager.add_widget(self.commande_screen)

        account_screen = self.screen_manager.get_screen("account_screen")
        print(f"[ScreenManager] AccountScreen instance: {account_screen}")
        # Add the ConfirmationPage screen to the screen manager
        confirmation_page = ConfirmationPage()
        self.screen_manager.add_widget(confirmation_page)

        return self.screen_manager

    def go_to_technician_list(self):
        """
        Passe à l'écran de la liste des techniciens et transmet le service sélectionné.
        """
        service_screen = self.sm.get_screen("service_selection_screen")
        technician_screen = self.sm.get_screen("technician_list_screen")

        selected_service = service_screen.get_selected_service()
        if selected_service:
            technician_screen.update_with_selected_service(selected_service)
            self.sm.current = "technician_list_screen"  # Change l'écran
        else:
            print("Aucun service sélectionné.")

    def load_technicians(self, dt):
        technicians = [
            {"name": "Said", "métier": "plombier", "distance": "1.0 km", "price": "300 MAD"},
            {"name": "Mohamed", "métier": "électricien", "distance": "0.6 km", "price": "250 MAD"},
            {"name": "Khalid", "métier": "réparateur", "distance": "1.2 km", "price": "280 MAD"},
            {"name": "Ali", "métier": "Plombier", "distance": "0.8 km", "price": "320 MAD",
             "image_url": "https://example.com/ali.jpg"},
            {"name": "Sara", "métier": "Électricien", "distance": "1.5 km", "price": "270 MAD",
             "image_url": "https://example.com/sara.jpg"},
        ]
        # Update the technician list on the TechnicianListScreen
        technician_screen = self.screen_manager.get_screen("technician_list_screen")
        technician_screen.update_technicians(technicians)

    def toggle_navigation_drawer(self):
        self.root.ids.nav_drawer.set_state("toggle")

    def open_menu(self, caller):
        pass  # Fonctionnalité de menu contextuel à ajouter si nécessaire

    def built(self):

        return Builder.load_string(KV)


        # Set primary color theme
        self.theme_cls.primary_palette = "Purple"

        # Create an AccountScreen instance
        account_screen = AccountScreen()

        # Update profile data
        account_screen.update_profile("Alice Doe", "+9876543210")

        return account_screen
        # Set primary color theme
        self.theme_cls.primary_palette = "Blue"

        # Create a RegistrationScreen instance
        #registration_screen = RegistrationScreen()

        #return registration_screen

if __name__ == "__main__":
    TechniProApp().run()
