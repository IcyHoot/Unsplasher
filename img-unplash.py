# This Python script is using the `requests` library to interact with the Unsplash
# API in order to download images based on a specific search query (in this case,
# 'pessoas' which means 'people'). Here's a breakdown of what the script is doing:

import requests
import os

api_key = '' # a sua API KEY do Unsplash 
filtro = 'people' # oq vai pesquisar
dest = 'datasets/images/people/train' # onde vai salvar as imgs
t_img = 99 # total de imagens
i_pg = 30 # imagens por pagina

if not os.path.exists(dest): # cria a pasta se n existir
    os.makedirs(dest)

# url q ele vai utilizar para buscar as imgs
url = f'https://api.unsplash.com/search/photos?query={filtro}&client_id={api_key}'

response = requests.get(url)

for page in range(1, (t_img // i_pg) + 2): # +2 pra garantir q vai pegar 100 imagens
    url = f'https://api.unsplash.com/search/photos?query={filtro}&client_id={api_key}&per_page={i_pg}&page={page}'
    response = requests.get(url)
    
    if response.status_code == 401: # verifica se o codigo de erro é 401, se sim verifique a API KEY
        print('Erro 401: Nao autorizado. Verifique sua chave API.')
    elif response.status_code != 200:
        print(f'Nao foi possivel buscar a imagem: {response.status_code}')
        print(response.json())
    else:
        data = response.json()
        if 'results' in data:
            for i, image in enumerate(data['results']):
                img_url = image['urls']['small']
                img_data = requests.get(img_url).content
                # nome do arquivo com indice correto
                file_number = (page - 1) * i_pg + i
                with open(os.path.join(dest, f'img_{file_number}.jpg'), 'wb') as handler:
                    handler.write(img_data)
                print(f'imagem {file_number + 1} baixada.')
                
                if file_number + 1 >= t_img:
                    break
        else:
            print('Nenhuma imagem encontrada ou chave "results" nao encontrada.')
            print(data)

print('download concluido, sobre: ', filtro)