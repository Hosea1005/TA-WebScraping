from asyncio.windows_events import NULL
from os import link
from urllib import request
import requests
import io
from bs4 import BeautifulSoup
import csv
import mysql.connector
import re
import pytesseract
from pytesseract import (
    Output,
    TesseractError,
    TesseractNotFoundError,
    TSVNotSupported,
    get_tesseract_version,
    image_to_boxes,
    image_to_data,
    image_to_osd,
    image_to_pdf_or_hocr,
    image_to_string,
    run_and_get_output
)
from PIL import Image


#URL
urlTraveloka = 'https://www.traveloka.com/en-id/promotion'
urlTiket = 'https://www.tiket.com/promo'
urlPegi = 'https://www.pegipegi.com/promo/?f=slider'
urlAirpaz = 'https://www.airpaz.com/id/promo'
urlNusa = "https://www.nusatrip.com/id/promo/travel-tiket-pesawat-hotel-domestik-internasional"
urlGaruda = 'https://www.garuda-indonesia.com/id/id/special-offers/sales-promotion'
urlCiti = 'https://www.citilink.co.id/events'


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
}
#Request
reqTraveloka = requests.get(urlTraveloka, headers=headers)
soupTraveloka = BeautifulSoup(reqTraveloka.text,'html.parser')

reqTiket = requests.get(urlTiket, headers=headers)
soupTiket = BeautifulSoup(reqTiket.text,'html.parser')

reqPegi = requests.get(urlPegi, headers=headers)
soupPegi = BeautifulSoup(reqPegi.text,'html.parser')

reqAirpaz = requests.get(urlAirpaz, headers=headers)
soupAirpaz = BeautifulSoup(reqAirpaz.text,'html.parser')

reqNusa = requests.get(urlNusa, headers=headers)
soupNusa = BeautifulSoup(reqNusa.text,'html.parser')

reqGar = requests.get(urlGaruda, headers=headers)
soupGar = BeautifulSoup(reqGar.text, 'html.parser')

reqCit = requests.get(urlCiti, headers=headers)
soupCit = BeautifulSoup(reqCit.text, 'html.parser')



#Items
itemsTraveloka = soupTraveloka.findAll('div','promo-thumb')
itemsPegi = soupPegi.findAll('div','col-sm-6 col-md-4')
itemsTiket = soupTiket.findAll('a',{'class':'promo-card'})
itemsAirpaz = soupAirpaz.findAll('a', 'promo-list-card card')
itemsNusa = soupNusa.findAll('div', 'col clearst no-padding divi3 ts grebo')
itemsGar = soupGar.findAll('div', 'col col-xs-12 col-sm-6 col-md-4')
itemsCit = soupCit.findAll('table', 'no-border')


#Scraping Sudah Fix

