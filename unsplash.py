import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import requests
import os
import json
from cryptography.fernet import Fernet # Import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode, b64decode

root = tk.Tk()
user = os.getlogin()
api_key = ""  # User's API KEY
filtro = ""  # Seach Query
dest = ""  # Save Location
total_img = ""  # Total of Images
password = ""  # Password
base = f"C:/Users/{user}/Documents/.img-down/config"  # config.json default directory
url = f"https://api.unsplash.com/search/photos?query={filtro}&client_id={api_key}" # Unsplash API URL
response = requests.get(url)

def mkdir(dest): # Creates a directory based on "base"
    if not os.path.exists(dest):
        os.makedirs(dest)

def derive_key(password: str, salt: bytes):
    # Creates a Fernet Key based on a password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, # Fernet's Length
        salt=salt,
        iterations=100000, # How many Iterations (the bigger, more safe)
    )
    key = urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def generate_key(password_input: str):
    """
    Load the Cryptography Key from salt or generates it
    using the given password
    """
    global fernet_key
    
    # Salt must be persistent for the same password generate the same key
    salt_path = os.path.join(base, 'salt.salt')
    salt = None
    mkdir(base)
    if os.path.exists(salt_path):
        with open(salt_path, 'rb') as f:
            salt = f.read()
    else:
        salt = os.urandom(16)
        with open(salt_path, 'wb') as f:
            f.write(salt)
            
    fernet_key = Fernet(derive_key(password_input, salt))
    
    return fernet_key

def jsonloader(): # Decodes the JSON File and Loads
    root.withdraw()
    global password, api_key, fernet_key
    try:
        # Asks for password for the Cryptography Key
        master_pass = simpledialog.askstring('Image Downloader', 'Digite sua senha mestra para descriptografar:')
        if not master_pass:
            messagebox.showwarning('Image Downloader', 'Senha mestra necessária para descriptografar. Saindo.')
            root.quit()
            return
        fernet_key = generate_key(master_pass)
        
        # Try to load the Encrypted File
        with open(os.path.join(base, "config.json"), "rb") as f:
            encrypted_data = f.read()
            decrypted_data = fernet_key.decrypt(encrypted_data)
            config = json.loads(decrypted_data.decode())
            
            password = config.get('password', '')
            api_key = config.get('api_key', '')
    except FileNotFoundError:
        messagebox.showwarning("Image Downloader", "Arquivo de Configurações não encontrado!")
        master_pass = simpledialog.askstring('Image Downloader', 'Crie uma chave mestra: ')
        if not master_pass:
            messagebox.showwarning('Image Dwonloader', 'Uma chave mestra é necessária!')
            root.quit()
            return
        fernet_key = generate_key(master_pass) # Create's the new Key with the Password
        
        password = simpledialog.askstring("Image Downloader", "Digite uma senha:")
        api_key = simpledialog.askstring("Image Downloader", "Digite a sua API Key:")
        if password and api_key:
            messagebox.showinfo("Image Downloader", "Senha e API Key definidos com sucesso!")
            jsoncreate() # Create's the Encrypted File
        else:
            messagebox.showerror("Image Downloader", "Digite uma senha e API Key!")
            root.quit()
            return
        return
    except Exception as e: # Capture's cryptography or JSON Errors
        messagebox.showerror('Image Downloader', f'Erro ao carregar ou descriptografar o arquivo de config: {e}. Verifique a chave mestra ou o arquivo.')
        root.quit()
        return

def jsoncreate():
    global base, password, api_key, fernet_key, max_t
    root.withdraw()
    mkdir(base)
    if not fernet_key: # Make's sure the key is Loaded/Created
        messagebox.showerror('Image Downloader', 'Chave de criptografia não disponível. Não foj possível salvar.')
        root.quit()
        return
    
    config = {
        "\npassword": password,
        "\napi_key": api_key
        }
    json_bytes = json.dumps(config).encode() # Parses the JSON to a String and then Bytes
    encrypted_json = fernet_key.encrypt(json_bytes) # Encrypts the Bytes
    
    with open(os.path.join(base, "config.json"), "wb") as f: # Opens in Binary Mode "wb"
        f.write(encrypted_json)
    messagebox.showinfo('Image Downloader', 'Configurações salvas e criptografadas com sucesso!')

def download():  # Starts the Download of the Images based on the given Data
    total = int(total_img)
    index_pg = 30  # Images-per-page

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
