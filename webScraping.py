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



urlTraveloka = 'https://www.traveloka.com/en-id/promotion'
urlTiket = 'https://www.tiket.com/promo'
urlPegi = 'https://www.pegipegi.com/promo/?f=slider'

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
}
reqTraveloka = requests.get(urlTraveloka, headers=headers)
soupTraveloka = BeautifulSoup(reqTraveloka.text,'html.parser')
reqTiket = requests.get(urlTiket, headers=headers)
soupTiket = BeautifulSoup(reqTiket.text,'html.parser')
reqPegi = requests.get(urlPegi, headers=headers)
soupPegi = BeautifulSoup(reqPegi.text,'html.parser')

itemsTraveloka = soupTraveloka.findAll('div','promo-thumb')
itemsPegi = soupPegi.findAll('div','col-sm-6 col-md-4')
itemsTiket = soupTiket.findAll('a',{'class':'promo-card'})

for peg in itemsPegi : 
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
    sql = ("INSERT INTO promo (judul,durasi,image,deskripsi,link) VALUES (%s, %s, %s, %s, %s)")
    val = (judulPegi,durasiPegi,imgPegi,temaPegi,linknyaPegi)
    cursor.execute(sql,val)
    db.commit()
    cursor.close()
    db.close()
    # print("==============")
    # print("PEGI PEGI")
    # print("Judul : " + judulPegi)
    # print("Masa Berlaku :"+ durasiPegi)
    # print("Image : "+ imgPegi)
    # print("Link ke detail"+linknyaPegi)
    # print("Deskripsi"+temaPegi)
    # print("--------------")


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
    print("#############################")
    print("TIKET.COM")
    print("Judul : ",judulTiket)
    print("Deskripsi : ",temaTiket)
    print("Info Tambahan : "+periodeTiket)
    print("Link Detail : ",linknyaTiket)
    print("Link Image : ",imageTiket)
    print("############################# \n")


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

print(data)