for peg in itemsPegi : 
    nilai = 1
    judulPegi = peg.find('div','caption').find('p').text
    try : durasiPegi = peg.find('p','endpromo').text
    except : durasiPegi = 'Tidak memiliki durasi'
    linknyaPegi = peg.find('a')['href']
    imgPegi = peg.find('div','thumbnail').find('img')['src']
    if 'http' not in imgPegi : imgPegi = 'https://www.pegipegi.com/promo/{}'.format(imgPegi)
    # img = Image.open("ayu.png")
    rPegi = requests.get(imgPegi, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')
    # if 'http' not in img : img = 'https://www.pegipegi.com/promo/{}'.format(img)
    deskripsiPegi = BeautifulSoup(requests.get(linknyaPegi).text,'html.parser')
    try: 
        try : temaPegi = deskripsiPegi.find('div','promo-info__description').text
        except : temaPegi = deskripsiPegi.find('div','promo-info__description--center').text
    except : 
        try :
            temaPegi = deskripsiPegi.find('div','wording').text
        except :
            temaPegi = 'kosong'

    db = mysql.connector.connect(host = "127.0.0.1",user="root", password = "", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,durasi,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judulPegi,durasiPegi,imgPegi,temaPegi,linknyaPegi,nilai)
    cursor.execute(sql,val)
    db.commit()
    cursor.close()
    db.close()



for tik in itemsTiket:
    # try : name = tra.find('div','promo-thumb-desc').text
    # except : name = "Tidak memiliki Judul"
    # try : duration = tra.find('div','promo-thumb-duration').text
    # except : duration = "Tidak memiliki masa berlaku"
    try : 
        linknyaTiket = tik['href']
        if 'http' not in linknyaTiket : linknyaTiket = 'https://www.tiket.com{}'.format(linknyaTiket)
    except : linknyaTiket = "Tidak memiliki link detail"
    deskripsiTiket = BeautifulSoup(requests.get(linknyaTiket).text,'html.parser')
    try:
        temaTiket = deskripsiTiket.find('div','promo-detail-description').text
    except : temaTiket = 'kosong'
    try: 
        judulTiket = deskripsiTiket.find('div','promo-detail-title').text
    except : judulTiket = 'kosong'
    try: 
        periodeTiket = deskripsiTiket.find('div','content-wrap').text
    except : periodeTiket = 'kosong'
    try : imageTiket = tik.find('div','img-component').find('img')['data-src']
    except : imageTiket = "Tidak memiliki gambar"
    db = mysql.connector.connect(host = "127.0.0.1",user="root", password = "", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,durasi,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judulTiket, periodeTiket, imageTiket, temaTiket, linknyaTiket,2)
    cursor.execute(sql,val)
    db.commit()
    cursor.close()
    db.close()


for tra in itemsTraveloka:
    try : judulTraveloka = tra.find('div','promo-thumb-desc').text
    except : judulTraveloka = "Tidak memiliki Judul"
    try : durationTraveloka = tra.find('div','promo-thumb-duration').text
    except : durationTraveloka = "Tidak memiliki masa berlaku"
    try : 
        linknyaTraveloka = tra.find('a')['href']
        if 'http' not in linknyaTraveloka : linknyaTraveloka = 'https://www.traveloka.com{}'.format(linknyaTraveloka)
    except : linknyaTraveloka = "Tidak memiliki link detail"
    deskripsiTraveloka = BeautifulSoup(requests.get(linknyaTraveloka).text,'html.parser')
    
    try : temaTraveloka = deskripsiTraveloka.find('div','css-901oao r-1sixt3s r-majxgm r-fdjqy7').find('p').text
        
    except : 
        aa = []
        temas = deskripsiTraveloka.findAll('p', attrs = {'style':'color:rgba(3,18,26,1.00);font-family:MuseoSans,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol;font-size:14px;font-weight:500;line-height:20px;margin-top:0px;margin-right:0px;margin-bottom:0px;margin-left:0px;text-align:center'})
        for a in temas:
                aa.append(a.text)
        temaTraveloka = ' '.join(map(str,aa))
    try : imageTraveloka = tra.find('div','promo-thumb-img').find('img')['src']
    except : imageTraveloka = "Tidak memiliki gambar"
    print("#############################")
    print("TRAVELOKA")
    print("Judul : ",judulTraveloka)
    print("Durasi : ",durationTraveloka)
    print("Deskripsi : ",temaTraveloka)
    print("Link Detail : ",linknyaTraveloka )
    print("Link Image : ",imageTraveloka)
    print("############################# \n")
    db = mysql.connector.connect(
        host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,durasi,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judulTraveloka, durationTraveloka, imageTraveloka, temaTraveloka, linknyaTraveloka, 3)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


for paz in itemsAirpaz:
    judulAirpaz = paz.find('span', 'link normal-b has-text-grey-darker').text
    durationAirpaz = paz.find('span', 'small-b has-text-grey-darker').text
    # imgAirpaz = paz.find('div', 'card-image')
    linkAirpaz = paz.find('div', 'button is-light is-fullwidth')['to']
    try:
        linkAirpaz = paz.find('div', 'button is-light is-fullwidth')['to']
        if 'https' not in linkAirpaz:
            linkAirpaz = 'https://www.airpaz.com{}'.format(linkAirpaz)
    except:
        linkAirpaz = "Tidak ada"
    # imageAirpaz = paz.find('figure','image').find('img').text
    deskripsi = BeautifulSoup(requests.get(linkAirpaz).text, 'html.parser')
    try:
        tema = deskripsi.find('span', 'normal-b is-uppercase').text
    except:
        tema = "Tidak memiliki"
    # imageAirpaz = deskripsi.find('img')
    imageAirpaz = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRSCJcmW8o--f8RjjBGP964tWN6NY9RBw4ww&usqp=CAU"

    print("#############################")
    print("airpaz")
    print("Judul : ", judulAirpaz)
    print("Tema : ", tema)
    print("Duration : ", durationAirpaz)
    print("Link : ", linkAirpaz)
    print("Image : ",imageAirpaz)
    print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,durasi,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judulAirpaz, durationAirpaz, imageAirpaz, tema, linkAirpaz, 4)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

