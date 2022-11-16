import requests
from bs4 import BeautifulSoup
import validators
from validators import ValidationFailure
import re


def str_is_valid(newStr):
	assert newStr != ""

class Article:
	def __init__(self, title, paragraphs):
		self.title = title  
		self.paragraphs = paragraphs


def is_string_an_url(url_string: str) -> bool:
    grab = requests.get(url_string)
    result = validators.url(url_string)

    if isinstance(result, ValidationFailure) or 'La página que buscás no está disponible.' in grab.text:
        return False

    return result

def scrape_laNacion(url,fileName):
	if url[-1] == '/':
		url = url.rstrip('/')

	
	grab = requests.get(url)
	soup = BeautifulSoup(grab.text, 'html.parser')

	# opening a file in write mode
	f = open(fileName, "w")
	urls = []
	# traverse paragraphs from soup
	for link in soup.find_all("a"):
		href = link.get('href')
		full_url = url + href
		if '.com' not in href and '.' not in href and 'tema' not in href and href.count('/') > 1 and full_url not in urls :
			data = link.get('href')
			full_url = url + data
			urls.append(full_url)
			str_is_valid(full_url)
			
	urls = [*set(urls)]
	for url in urls:
		f.write(url)
		f.write("\n")
	f.close()
	return urls

def are_links_valid(txtfile):

	i_file = open(txtfile)
	lines = i_file.readlines()

	for line in lines:
		assert is_string_an_url(line) == True
	



def returnDict(url):
	grab = requests.get(url)
	soup = BeautifulSoup(grab.text, 'html.parser')


	title = soup.find("h1", {"class": "com-title --threexl"})

	paragraphs = soup.find_all("p")
	not_in = [
		"Copyright 2022 SA LA NACION | Todos los derechos reservados",
		"Copyright 2023 SA LA NACION | Todos los derechos reservados",
		"Descargá la aplicación de LA NACION. Es rápida y liviana.",
		"¿Querés recibir notificaciones de alertas?",
		"Ha ocurrido un error de conexión",
		"Home",
		"Secciones",
		"Club LN",
		"Mi Cuenta"
		]

		
		
		
	paragraphs_text = []

	for par in paragraphs:
		
		
		if par.text not in not_in and par.text != title.text:
			paragraphs_text.append(par.text)
			str_is_valid(paragraphs_text)

	subhead = soup.find('h2', {'class':"com-subhead --bajada --m-xs"})
	this_dict = {
		"Title": title.text,
		"subhead":subhead.text,
		"paragraphs": paragraphs_text
	}
	return this_dict
			

	
	


def main():
	urls = scrape_laNacion("https://www.lanacion.com.ar/","randfile.txt")

	# are_links_valid("randfile.txt")
	newArticle = returnDict(urls[0])
	print(f'Título: {newArticle["Title"]}')
	print("\n\n")
	print(f'subhead: {newArticle["subhead"]}')
	print('\n\n')
	for par in newArticle["paragraphs"]:
		print(f'Párrafo: {par}')
		print("\n")
	




if __name__ == '__main__':
	main()