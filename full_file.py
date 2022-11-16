import requests
from bs4 import BeautifulSoup
import validators
from validators import ValidationFailure

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

def scrape_laNacion(fileName):

	url = 'https://www.lanacion.com.ar/'
	grab = requests.get(url)
	soup = BeautifulSoup(grab.text, 'html.parser')

	# opening a file in write mode
	f = open(fileName, "w")
	urls = []
	# traverse paragraphs from soup
	for link in soup.find_all("a"):
		href = link.get('href')
		if '.com' not in href and '.' not in href and 'tema' not in href and href.count('/') > 1 and href not in urls :
			data = link.get('href')
			full_url = url + data
			urls.append(full_url)
			str_is_valid(full_url)
			f.write(full_url)
			f.write("\n")

	f.close()
	return urls

def are_links_valid(txtfile):

	i_file = open(txtfile)
	lines = i_file.readlines()

	for line in lines:
		assert is_string_an_url(line) == True
	



def returnObj(url):
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
			

	articleObj = Article(title.text, paragraphs_text)
	str_is_valid(title.text)

	return articleObj


def main():
	urls = scrape_laNacion("randfile.txt")

	# are_links_valid("randfile.txt")
	newArticle = returnObj(urls[0])
	print(f'Título: {newArticle.title}')
	print("\n\n")
	for par in newArticle.paragraphs:
		print(f'Párrafo: {par}')
		print("\n")




if __name__ == '__main__':
	main()