for nusa in itemsNusa:
    try:
        judulNusa = nusa.find('div', {'class': 'txt-ket'}).text
    except:
        judulNusa = "Tidak memiliki judul"
    try:
        imgNusa = nusa.find('img')['src']
        if 'https' not in imgNusa:
            imgNusa = 'https:{}'.format(imgNusa)
    except:
        imgNusa = "Tidak ada"
    try:
        linkNusa = nusa.find('a', 'tmbl-biru')['href']
        if 'https' not in linkNusa:
            linkNusa = 'https:{}'.format(linkNusa)
    except:
        linkNusa = "Tidak ada"

    deskripsi = BeautifulSoup(requests.get(linkNusa).text, 'html.parser')
    try:
        try:
            temaNusa = deskripsi.find('table', 'txtpromo').text
        except:
            temaNusa = deskripsi.find('div', 'line2').text
    except:
        temaNusa = "Tidak memiliki deskripsi"
    duration = "Dapat dilihat deskripsi"

    print("#############################")
    print("Nusatrip")
    print("Judul : ", judulNusa)
    print("image : ", imgNusa)
    print("Detail : ", linkNusa)
    print("Durasi : ", duration)
    print("tema : ", temaNusa)

    print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,durasi,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judulNusa, duration, imgNusa, temaNusa, linkNusa, 5)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    

for gar in itemsGar:
    try:
        img = gar.find('img', 'img-responsive')['src']
        if 'https' not in img:
            img = 'https://www.garuda-indonesia.com{}'.format(img)
    except:
        img = "Tidak ada"
    try:
        link = gar.find('a', 'btn btn-secondary_square pull-right')['href']
        if 'https' not in link:
            link = 'https://www.garuda-indonesia.com{}'.format(link)
    except:
        link = "Tidak ada"
    deskripsi = BeautifulSoup(requests.get(link).text, 'html.parser')
    try:
        judul = deskripsi.find('div', 'section-title').text
    except:
        judul = gar.find('div', 'description').text
    try:
        tema = deskripsi.find('div', 'content').text
    except:
        tema = "Tidak ada"
    duration = "Dapat dilihat di deskripsi"

    # imageAirpaz = paz.find('img')['data-src']
    print("#############################")
    print("Garuda")
    print("Image : ", img)
    print("Judul : ", judul)
    print("link : ", link)
    print("deskripsi : ", tema)
    print("Durasi : ", duration)
    print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,durasi,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judul, duration, img, tema, link, 6)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


for gar in itemsCit:
    judul = gar.text
    try:
        img = gar.find('img')['src']
        if 'https' not in img:
            img = 'https://www.citilink.co.id{}'.format(img)
    except:
        img = "Tidak ada"

    try:
        linka = gar.find('a')['href']
    except:
        continue

    deskripsi = BeautifulSoup(requests.get(linka).text, 'html.parser')
    try:
        try:
            tema = deskripsi.find('ol').text
        except:
            tema = deskripsi.find('div', 'content').find(
                'div', 'sfContentBlock').text
    except:
        tema = "Go to detail link promo"
    duration = "Go to detail link promo"
    print("#############################")
    print("Citi")
    print("Judul : ", judul)
    print("Image : ", img)
    print("Link : ", link)
    print("Tema : ", tema)
    print("durasi : ", duration)
    print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,durasi,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judul, duration, img, tema, link, 7)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

# for gar in itemsToa:
#     try: isa = gar.find('img')['src']
#     except: continue
#     try: judul = gar.find('h2').text
#     except: continue
#     try:
#         desk = gar.find('section', 'summary').text
#     except:
#         desk = "Kosong"
#     try:
#         link = gar.find('figure', 'featured-image').find('a')['href']
#     except:
#         link = "Kosong"
#     # img = gar.find('img')['src']
#     # judul = gar.find('h4', 'violet-color text-uppercase').text
#     # deskripsi = gar.find('p').text
#     print("#############################")
#     print("Batik")
#     print("Image : ", isa)
#     print("Judul : ", judul)
#     print("Link : ", link)
#     print("Deskripsi : ", desk)
#     print("############################# \n")

# for scan in itemsSky:
#     # isa = gar
#     try:
#         img = scan.find('h3').text
#     except:
#         img = "Tidak ada"
#     try:
#         desk = scan.find('li', 'rf rg rh').text
#     except:
#         desk = "Tidak ada"
#     try:
#         link = scan['data-voucher-id']
#         if 'http' not in link:
#             link = 'https://www.cuponation.co.id/kode-promo-skyscanner#voucher-{}'.format(
#                 link)
#     except:
#         link = "Tidak ada"
#     gambar = "https://cdn.cuponation.co.id/120x/images/s/skyscanner_Logo_0.png"
#     # judul = gar.find('h4', 'violet-color text-uppercase').text
#     # deskripsi = gar.find('p').text
#     print("#############################")
#     print("SkyScanner")
#     print("Judul : ", img)
#     print("Link : ", link)
#     print("Image : ", gambar)
#     print("Deskripsi : ", desk)
#     print("############################# \n")
