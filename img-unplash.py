# This Python script is using the `requests` library to interact with the Unsplash
# API in order to download images based on a specific search query (in this case,
# 'pessoas' which means 'people'). Here's a breakdown of what the script is doing:
import tkinter as tk
from tkinter import messagebox, simpledialog

import requests
import threading
import os


entry_filtro = None
entry_dest = None
root = tk.Tk()
api_key = 't3aoXTl1h2BD9vtMi8Fv_wP2mTshMUUff6w6Cj-zLpY' # a sua API KEY do Unsplash 
filtro = '' # oq vai pesquisar
dest = '' # onde vai salvar as imgs
t_img = 100
i_pg = 30

# url q ele vai utilizar para buscar as imgs
url = f'https://api.unsplash.com/search/photos?query={filtro}&client_id={api_key}'

response = requests.get(url)

def passUser(): # função de verif
    root.withdraw()
    passw = 'unsplash'
    t = 0
    while True:
        pw = simpledialog.askstring('Image Downloader', 'Digite a sua senha: ')
        if pw:
            if pw == passw:
                messagebox.showinfo('Image Downloader', 'SENHA CORRETA. \nIniciando o sistema.')
                download()
                break
            else:
                t += 1
                messagebox.showwarning('Image Downloader',f'SENHA INCORRETA. \nTentativa: {t}')
                if t == 3:
                    messagebox.showwarning('Image Downloader','Tente novamente mais tarde.')
                    root.quit()
                    break
        else:
            messagebox.showwarning('Image Downloader','Insira uma senha!')

def mkdir(dest): # função que cria o destino se for falso
    if not os.path.exists(dest):
        os.makedirs(dest)

def thread():
    threading.Thread(target=download())
    threading.Thread(target=passUser())

def download(): # inicia o download das imagens com base no dados fornecidos
    global api_key, filtro, dest

    filtro = entry_filtro.get()
    dest = entry_dest.get()

    mkdir(dest)

    for page in range(1, (t_img // i_pg) + 2): # +2 pra garantir q vai pegar 100 imagens
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
                
                if file_number + 1 >= t_img:
                    print('download concluido, sobre: ', filtro)
                    break
        else:
            print('Nenhuma imagem encontrada ou chave "results" nao encontrada.')
            print(data)

def submit():
    passUser()

def main():
    global entry_filtro, entry_dest

    tk.Label(root, text='Filtro:').grid(row=0, column=0, padx=10, pady=5)
    entry_filtro = tk.Entry(root)
    entry_filtro.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text='Destino:').grid(row=1, column=0, padx=10, pady=5)
    entry_dest = tk.Entry(root)
    entry_dest.grid(row=1, column=1, padx=10, pady=5)

    button_iniciar = tk.Button(root, text="Iniciar Download", command=submit)
    button_iniciar.grid(row=3, columnspan=2, pady=10)

if __name__ == '__main__':
    main()
    root.mainloop()
