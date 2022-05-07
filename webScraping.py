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


#Kota
kotas = ['aceh', 'banda aceh', 'langsa','lhokseumawe', 'sabang', 'subulussalam','bali','denpasar','bangka belitung','pangkal pinang',
         'banten','cilegon','serang','tengerang','bengkulu','yogyakarta','gorontalo','jakarta','jambi','sungai penuh',
         'jawa barat','bandung','bekasi','bogor','cimahi','cirebon','depok','sukabumi','tasikmalaya','banjar',
         'jawa tengah','magelang','pekalongan','salatiga','semarang','surakarta','tegal','jawa timur','batu','blitar',
         'kediri','madiun','malang','mojokerto','pasuruan','probolinggo','surabaya','kalimantan barat','pontianak','singkawang',
         'kalimantan selatan','banjarbaru','banjarmasin','kalimantan tengah','palangkaraya','kalimantan timur','balikpapan','bontang','samarinda','kalimantan utara',
         'tarakan','riau','batam','tanjungpinang','lampung','metro','maluku','ternate','tidoro','ambon',
         'tual','bima','mataram','kupang','ntt','papua','jayapura','dumai','sorong','pekanbaru',
         'sulawesi selatan','makasar','palopo','parepare','sulawesi','sulawesi tengah','palu','baubau','kendari','bitung',
         'kotambagu','manado','tomohon','sumatera barat','lubuklinggau','pagar alam','palembang','prabumulih','sekayu','sumatera utara',
         'binjai','gunungsitoli','medan','sidempuan','pematang siantar','siantar','sibolga','tanjung balai','tebing tinggi',"Afghanistan",
         "Albania",
         "Algeria",
         "American Samoa",
         "Andorra",
         "Angola",
         "Anguilla",
         "Antarctica",
         "Antigua and Barbuda",
         "Argentina",
         "Armenia",
         "Aruba",
         "Australia",
         "Austria",
         "Azerbaijan",
         "Bahamas (the)",
         "Bahrain",
         "Bangladesh",
         "Barbados",
         "Belarus",
         "Belgium",
         "Belize",
         "Benin",
         "Bermuda",
         "Bhutan",
         "Bolivia (Plurinational State of)",
         "Bonaire, Sint Eustatius and Saba",
         "Bosnia and Herzegovina",
         "Botswana",
         "Bouvet Island",
         "Brazil",
         "British Indian Ocean Territory (the)",
         "Brunei Darussalam",
         "Bulgaria",
         "Burkina Faso",
         "Burundi",
         "Cabo Verde",
         "Cambodia",
         "Cameroon",
         "Canada",
         "Cayman Islands (the)",
         "Central African Republic (the)",
         "Chad",
         "Chile",
         "China",
         "Christmas Island",
         "Cocos (Keeling) Islands (the)",
         "Colombia",
         "Comoros (the)",
         "Congo (the Democratic Republic of the)",
         "Congo (the)",
         "Cook Islands (the)",
         "Costa Rica",
         "Croatia",
         "Cuba",
         "Curaçao",
         "Cyprus",
         "Czechia",
         "Côte d'Ivoire",
         "Denmark",
         "Djibouti",
         "Dominica",
         "Dominican Republic (the)",
         "Ecuador",
         "Egypt",
         "El Salvador",
         "Equatorial Guinea",
         "Eritrea",
         "Estonia",
         "Eswatini",
         "Ethiopia",
         "Falkland Islands (the) [Malvinas]",
         "Faroe Islands (the)",
         "Fiji",
         "Finland",
         "France",
         "French Guiana",
         "French Polynesia",
         "French Southern Territories (the)",
         "Gabon",
         "Gambia (the)",
         "Georgia",
         "Germany",
         "Ghana",
         "Gibraltar",
         "Greece",
         "Greenland",
         "Grenada",
         "Guadeloupe",
         "Guam",
         "Guatemala",
         "Guernsey",
         "Guinea",
         "Guinea-Bissau",
         "Guyana",
         "Haiti",
         "Heard Island and McDonald Islands",
         "Holy See (the)",
         "Honduras",
         "Hong Kong",
         "Hungary",
         "Iceland",
         "India",
         "Indonesia",
         "Iran (Islamic Republic of)",
         "Iraq",
         "Ireland",
         "Isle of Man",
         "Israel",
         "Italy",
         "Jamaica",
         "Japan",
         "Jersey",
         "Jordan",
         "Kazakhstan",
         "Kenya",
         "Kiribati",
         "Korea (the Democratic People's Republic of)",
         "Korea (the Republic of)",
         "Kuwait",
         "Kyrgyzstan",
         "Lao People's Democratic Republic (the)",
         "Latvia",
         "Lebanon",
         "Lesotho",
         "Liberia",
         "Libya",
         "Liechtenstein",
         "Lithuania",
         "Luxembourg",
         "Macao",
         "Madagascar",
         "Malawi",
         "Malaysia",
         "Maldives",
         "Mali",
         "Malta",
         "Marshall Islands (the)",
         "Martinique",
         "Mauritania",
         "Mauritius",
         "Mayotte",
         "Mexico",
         "Micronesia (Federated States of)",
         "Moldova (the Republic of)",
         "Monaco",
         "Mongolia",
         "Montenegro",
         "Montserrat",
         "Morocco",
         "Mozambique",
         "Myanmar",
         "Namibia",
         "Nauru",
         "Nepal",
         "Netherlands (the)",
         "New Caledonia",
         "New Zealand",
         "Nicaragua",
         "Niger (the)",
         "Nigeria",
         "Niue",
         "Norfolk Island",
         "Northern Mariana Islands (the)",
         "Norway",
         "Oman",
         "Pakistan",
         "Palau",
         "Palestine, State of",
         "Panama",
         "Papua New Guinea",
         "Paraguay",
         "Peru",
         "Philippines (the)",
         "Pitcairn",
         "Poland",
         "Portugal",
         "Puerto Rico",
         "Qatar",
         "Republic of North Macedonia",
         "Romania",
         "Russian Federation (the)",
         "Rwanda",
         "Réunion",
         "Saint Barthélemy",
         "Saint Helena, Ascension and Tristan da Cunha",
         "Saint Kitts and Nevis",
         "Saint Lucia",
         "Saint Martin (French part)",
         "Saint Pierre and Miquelon",
         "Saint Vincent and the Grenadines",
         "Samoa",
         "San Marino",
         "Sao Tome and Principe",
         "Saudi Arabia",
         "Senegal",
         "Serbia",
         "Seychelles",
         "Sierra Leone",
         "Singapore",
         "Sint Maarten (Dutch part)",
         "Slovakia",
         "Slovenia",
         "Solomon Islands",
         "Somalia",
         "South Africa",
         "South Georgia and the South Sandwich Islands",
         "South Sudan",
         "Spain",
         "Sri Lanka",
         "Sudan (the)",
         "Suriname",
         "Svalbard and Jan Mayen",
         "Sweden",
         "Switzerland",
         "Syrian Arab Republic",
         "Taiwan",
         "Tajikistan",
         "Tanzania, United Republic of",
         "Thailand",
         "Timor-Leste",
         "Togo",
         "Tokelau",
         "Tonga",
         "Trinidad and Tobago",
         "Tunisia",
         "Turkey",
         "Turkmenistan",
         "Turks and Caicos Islands (the)",
         "Tuvalu",
         "Uganda",
         "Ukraine",
         "United Arab Emirates (the)",
         "United Kingdom of Great Britain and Northern Ireland (the)",
         "United States Minor Outlying Islands (the)",
         "United States of America (the)",
         "Uruguay",
         "Uzbekistan",
         "Vanuatu",
         "Venezuela (Bolivarian Republic of)",
         "Viet Nam",
         "Virgin Islands (British)",
         "Virgin Islands (U.S.)",
         "Wallis and Futuna",
         "Western Sahara",
         "Yemen",
         "Zambia",
         "Zimbabwe",
         "Åland Islands"]


