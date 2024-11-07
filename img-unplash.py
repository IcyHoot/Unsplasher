# This Python script is using the `requests` library to interact with the Unsplash
# API in order to download images based on a specific search query (in this case,
# 'pessoas' which means 'people'). Here's a breakdown of what the script is doing:
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

import requests
import threading
import os
import json

entry_filtro = None
entry_dest = None
root = tk.Tk()
api_key = 't3aoXTl1h2BD9vtMi8Fv_wP2mTshMUUff6w6Cj-zLpY' # a sua API KEY do Unsplash 
filtro = '' # oq vai pesquisar
dest = '' # onde vai salvar as imgs
t_img = ''
passw = ''
max_t = 3
i_pg = 30

# url q ele vai utilizar para buscar as imgs
url = f'https://api.unsplash.com/search/photos?query={filtro}&client_id={api_key}'

response = requests.get(url)

def jsonsaver():
    root.withdraw()
    config = {'password': passw, 'tentativas': max_t}
    with open('config.json', 'w') as f:
        json.dump(config, f)

def jsonloader():
    root.withdraw()
    global passw, max_t
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            passw = config.get('password', '0000')
            max_t = config.get('tentativas', 3)
    except FileNotFoundError:
        passw = simpledialog.askstring('Image Downloader','Arquivo de Configurações não encontrado! \nDigite uma senha: ')
        return

def passUser(): # função de verif
    root.withdraw()
    t = 0
    while True:
        pw = simpledialog.askstring('Image Downloader', 'Digite a sua senha: ')
        if pw:
            if pw == passw:
                messagebox.showinfo('Image Downloader', 'SENHA CORRETA. \nIniciando o sistema.')
                main()
                break
            else:
                t += 1
                messagebox.showwarning('Image Downloader',f'SENHA INCORRETA. \nTentativa: {t}')
                if t == max_t:
                    messagebox.showwarning('Image Downloader','Tente novamente mais tarde.')
                    root.quit()
                    break
        else:
            messagebox.showwarning('Image Downloader','Insira uma senha!')

def main():
    global filtro, dest, t_img
    filtro = simpledialog.askstring('Image Downloader','Insira o Filtro: ')
    print('Filtro: ', filtro)
    messagebox.showinfo('Image Downloader','Escolha o diretório')
    dest = filedialog.askdirectory(title='Escolha o diretório.')
    print('Destino: ', dest)
    t_img = simpledialog.askinteger('Image Downloader', 'Insira a Quantidade: ')
    print('Quantidade: ', t_img)
    if filtro is not None and t_img is not None and dest is not None:
        download()

def mkdir(dest): # função que cria o destino se for falso
        if not os.path.exists(dest):
            os.makedirs(dest)

def thread():
    threading.Thread(target=download())
    threading.Thread(target=passUser())
    threading.Thread(target=main())

def download(): # inicia o download das imagens com base no dados fornecidos
    t_Img = int(t_img)
    for page in range(1, (t_Img // i_pg) + 2): # +2 pra garantir q vai pegar 100 imagens
        url = f'https://api.unsplash.com/search/photos?query={filtro}&client_id={api_key}&per_page={i_pg}&page={page}'
        response = requests.get(url)

        if response.status_code == 401:
            print('Erro 401: Nao autorizado. Verifique sua chave API.')
        elif response.status_code != 200:
            print(f'Nao foi possivel buscar a imagem: {response.status_code}')
            print(response.json())
        else:
            data = response.json()

        if 'results' in data:
            for i, image in enumerate(data['results']):
                img_url = image['urls']['regular']
                img_data = requests.get(img_url).content
                file_number = (page - 1) * i_pg + i # nome do arquivo com indice correto
                with open(os.path.join(dest, f'img_{file_number}.jpg'), 'wb') as handler:
                    handler.write(img_data)
                print(f'imagem {file_number + 1} baixada.')
                
                if file_number + 1 >= t_Img:
                    messagebox.showinfo('Image Downloader',f'Download finalizado! \n\nFiltro: {filtro} \nDestino: {dest} \nTotal de Imagens: {t_Img}')
                    break
        else:
            print('Nenhuma imagem encontrada ou chave "results" nao encontrada.')
            print(data)

jsonloader()
jsonsaver()
passUser()
