import requests
import os
import json
from cryptography.fernet import Fernet # Import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode, b64decode

class UnsplasherFunc:
    def __init__(self, show_popup_callback=None):
        self.user = os.getlogin()
        self.api_key = ""  # User's API KEY
        self.dest = ""  # Save Location
        self.password = ""  # Password
        self.base = f"C:/Users/{user}/Documents/.img-down/config"  # config.json default directory
        self.config_path = os.path.join(self.base, "config.json")
        self.url = f"https://api.unsplash.com/search/photos?query={filtro}&client_id={api_key}" # Unsplash API URL
        self.response = requests.get(url)
        self.salt_path = os.path.join(base, 'salt.salt') # Salt must be persistent for the same password generate the same key
        self.fernet_key = None
        self.max_attempts = 3
        
    def _show_popup(self, title, message):
        if self.show_popup_callback:
            self.show_popup_callback:(title, message)
        else:
            print(f'POPUP (Logica): {title} - {message}')

    def mkdir(self, dest): # Creates a directory based on "base"
        if not os.path.exists(dest):
            os.makedirs(dest)

    def derive_key(self, master_password: str, salt: bytes):
        # Creates a Fernet Key based on a password and salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32, # Fernet's Length
            salt=salt,
            iterations=100000, # How many Iterations (the bigger, more safe)
        )
        key = urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key

    def generate_key(self, master_password_input: str):
        """
        Load the Cryptography Key from salt or generates it
        using the given password
        """
        salt = None
        if os.path.exists(self.salt_path):
            with open(self.salt_path, 'rb') as f:
                salt = f.read()
        else:
            salt = os.urandom(16)
            with open(self.salt_path, 'wb') as f:
                f.write(salt)
        self.fernet_key = Fernet(self.derive_key(master_password_input, salt))
        return self.fernet_key

    def config_loader(self, master_password): # Decodes the JSON File and Loads
        try:
        # Asks for password for the Cryptography Key
            self.fernet_key = self.generate_key(master_password)
            
            # Try to load the Encrypted File
            with open(self.config_path, "rb") as f:
                encrypted_data = f.read()
                decrypted_data = self.fernet_key.decrypt(encrypted_data)
                config = json.loads(decrypted_data.decode())
            
                self.password = config.get('password', '')
                self.api_key = config.get('api_key', '')
                return True
        except FileNotFoundError:
            self._show_popup('Configuração', 'Arquivo de configurações não encontrado!')
            return False
        except Exception as e: # Capture's cryptography or JSON Errors
            self._show_popup('Erro de Configuração', f'Erro ao carregar ou descriptografar: {e}. Verifique a senha mestra ou o arquivo.')
            return False

    def save_config(self, password_app, api_key_input. master_password):
        self.password = password_app
        self.api_key = api_key_input
        self.fernet_key = self.generate_key(master_password)
    
        if not fernet_key: # Make's sure the key is Loaded/Created
            self._show_popup('Erro ao salvar', 'Chave de criptografia não disponível.')
            return False
    
        config = {
            "password": self.password,
            "api_key": self.api_key
        }
        json_bytes = json.dumps(config).encode() # Parses the JSON to a String and then Bytes
        encrypted_json = self.fernet_key.encrypt(json_bytes) # Encrypts the Bytes
    
        with open(self.config_path, "wb") as f: # Opens in Binary Mode "wb"
            f.write(encrypted_json)
        self._show_popup('Sucesso', 'Configurações salvas e criptografadas com sucesso.')
        return True

    def download(self, search_filter, dest_folder, total_images, update_progress_callback):  # Starts the Download of the Images based on the given Data
        try:
            total_images_int = int(total_images)
            if total_images_int <= 0:
                self.show_popup_callback('Erro', 'Total de Imagens deve ser positivo')
                return False
            if not search_filter.strip():
                self._show_popup('Erro', 'O filtro de pesquisa não pode estar vazio.')
                return False
            if not dest_folder:
                self._show_popup('Erro', 'Caminho de destino não pode estar vazio.')
                return False

            if not os.path.exists(dest_folder):
                self.mkdir(dest_folder)
                if not os.path.exists(dest_folder):
                    self._show_popup('Erro', 'Destino de download inválido ou não foi possível criar.')
                    return False
                
            index_per_page = 30
            downloaded_count = 0
    for page in range(1, (total // index_pg) + 2):
        url = f"https://api.unsplash.com/search/photos?query={filtro}&client_id={api_key}&per_page={index_pg}&page={page}"
        response = requests.get(url)

        data = response.json()
        if "results" in data:
            for i, image in enumerate(data["results"]):
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()

                    img_url = image["urls"]["regular"]
                    img_data = requests.get(img_url).content
                    file_number = (
                        page - 1
                    ) * index_pg + i  # Name of the correct File & Index
                    with open(
                        os.path.join(dest, f"{filtro}_{file_number}.jpg"), "wb"
                    ) as handler:
                        handler.write(img_data)
                    print(f"Imagem {file_number + 1} baixada.")
                    if file_number + 1 >= total:
                        messagebox.showinfo("Image Downloader",f"Download finalizado! \n\nFiltro: {filtro} \nDestino: {dest} \nTotal de Imagens: {total}",)
                        break
                    else:
                        print('Nenhuma imagem encontrada ou chave "results" nao encontrada.')
                        # print(data)
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Unsplasher", f"Erro ao buscar imagem: {e}")
                except OSError as e:
                    messagebox.showerror("Unsplasher", f"Não foi possivel salvar a imagem: {e}")

def passuser():  # User Data verification
    root.withdraw()
    t = 0
    while True:
        pw = simpledialog.askstring("Image Downloader", "Digite a sua senha: ")
        if pw:
            if pw == password:
                messagebox.showinfo("Image Downloader", "SENHA CORRETA. \nIniciando o sistema.")
                get_user()
                break
            elif pw is None:
                messagebox.showwarning("Image Downloader", "Insira uma senha!")
                return
            else:
                t += 1
                messagebox.showwarning("Image Downloader", f"SENHA INCORRETA. \nTentativa: {t}")
                if t == max_t:
                    messagebox.showwarning("Image Downloader", "Tente novamente mais tarde.")
                    root.quit()
                    break
                else:
                    root.quit()
                    break

def get_user(): # Get's User Data if it's None
    global filtro, dest, total_img
    filtro = simpledialog.askstring("Image Downloader", "Digite o filtro de pesquisa:")
    dest = filedialog.askdirectory(title="Selecione o destino das imagens:")
    total_img = simpledialog.askstring("Image Downloader", "Digite o total de imagens:")
    if filtro and dest and total_img:
        try:
            download()
        except ValueError:
            messagebox.showerror("Image Downloader", "Total de imagens inválido. Insira um número inteiro.",)
    else:
        messagebox.showerror("Image Downloader", "Preencha todos os campos!")

jsonloader() # Calls JSONLoader Function
passuser() # Calls the User verification Function