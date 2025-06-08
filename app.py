# image_downloader_gui.py

import os
import sys
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock

# Importa a classe de lógica do arquivo separado
sys.path.append(os.path.dirname(__file__)) # Garante que o diretório atual está no PATH
from func import UnsplasherFunc

kivy.require('2.0.0')

Window.size = (500, 650)

class Unsplasher(App):
    app_status_text = StringProperty("Bem-vindo ao Image Downloader!")
    downloader = ObjectProperty(None)
    login_attempts = 0

    # Referências para os TextInputs e Labels
    app_password_input = ObjectProperty(None)
    cfg_app_password_input = ObjectProperty(None)
    cfg_api_key_input = ObjectProperty(None)
    cfg_master_password_input = ObjectProperty(None)
    filter_input = ObjectProperty(None)
    dest_input = ObjectProperty(None)
    total_img_input = ObjectProperty(None)
    download_status_label = ObjectProperty(None)

    def build(self):
        # Passa o método de popup da GUI para a classe de lógica
        self.downloader = UnsplasherFunc(show_popup_callback=self._show_kivy_popup)
        self.root_layout = BoxLayout(orientation='vertical')

        # Armazena os layouts de cada tela
        self.login_screen_layout = self._create_login_screen()
        self.config_screen_layout = self._create_config_screen()
        self.main_screen_layout = self._create_main_screen()

        # Inicia com a tela de login ou configuração
        self.show_screen(self.login_screen_layout)

        # Tenta carregar as configurações ao iniciar
        Clock.schedule_once(self.initial_config_check, 0.1)

        return self.root_layout

    def _show_kivy_popup(self, title, message):
        """Método da GUI para exibir popups Kivy."""
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.4))
        popup.open()

    def show_screen(self, screen_layout):
        """Alterna entre as telas da aplicação."""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(screen_layout)

    def initial_config_check(self, dt):
        """Verifica se o arquivo de configuração existe ao iniciar o app."""
        if not os.path.exists(self.downloader.config_path):
            self.show_screen(self.config_screen_layout)
            self.app_status_text = "Arquivo de configuração não encontrado. Por favor, configure o aplicativo."
        else:
            self.show_popup_input("Senha Mestra", "Digite sua senha mestra para descriptografar:", self.verify_master_password_on_load, password=True)

    def _create_login_screen(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        layout.add_widget(Label(text="Login do Image Downloader", font_size='24sp', size_hint_y=None, height=50))
        
        layout.add_widget(Label(text="Senha do Aplicativo:", size_hint_y=None, height=30))
        self.app_password_input = TextInput(
            hint_text="Digite sua senha do aplicativo",
            password=True,
            multiline=False,
            font_size='18sp',
            size_hint_y=None, height=50
        )
        layout.add_widget(self.app_password_input)

        login_button = Button(
            text="Entrar",
            font_size='20sp',
            size_hint_y=None, height=60,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        login_button.bind(on_press=self.verify_app_password)
        layout.add_widget(login_button)
        
        config_button = Button(
            text="Configurações",
            font_size='16sp',
            size_hint_y=None, height=50,
            background_color=(0.7, 0.7, 0.7, 1)
        )
        config_button.bind(on_press=lambda x: self.show_screen(self.config_screen_layout))
        layout.add_widget(config_button)

        layout.add_widget(Label(text="", size_hint_y=1))

        return layout

    def verify_master_password_on_load(self, popup, master_pass_input):
        if not master_pass_input:
            self._show_kivy_popup('Erro', 'Senha mestra é necessária para descriptografar. Saindo.')
            App.get_running_app().stop()
            return

        if self.downloader.config_loader(master_pass_input):
            self._show_kivy_popup("Sucesso", "Configurações carregadas com sucesso! Faça login.")
            self.show_screen(self.login_screen_layout)
        else:
            self._show_kivy_popup("Erro", "Falha ao carregar configurações. Verifique a senha mestra.")
            App.get_running_app().stop()

    def verify_app_password(self, instance):
        entered_password = self.app_password_input.text
        if entered_password == self.downloader.password:
            self._show_kivy_popup("Sucesso", "Login efetuado com sucesso!")
            self.show_screen(self.main_screen_layout)
            self.app_password_input.text = ""
        else:
            self.login_attempts += 1
            self._show_kivy_popup("Erro de Login", f"Senha incorreta. Tentativa: {self.login_attempts}/{self.downloader.max_login_attempts}")
            if self.login_attempts >= self.downloader.max_login_attempts:
                self._show_kivy_popup("Bloqueado", "Muitas tentativas. Tente novamente mais tarde.")
                App.get_running_app().stop()

    def _create_config_screen(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        layout.add_widget(Label(text="Configurações", font_size='24sp', size_hint_y=None, height=50))

        layout.add_widget(Label(text="Senha do Aplicativo (para login):", size_hint_y=None, height=30))
        self.cfg_app_password_input = TextInput(
            hint_text="Defina uma senha para o aplicativo",
            password=True,
            multiline=False,
            font_size='18sp',
            size_hint_y=None, height=50
        )
        layout.add_widget(self.cfg_app_password_input)

        layout.add_widget(Label(text="Sua API Key do Unsplash:", size_hint_y=None, height=30))
        self.cfg_api_key_input = TextInput(
            hint_text="Cole sua API Key aqui",
            multiline=False,
            font_size='18sp',
            size_hint_y=None, height=50
        )
        layout.add_widget(self.cfg_api_key_input)
        
        layout.add_widget(Label(text="Senha Mestra (para criptografia):", size_hint_y=None, height=30))
        self.cfg_master_password_input = TextInput(
            hint_text="Defina uma senha mestra (para criptografar as configs)",
            password=True,
            multiline=False,
            font_size='18sp',
            size_hint_y=None, height=50
        )
        layout.add_widget(self.cfg_master_password_input)

        save_button = Button(
            text="Salvar Configurações",
            font_size='20sp',
            size_hint_y=None, height=60,
            background_color=(0.3, 0.7, 0.2, 1)
        )
        save_button.bind(on_press=self.save_configurations)
        layout.add_widget(save_button)

        back_to_login_button = Button(
            text="Voltar para Login",
            font_size='16sp',
            size_hint_y=None, height=50,
            background_color=(0.7, 0.7, 0.7, 1)
        )
        back_to_login_button.bind(on_press=lambda x: self.show_screen(self.login_screen_layout))
        layout.add_widget(back_to_login_button)
        
        layout.add_widget(Label(text="", size_hint_y=1))

        return layout

    def save_configurations(self, instance):
        app_pass = self.cfg_app_password_input.text
        api_key_val = self.cfg_api_key_input.text
        master_pass = self.cfg_master_password_input.text

        if not app_pass or not api_key_val or not master_pass:
            self._show_kivy_popup("Erro ao Salvar", "Todos os campos de configuração são obrigatórios!")
            return

        if self.downloader.save_config(app_pass, api_key_val, master_pass):
            # Limpa os campos após salvar
            self.cfg_app_password_input.text = ""
            self.cfg_api_key_input.text = ""
            self.cfg_master_password_input.text = ""
            self.show_screen(self.login_screen_layout)

    def _create_main_screen(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        layout.add_widget(Label(text="Filtro de Pesquisa:", size_hint_y=None, height=30))
        self.filter_input = TextInput(
            hint_text="Ex: paisagem, carros, comida",
            multiline=False,
            font_size='18sp',
            padding_y=[(50 - 18) / 2.0, 0],
            size_hint_y=None, height=50
        )
        layout.add_widget(self.filter_input)

        layout.add_widget(Label(text="Pasta de Destino:", size_hint_y=None, height=30))
        self.dest_input = TextInput(
            hint_text="Caminho da pasta de download (Ex: C:/Imagens)",
            multiline=False,
            font_size='18sp',
            padding_y=[(50 - 18) / 2.0, 0],
            size_hint_y=None, height=50
        )
        layout.add_widget(self.dest_input)
        select_dest_button = Button(
            text="Selecionar Pasta",
            size_hint_y=None, height=40,
            background_color=(0.5, 0.5, 0.5, 1),
            font_size='16sp'
        )
        select_dest_button.bind(on_press=self.open_file_dialog)
        layout.add_widget(select_dest_button)

        layout.add_widget(Label(text="Total de Imagens (máx. 1000):", size_hint_y=None, height=30))
        self.total_img_input = TextInput(
            hint_text="Ex: 100",
            input_type='number',
            multiline=False,
            font_size='18sp',
            padding_y=[(50 - 18) / 2.0, 0],
            size_hint_y=None, height=50
        )
        layout.add_widget(self.total_img_input)

        download_button = Button(
            text="Iniciar Download",
            font_size='22sp',
            size_hint_y=None, height=70,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        download_button.bind(on_press=self.start_download_process)
        layout.add_widget(download_button)

        self.download_status_label = Label(
            text="Aguardando início do download...",
            font_size='16sp',
            size_hint_y=None, height=40,
            color=(0.8, 0.8, 0.8, 1)
        )
        layout.add_widget(self.download_status_label)

        logout_config_button = Button(
            text="Logout / Alterar Configurações",
            font_size='16sp',
            size_hint_y=None, height=50,
            background_color=(0.8, 0.4, 0.2, 1)
        )
        logout_config_button.bind(on_press=self.go_to_config_or_logout)
        layout.add_widget(logout_config_button)

        return layout
    
    def go_to_config_or_logout(self, instance):
        self.filter_input.text = ""
        self.dest_input.text = ""
        self.total_img_input.text = ""
        self.download_status_label.text = "Aguardando início do download..."
        self.login_attempts = 0
        self.show_screen(self.login_screen_layout)

    def open_file_dialog(self, instance):
        self.show_popup_input("Selecionar Pasta", "Digite o caminho completo da pasta de destino:", self.set_dest_folder_from_input)

    def set_dest_folder_from_input(self, popup, folder_path):
        if folder_path:
            self.dest_input.text = folder_path
            self._show_kivy_popup("Pasta Selecionada", f"Pasta definida para: {folder_path}")
        else:
            self._show_kivy_popup("Aviso", "Nenhuma pasta selecionada.")

    def update_download_status(self, message):
        self.download_status_label.text = message

    def start_download_process(self, instance):
        search_filter = self.filter_input.text
        dest_folder = self.dest_input.text
        total_images = self.total_img_input.text
        
        # O self.update_download_status é passado como um callback
        self.downloader.download(search_filter, dest_folder, total_images, self.update_download_status)

    def show_popup_input(self, title, message, callback, password=False):
        content_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content_layout.add_widget(Label(text=message, size_hint_y=None, height=40))
        input_text = TextInput(multiline=False, password=password, size_hint_y=None, height=50)
        content_layout.add_widget(input_text)
        
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        ok_button = Button(text="OK", background_color=(0.2, 0.7, 0.3, 1))
        cancel_button = Button(text="Cancelar", background_color=(0.8, 0.2, 0.2, 1))
        button_layout.add_widget(ok_button)
        button_layout.add_widget(cancel_button)
        content_layout.add_widget(button_layout)

        popup = Popup(title=title, content=content_layout, size_hint=(0.8, 0.5))

        def on_ok(instance):
            popup.dismiss()
            callback(popup, input_text.text)
        
        def on_cancel(instance):
            popup.dismiss()
            callback(popup, None)

        ok_button.bind(on_press=on_ok)
        cancel_button.bind(on_press=on_cancel)
        
        popup.open()


if __name__ == "__main__":
    Unsplasher().run()