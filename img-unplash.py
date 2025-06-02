# This Python script is using the `requests` library to interact with the Unsplash
# API in order to download images based on a specific search query (in this case,
# 'pessoas' which means 'people'). Here's a breakdown of what the script is doing:

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import requests
import os
import json

root = tk.Tk()
user = os.getlogin()
api_key = ""  # a sua API KEY do Unsplash
filtro = ""  # oq vai pesquisar
dest = ""  # onde vai salvar as imgs
total_img = ""  # total de imgs
password = ""  # senha
base = f"C:/Users/{user}/Documents/.img-down/config"  # padrão da config file
url = f"https://api.unsplash.com/search/photos?query={filtro}&client_id={api_key}"
response = requests.get(url)

def mkdir(dest):
    if not os.path.exists(dest):
        os.makedirs(dest)

def jsonloader():
    root.withdraw()
    global password, max_t, api_key
    try:
        with open(os.path.join(base, "config.json"), "r") as f:
            config = json.load(f)
            password = config.get("password", "")
            api_key = config.get("api_key", "")
    except FileNotFoundError:
        messagebox.showwarning(
            "Image Downloader", "Arquivo de Configurações não encontrado!"
        )
        password = simpledialog.askstring("Image Downloader", "Digite uma senha:")
        api_key = simpledialog.askstring("Image Downloader", "Digite a sua API Key:")
        if password and api_key:
            messagebox.showinfo(
                "Image Downloader", "Senha e API Key definidos com sucesso!"
            )
            jsoncreate()
        else:
            messagebox.showerror("Image Downloader", "Digite uma senha e API Key!")
            root.quit()
            return
        return
    except json.JSONDecodeError:
        messagebox.showerror("Unsplasher", "O arquivo de config está corrompido!")

def jsoncreate():
    global base, password, api_key
    root.withdraw()
    mkdir(base)
    config = {"password": password, "api_key": api_key}
    with open(os.path.join(base, "config.json"), "w") as f:
        json.dump(config, f)

def download():  # inicia o download das imagens com base no dados fornecidos
    total = int(total_img)
    index_pg = 30  # imgs por page

    for page in range(
        1, (total // index_pg) + 2
    ):  # +2 pra garantir q vai pegar 100 imagens
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
                    ) * index_pg + i  # nome do arquivo com indice correto
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

def passuser():  # função de verif
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

def get_user():
    global filtro, dest, total_img
    filtro = simpledialog.askstring("Image Downloader", "Digite o filtro de pesquisa:")
    dest = filedialog.askdirectory(title="Selecione o destino das imagens:")
    total_img = simpledialog.askstring("Image Downloader", "Digite o total de imagens:")
    if filtro and dest and total_img:
        try:
            download()
        except ValueError:
            messagebox.showerror(
                "Image Downloader",
                "Total de imagens inválido. Insira um número inteiro.",
            )
    else:
        messagebox.showerror("Image Downloader", "Preencha todos os campos!")

jsonloader()
passuser()
