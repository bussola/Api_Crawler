from selenium.webdriver import FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from app_api.crawler import quebraCaptcha
import urllib.request # Download da imagem
from ..models import Dados
from django.db import transaction
import os
import shutil


# Preenche os dados da nota
def preenche_dados(driver, name, dados):
	elem = driver.find_element_by_name(name)
	elem.clear()
	elem.send_keys(dados)


def preenche_formulario(driver, bool_refresh_pagina):
	# Dados
	cnpj = "10831692000173"
	nfs = "1886"
	inscricao = "1628534"
	cod_verif = "8eb34d2809793d1d8aabdcb4fb7488d9bd2cfe58"

	# Preenche os dados necessarios, menos o captcha
	preenche_dados(driver, "rPrest", cnpj)
	preenche_dados(driver, "rNumNota", nfs)
	preenche_dados(driver, "rInsMun", inscricao)
	preenche_dados(driver, "rCodigoVerificacao", cod_verif)

	# ******** Captcha
	# Pega url da imagem
	img = driver.find_elements_by_tag_name('img')
	if bool_refresh_pagina: # Qnd a pagina da refresh, muda o local da imagem
		url_img_captcha = img[6].get_attribute("src")
	else:
		url_img_captcha = img[5].get_attribute("src")
	print("URL: " + str(url_img_captcha))

	# Download da imagem
	urllib.request.urlretrieve(url_img_captcha, "img.jpg")
	time.sleep(2)

	# Reconhecimento do captcha
	captcha_text = quebraCaptcha.quebra() 	# Retorna uma string do captcha
	preenche_dados(driver, "rSelo", captcha_text)

	# Clica no botão
	element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "btnVerificar"))
    )
	driver.find_element_by_name('btnVerificar').click()
	time.sleep(2)

	qnt_paginas_abertas = len(driver.window_handles)
	if qnt_paginas_abertas != 3: #Se o captcha não der certo, nao abre uma terceira pagina
		driver.switch_to.window(driver.window_handles[1])
		driver.close()
		driver.switch_to.window(driver.window_handles[0])
		driver.refresh()
		bool_refresh_pagina = True
		time.sleep(2)
		return False, bool_refresh_pagina
	else: #Se o captcha der certo
		# Renomeia o arquivo da img do captcha, com o valor correto
		img_file_name = str(captcha_text) + ".jpg"
		current_path = os.path.dirname(os.path.abspath(__file__))
		destino = current_path + "/captcha_imgs/" + img_file_name
		os.rename('img.jpg', destino)
		return True, bool_refresh_pagina


@transaction.atomic
def crawler():
	print("Comecar")
	opts = FirefoxOptions()
	#opts.add_argument("--headless")
	print("Criando driver...")
	driver = webdriver.Firefox(options=opts)
	driver.implicitly_wait(10)
	print("Driver criado")

	# Entra no site
	driver.get("https://nfse.campinas.sp.gov.br/NotaFiscal/verificarAutenticidade.php")
	
	# Insere as info em loop até passar o captcha
	boll_captcha = False
	bool_refresh_pagina = False
	while boll_captcha == False:
		boll_captcha, bool_refresh_pagina = preenche_formulario(driver, bool_refresh_pagina)

	# Fecha as paginas abertas e muda para a pagina dos registros
	for i in range(0, 3):
		driver.switch_to.window(driver.window_handles[0])
		if i != 2:
			driver.close()
	print(driver.current_url)

	# Pega os dados da nova pagina dos registros
	tabelas = driver.find_elements_by_class_name('impressaoTabela')
	print("Qnt de tabelas: ", len(tabelas))
	for i in range(0, 4):
		row_index = 0
		categoria = ""
		for row in tabelas[i].find_elements_by_tag_name('tr'):
			for col in row.find_elements_by_tag_name('td'):
				if col.text != "":
					# Insere os dados no DB
					row_index+=1
					if i == 0:
						pass
						#print (i, col.text)
					elif i == 1:
						categoria = "Dados da nota"
						if row_index%2!=0:
							title = col.text
							#print ("title: ", title)
						else:
							body = col.text
							#print ("body: ", body)
							tabela = Dados(categoria=categoria, title=title, body=body)
							tabela.save()
					elif i == 2:
						if row_index == 1:
							categoria = col.text
							#print ("categoria: ", categoria)
						else:
							title = col.text.split(":")[0]
							body = col.text.split(":")[1]
							#print("title", title)
							#print("body", body)
							tabela = Dados(categoria=categoria, title=title, body=body)
							tabela.save()
					elif i == 3:
						if row_index == 1:
							categoria = col.text
							#print ("categoria: ", categoria)
						else:
							title = col.text.split(":")[0]
							body = col.text.split(":")[1]
							#print("title", title)
							#print("body", body)
							tabela = Dados(categoria=categoria, title=title, body=body)
							tabela.save()
	driver.close()



# if __name__ == '__main__':
#     crawler()