#check lokasi
def check_location(kot,kal):
    for kota in kot:
        kota.lower()
        if kota in kal:
            print(kota)
        else:
            continue
#Scraping Sudah Fix
    

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
    rPegi = requests.get(img, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')
    lokasi = ""
    for kota in kotas:
        if kota.lower() in judul.lower():
            lokasi = kota
            print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota
        

    # imageAirpaz = paz.find('img')['data-src']
    print("#############################")
    print("Garuda")
    print("lokasi : ", lokasi)
    # print("Image : ", img)
    # print("Judul : ", judul)
    # print("link : ", link)
    # print("deskripsi : ", tema)
    # print("Durasi : ", duration)
    print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,location,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judul, lokasi, img, tema, link, 6)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

Jenis


for tra in itemsTraveloka:
    try:
        judulTraveloka = tra.find('div', 'promo-thumb-desc').text
    except:
        judulTraveloka = "Tidak memiliki Judul"
    try:
        jenis = tra["data-product"]
    except:
        jenis = "Tidak memiliki Judul"
    try:
        durationTraveloka = tra.find('div', 'promo-thumb-duration').text
        san = durationTraveloka.split('\n')
        a = san[1]
        awal = san[1].split('-', 1)
        pisah = awal[0].split(':')
        hasil = pisah[1]
        start = hasil.split("-")

    except:
        durationTraveloka = "Tidak memiliki masa berlaku"
    try:
        linknyaTraveloka = tra.find('a')['href']
        if 'http' not in linknyaTraveloka:
            linknyaTraveloka = 'https://www.traveloka.com{}'.format(
                linknyaTraveloka)
    except:
        linknyaTraveloka = "Tidak memiliki link detail"
    deskripsiTraveloka = BeautifulSoup(
        requests.get(linknyaTraveloka).text, 'html.parser')

    try:
        temaTraveloka = deskripsiTraveloka.find(
            'div', 'css-901oao r-1sixt3s r-majxgm r-fdjqy7').find('p').text

    except:
        aa = []
        temas = deskripsiTraveloka.findAll('p', attrs={
                                           'style': 'color:rgba(3,18,26,1.00);font-family:MuseoSans,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol;font-size:14px;font-weight:500;line-height:20px;margin-top:0px;margin-right:0px;margin-bottom:0px;margin-left:0px;text-align:center'})
        for a in temas:
            aa.append(a.text)
        temaTraveloka = ' '.join(map(str, aa))
    try:
        inga = tra.find('div', 'promo-thumb-img').find('img')['src']
        pisah = inga.split("?")
        imageTraveloka = pisah[0]
        
    except:
        imageTraveloka = "Tidak memiliki gambar"
    
    rPegi = requests.get(imageTraveloka, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')
    lokasi = ""
    for kota in kotas:
        if kota.lower() in judulTraveloka.lower():
            lokasi = kota
            print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota
        # if lokasi is None:
        #     lokasi = check_location(kotas, textPegi.lower())
    print("#############################")
    print("TRAVELOKA")
    print("kalimat", textPegi)
    print("lokasi", lokasi)
    # print("Judul : ",judulTraveloka)
    # print("Durasi : ", durationTraveloka)
    # print("start : ", hasil)
    # print("end : ", durationTraveloka)
    # print("Deskripsi : ",temaTraveloka)
    # print("Link Detail : ",linknyaTraveloka )
    print("Link Image : ",imageTraveloka)
    # print("Jenis : ", jenis)
    print("############################# \n")
    db = mysql.connector.connect(
        host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,location,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judulTraveloka, lokasi, imageTraveloka, temaTraveloka, linknyaTraveloka, 3)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

for peg in itemsPegi:
    nilai = 1
    asd = ""
    judulPegi = peg.find('div', 'caption').find('p').text

    if "hotel" in judulPegi and "tiket pesawat" in judulPegi:
        asd = "flight hotel"
        print("flight hotel")
        jenisp = asd
    elif "hotel" in judulPegi:
        jenisp = "hotel"
        print("hotel")
    elif "tiket pesawat" in judulPegi:
        jenisp = "flight"
        print("flight")
    else:
        jenisp = "Kosong"

    try:
        durasiPegi = peg.find('p', 'endpromo').text
    except:
        durasiPegi = 'Tidak memiliki durasi'
    linknyaPegi = peg.find('a')['href']
    imgPegi = peg.find('div', 'thumbnail').find('img')['src']
    if 'http' not in imgPegi:
        imgPegi = 'https://www.pegipegi.com/promo/{}'.format(imgPegi)
    # img = Image.open("ayu.png")
    rPegi = requests.get(imgPegi, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')
    # if 'http' not in img : img = 'https://www.pegipegi.com/promo/{}'.format(img)
    deskripsiPegi = BeautifulSoup(
        requests.get(linknyaPegi).text, 'html.parser')
    try:
        try:
            temaPegi = deskripsiPegi.find(
                'div', 'promo-info__description').text
        except:
            temaPegi = deskripsiPegi.find(
                'div', 'promo-info__description--center').text
    except:
        try:
            temaPegi = deskripsiPegi.find('div', 'wording').text
        except:
            temaPegi = 'kosong'
    rPegi = requests.get(imgPegi, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')
    lokasi = ""
    for kota in kotas:
        if kota.lower() in judulPegi.lower():
            lokasi = kota
            print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota

    print("==================")
    print("jenis ", lokasi)
    print("jenis ", jenisp)
    print("==================")

    db = mysql.connector.connect(
        host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,location,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judulPegi, lokasi, imgPegi, jenisp, linknyaPegi, nilai)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


for tik in itemsTiket:
    # try : name = tra.find('div','promo-thumb-desc').text
    # except : name = "Tidak memiliki Judul"
    # try : duration = tra.find('div','promo-thumb-duration').text
    # except : duration = "Tidak memiliki masa berlaku"
    try:
        linknyaTiket = tik['href']
        if 'http' not in linknyaTiket:
            linknyaTiket = 'https://www.tiket.com{}'.format(linknyaTiket)
    except:
        linknyaTiket = "Tidak memiliki link detail"

    deskripsiTiket = BeautifulSoup(
        requests.get(linknyaTiket).text, 'html.parser')
    try:
        temaTiket = deskripsiTiket.find('div', 'promo-detail-description').text
    except:
        temaTiket = 'kosong'
    try:
        judulTiket = deskripsiTiket.find('div', 'promo-detail-title').text
    except:
        judulTiket = 'kosong'
    try:
        periodeTiket = deskripsiTiket.find('div', 'content-wrap').text
    except:
        periodeTiket = 'kosong'
    try:
        imageTiket = tik.find('div', 'img-component').find('img')['data-src']
    except:
        imageTiket = "Tidak memiliki gambar"
    if "pesawat" in linknyaTiket:
        jenis = "flight"
    elif"hotel" in linknyaTiket:
        jenis = "hotel"
    else:
        jenis = "lainnya"
    rPegi = requests.get(imageTiket, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')
    lokasi = ""
    for kota in kotas:
        if kota.lower() in judulTiket.lower():
            lokasi = kota
            print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota
    print(jenis)
    db = mysql.connector.connect(host = "127.0.0.1",user="root", password = "", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,location,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judulTiket, lokasi, imageTiket, temaTiket, linknyaTiket,2)
    cursor.execute(sql,val)
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

    if "flight" in linkAirpaz:
        jenis = "flight"
    elif "hotel" in linkAirpaz:
        jenis = "hotel"
    elif "Flight" in linkAirpaz:
        jenis = "flight"
    elif "Hotel" in linkAirpaz:
        jenis = "hotel"
    else:
        jenis = "lainnya"
    rPegi = requests.get(imageAirpaz, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')
    lokasi = ""
    for kota in kotas:
        if kota.lower() in judulAirpaz.lower():
            lokasi = kota
            print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota
    print("#############################")
    # print("airpaz")
    # print("Judul : ", judulAirpaz)
    # print("Tema : ", tema)
    # print("Duration : ", durationAirpaz)
    # print("Link : ", linkAirpaz)
    # print("Image : ",imageAirpaz)
    print("Jenis : ", jenis)
    print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,location,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judulAirpaz, lokasi, imageAirpaz, tema, linkAirpaz, 4)
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

    if "pesawat" in linkNusa and "hotel" in linkNusa:
        jenis = "flight hotel"
    elif "hotel" in linkNusa:
        jenis = "hotel"
    elif "pesawat" in linkNusa:
        jenis = "flight"
    else:
        jenis = "lainnya"
    rPegi = requests.get(imgNusa, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')
    lokasi = ""
    for kota in kotas:
        if kota.lower() in judulNusa.lower():
            lokasi = kota
            print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota

#     print("#############################")
#     print(jenis)
#     # print("Judul : ", judulNusa)
#     # print("image : ", imgNusa)
#     # print("Detail : ", linkNusa)
#     # print("Durasi : ", duration)
#     # print("tema : ", temaNusa)

    print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,location,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judulNusa, lokasi, imgNusa, temaNusa, linkNusa, 5)
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

    rPegi = requests.get(img, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')

    if "tiket" in textPegi.lower() and "hotel" in textPegi.lower():
        jenis = "flight hotel"
    elif "tiket" in textPegi.lower():
        jenis = "flight"
    elif "hotel" in textPegi.lower():
        jenis = "hotel"
    else:
        jenis = "lainnya"
    lokasi = ""
    for kota in kotas:
        if kota.lower() in judul.lower():
            lokasi = kota
            print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota
    # if 'http' not in img : img = 'https://www.pegipegi.com/promo/{}'.format(img)
    print("#############################")
    print("Citi")
    # print("Judul : ", judul)
    print("Image : ", textPegi)
    print("jenis : ", jenis)
    # print("Link : ", link)
    # print("Tema : ", tema)
    # print("durasi : ", duration)
    print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (judul,location,image,deskripsi,link,id_website) VALUES (%s, %s, %s, %s, %s, %s)")
    val = (judul, lokasi, img, tema, link, 7)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
