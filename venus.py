# -*- coding: cp1252 -*-
import requests
import os
from StringIO import StringIO
try:
    from colorama import *
except:
    print "Suporte a cores nao encontrado"
    print "tente pip install colorama"
    sys.exit(0)
print Style.BRIGHT+Fore.RED
try:
    from bs4 import BeautifulSoup
except:
    print "Parser de html nao encontrado"
    print "tente pip install beautifulsoup4"
    sys.exit(0)
try:
    from PIL import Image
except:
    print "biblioteca de imagens nao encontrada"
    print "tente pip install pillow"
    sys.exit(0)

print Style.RESET_ALL


paginasPorCapitulos = []
def pegarImagem(capitulo, pagina ,arg):
    
    print "Baixando: {nrm}E{bright}{cap:02d}{nrm}P{brightC}{pag:02d}".format(nrm=Fore.WHITE+Style.BRIGHT,bright = Style.NORMAL+Fore.BLUE, brightC = Style.NORMAL+Fore.CYAN,  cap = capitulo, pag = pagina)+Style.RESET_ALL,
    r = requests.get('http://#SITE/manga/{}/{}/{}'.format(arg,capitulo,pagina))
    corpo = r.text
    soup = BeautifulSoup(r.text,"html.parser")
    if(os.path.exists(preTitulo+"/{cap:02d}".format(cap = capitulo)) == False):
        os.mkdir(preTitulo+"/{cap:02d}".format(cap = capitulo))
    try:
        imagem = soup.find(attrs={"class": "img-responsive"})
        i = requests.get(imagem['src']).content
        i = Image.open(StringIO(i))
        i.save(preTitulo+"/{cap:02d}/E{cap:02d}P{pag:02d}.jpg".format(cap = capitulo, pag =pagina),"JPEG")
        print Style.BRIGHT+Fore.GREEN+"[OK]"+Style.RESET_ALL
    except:
        print " --- Tentando Download Alternativo... ",
        try:
            i = requests.get(imagem['onerror'].replace("this.src='","")[:-1]).content
            i = Image.open(StringIO(i))
            i.save(preTitulo+"/{cap:02d}/E{cap:02d}P{pag:02d}.jpg".format(cap = capitulo, pag =pagina),"JPEG")
            print Style.BRIGHT+Fore.GREEN+"[OK]"+Style.RESET_ALL
        except (KeyboardInterrupt):
            sys.exit(1)
        except:
            print Style.BRIGHT+Fore.RED+"[Falhou]"+Style.RESET_ALL
            return False
    return True


def avaliarManga(comeco,capitulos,arg):
    global paginasPorCapitulos
    paginasTotal = 0
    print Style.BRIGHT+"Aguarde."+Style.RESET_ALL
    print
    print
    print "[",
    for a in xrange(comeco,capitulos+1):
    #contar quantas paginas nesse capitulo
        print Fore.RED+Style.BRIGHT+".",
        r = requests.get('http://#SITE/manga/{}/{}/1'.format(arg,a))
        parsed = BeautifulSoup(r.text,"html.parser")
        pag = parsed.find("select",{"id":"page-dropdown"})
        paginas = len(pag.find_all("option"))
        paginasPorCapitulos.append(paginas)
        paginasTotal+=paginas
    print Style.RESET_ALL+"]"
    return paginasTotal


def acharCapitulos(arg):
    r = requests.get('http://#SITE/system/temp/js/{}.js'.format(arg))
    linhas = r.text.split("\n")
    return (len(linhas)-1)

def formatarTitulo(s):
    s = s.replace(" ","_")
    return s

if __name__ == "__main__":
    #começa interface
    init() #colorama
    print Style.BRIGHT+Fore.YELLOW+"Welcome to "+Fore.MAGENTA+"VENUS"+Fore.YELLOW+" - Manga Downloader"
    print
    print
    preTitulo = raw_input(Style.BRIGHT+Fore.CYAN+"{T}itulo: "+Fore.RESET).lower()
    titulo = formatarTitulo(preTitulo)
    try:
        ini = input(Fore.CYAN+"{C}capitulo inicial  [vazio para primeiro]: "+Fore.RESET)
    except:
        ini = 1
    try:
        fim = input(Fore.CYAN+"{C}apitulo final  [vazio para ultimo]: "+Fore.RESET)
    except:
        fim = acharCapitulos(titulo)

    print Style.RESET_ALL
    print

    print "Quantidade de capitulos: {efeito}{f}{efeitofinal}".format(f=fim,efeito=Style.BRIGHT,efeitofinal=Style.RESET_ALL)

    print "Procurando Quantidade de paginas em cada capitulo."
    quantidade = avaliarManga(ini,fim,titulo)
    print "Encontradas {efeito}{q}{efeitofinal} paginas".format(q=quantidade,efeito=Style.BRIGHT+Fore.YELLOW,efeitofinal=Style.RESET_ALL)
    try:
        os.mkdir(preTitulo)
    except:
        pass
    capitulo = ini-1
    for capit in paginasPorCapitulos:
        capitulo+=1
        print
        print
        print "Iniciando capitulo {efeito}{c}{efeitofinal}".format(c = capitulo,efeito=Style.BRIGHT+Fore.BLUE,efeitofinal=Style.RESET_ALL)
        for pagi in xrange(1,capit):
            pegarImagem(capitulo,pagi,titulo)
    raw_input(Style.BRIGHT+Fore.RED+"[TUDO FEITO]"+Style.RESET_ALL)

