# Api_Crawler

Este projeto compões a criação de um simples web crawler com Selenium e Python, com inserção de dados e quebra de captcha.


# Instalação:
Clone esse repositório;
Crie um DB postgres com as especificações dos dados que estão em settings.py;
Instale o requirements.txt via pip;
Migre o banco e crie um 'superuser';


# Para rodar o Crawler
Foi criado um comando para rodar o script do crawler - python manage.py roda_crawler;
O crawler abre a página, preenche os dados necessários e tenta quebrar o captcha até conseguir;
Com o captcha 'quebrado', salva a imagem do captcha para futuras utilizações;


# API Endpoint
Depois de rodar o crawler, o resultado ficará disponível via Json, no endpoint http://localhost:8000/api/v1/dados/
