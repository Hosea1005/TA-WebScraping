from asyncio.windows_events import NULL
from email.mime import image
from os import link
import datetime
from tracemalloc import start
from urllib import request
from webbrowser import get
import requests
import cv2
import io
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
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



#Hotels
hotels = ['archipelago',
          'intiwhiz',
          'aryaduta',
          'artotelgroup',
          'marriot bonvoy'
          ]

#Bulan
bulans = {"januari":1,
          "january":1,
          "jan":1,
          "feb":2,
          "februari":2,
          "february":2,
          "maret":3,
          "mar":3,
          "march":3,
          "april":4,
          "apr":4,
          "mei":5,
          "may":5,
          "mey":5,
          "juni":6,
          "jun":6,
          "june":6,
          "julai":7,
          "juli":7,
          "jul":7,
          "july":7,
          "august":8,
          "agustus":8,
          "aug":8,
          "september":9,
          "sept":9,
          "sep":9,
          "oct":10,
          "okt":10,
          "oktober":10,
          "october":10,
          "nov":11,
          "november":11,
          "des":12,
          "desember":12,
          "december":1,
          }




#Maskapai

pesaw = ['garuda',
         'lion',
         'lion air',
         'citilink',
         'trigana',
         'pelita air',
         'wings',
         'air asia',
         'airasia',
         'tri-mg',
         'nusantara air',
         'indonesia air',
         'sriwijaya',
         'kalstrat',
         'asialink',
         'jayawijaya',
         'batik',
         'nam air',
         'super air jet',
         'susi air',
         'alda trans papua',
         'jetset',
         'flynas',
         'scoot',
         'etihad',
         'japan airlines',
         'jetstar',
         'cebu air',
         'pegasus air',
         'Qatar air',
         'philippine airlines'
         ]


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







# ############Potongan dapat, jenis Dapat, lokasi hotel dapat, maskapai dapat, health sudah diperbaiki ###############
#CLEAR DATE END Start

for peg in itemsPegi:
    nilai = 1
    jenisp = ""
    judulPegi = peg.find('div', 'caption').find('p').text   
    end = ""
    ends = ""
    start = ""
    try:
        durasiPegi = peg.find('p', 'endpromo').text
        waktu = durasiPegi.replace("Periode promo:","")
        if "s.d." in waktu:
            haa = waktu.replace("s.d.","")
            aa = re.sub(' +',' ',haa)
            end = aa.split(' ')
        elif "dan" in waktu:
            haa = waktu.split('dan')
            aa = re.sub(' +',' ',haa[1])
            end = aa.split(' ')
        elif "-" in waktu:
            haa= waktu.split('-')
            end = haa[1]
            tgl = haa[0]
            akhir = end.split(' ')
            bulan = akhir[1]
            tahun = akhir[2]
            start = tgl+ " " + bulan+ " " + tahun
            
        getHariEnd = end[1]
        getBulanEnd = end[2]
        getTahubEnd = end[3]
        
        ass = getTahubEnd+" "+getBulanEnd+" "+getHariEnd
        bulana = bulans[str(getBulanEnd).lower()]
        ends = datetime.date(int(getTahubEnd), bulana, int(getHariEnd))
    except:
        durasiPegi = 'Tidak memiliki durasi'
    linknyaPegi = peg.find('a')['href']
    if "hotel" in judulPegi and "tiket pesawat" in judulPegi:
        jenisp = "flight hotel"
    elif "vaksinasi" in judulPegi:
        jenisp = "health"
    elif "covid" in judulPegi.lower():
        jenisp = "health"
    elif "covid" in linknyaPegi.lower():
        jenisp = "health"
    elif "rapid" in judulPegi.lower():
        jenisp = "health"
    elif "pcr" in judulPegi.lower():
        jenisp = "health"
    elif "hotel" in judulPegi:
        jenisp = "hotel"
    elif "oyo" in judulPegi.lower():
            jenisp = "hotel"
    elif "tiket pesawat" in judulPegi:
        jenisp = "flight"
    elif "dokter" in judulPegi.lower():
        jenisp = "health"
    else:
        jenisp = "Kosong"
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
    lokhot = ""
    maskapai = ""
    lokasi = ""
    for kota in kotas:
        if kota.lower() in judulPegi.lower():
            lokasi = kota
            # print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota
    potongan =""
    for mas in pesaw:
        if mas.lower() in judulPegi.lower():
            maskapai = mas
    for hotl in hotels:
        if hotl.lower() in judulPegi.lower():
            lokhot = hotl
    try:
        if ".000.000" in judulPegi:
            b = judulPegi.split('.000.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + ".000.000"
        elif "00.000" in judulPegi:
            b = judulPegi.split('00.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "50.000" in judulPegi:
            b = judulPegi.split('50.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "50.000"
        elif "0.000" in judulPegi:
            b = judulPegi.split('0.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
        elif "%" in judulPegi:
            b = judulPegi.split('%')
            d= b[0]
            angka = d[-2:]
            potongan = angka + "%"
        elif ".000.000" in textPegi:
            b = textPegi.split('.000.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + ".000.000"
        elif "00.000" in textPegi:
            b = textPegi.split('00.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "50.000" in textPegi:
            b = textPegi.split('50.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "50.000"
        elif "0.000" in textPegi:
            b = textPegi.split('0.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
        elif "%" in textPegi:
            b = textPegi.split('%')
            d= b[0]
            angka = d[-2:]
            potongan = angka + "%"
    except:
        potongan =""

#     print("==================")
# #     print("Judul =", judulPegi)
# #     # print("Lokasi =  ", lokasi)
# #     print("Link Image =  ", imgPegi)
# #     # print("Potongan =  ", potongan)
# #     # print("Lokasi =  ", lokhot)
# #     # print("Jenis =  ", jenisp)
# #     print("Text =  ", textPegi)
#     print("Start =  ", start)
#     print("end =  ", ends)
# #     # print("Deskripsi =  ", temaPegi)
# #     # print("end =  ", len(end))
#     print("==================")

    db = mysql.connector.connect(
    host="127.0.0.1", user="admin", password="=@!#254tecmint", database="centproDB")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (name,location,img,description,link,id_website,start_date,end_date,category,discount,maskapai,lokasi_hotel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    val = (judulPegi, lokasi, imgPegi, temaPegi, linknyaPegi, 1,start,ends,jenisp,potongan,maskapai,lokhot)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()










# ############Jenis dapat, potongan dapat, akomodasi dapat,maskapai, lokasi hotel,###############
#CLEAR DATE

  
for tik in itemsTiket:
    # try : name = tra.find('div','promo-thumb-desc').text
    # except : name = "Tidak memiliki Judul"
    # try : duration = tra.find('div','promo-thumb-duration').text
    # except : duration = "Tidak memiliki masa berlaku"
    maskapai = ""
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
    end = ""
    aq = NULL
    try:
        periodeTiket = deskripsiTiket.find('div', 'content-wrap-col-right').find('p').text
        
        awal = periodeTiket.split('-')
        st = awal[0]
        en = awal[1]
        haa = en.replace(",","")
        aa = re.sub(' +',' ',haa)
        ed = aa.split(' ')
        bula = ed[2]
        bu = bulans[str(bula).lower()]
        end = str(bu)+"-"+ed[1]+"-"+ed[3]
        # end = datetime.date(ed[3], str(bu), ed[1])
        # date_object = datetime.strptime(end, '%Y-%m-%d').date()
        aq = datetime.date(int(ed[3]), bu, int(ed[1]))
        sta = ""
        bulan =""
        tahun =""
        start = ""
        if len(st) == 2 :
            sta = haa.split(' ')
            bula = sta[2]
            bulas = bula.replace(",","")
            bulan = bulans[str(bulas).lower()]
            tahun = sta[3]
            # start = st + bulan +" "+ tahun
            start = datetime.date(int(tahun), bulan, int(st))
        if len(st) > 3:
            # sta = haa.split(' ')
            # bula = sta[2]
            # bulas = bula.replace(",","")
            # bulan = bulans[str(bulas).lower()]
            # tahun = sta[3]
            # start = st+" "+ tahun
            aas = haa.split(' ')
            sta = st.split(' ')
            bula = sta[1]
            bulas = bula.replace(",","")
            bulan = bulans[str(bula).lower()]
            tahun = aas[3]
            hari = sta[0]
            start = datetime.date(int(tahun), bulan, int(hari))        
    except:
        periodeTiket = ''
    imageTiket = ""
    try:
        imageTiket = tik.find('div', 'img-component').find('img')['data-src']
    except:
        imageTiket = "Tidak memiliki gambar"
    akom = ""
    jenis =""
    if "pesawat" in linknyaTiket:
        jenis = "flight"
    elif "campaign" in linknyaTiket:
        if "pesawat" in temaTiket:
            jenis = "flight"
    elif"hotel" in linknyaTiket:
        jenis = "hotel"
    elif"homes" in linknyaTiket:
        jenis = "hotel"
    elif"kereta-api" in linknyaTiket:
        maskapai = "train"
        jenis = "akomodasi"
    elif"sewa-mobil" in linknyaTiket:
        maskapai = "car"
        jenis = "akomodasi"
    elif"airport-transfer" in linknyaTiket:
        maskapai = "jemput"
        jenis = "akomodasi"
    else:
        jenis = ""
    potongan =""
    lokhot = ""
    for mas in pesaw:
        if mas.lower() in judulTiket.lower():
            maskapai = mas
        elif mas.lower() in temaTiket.lower():
            maskapai = mas
    for hotl in hotels:
        if hotl.lower() in judulTiket.lower():
            lokhot = hotl
        elif hotl.lower() in temaTiket.lower():
            lokhot = hotl
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
    try:
        if ".000.000" in judulTiket:
            b = judulTiket.split('.000.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + ".000.000"
        elif "00.000" in judulTiket:
            b = judulTiket.split('00.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "0.000" in judulTiket:
            b = judulTiket.split('0.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
        elif ".000.000" in temaTiket:
            b = temaTiket.split('.000.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + ".000.000"
        elif "00.000" in temaTiket:
            b = temaTiket.split('00.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "0.000" in temaTiket:
            b = temaTiket.split('0.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
        elif "0%" in judulTiket:
            b = judulTiket.split('0%')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0%"
        elif "0%" in temaTiket:
            b = temaTiket.split('0%')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0%"
        elif "100%" in judulTiket:
            potongan = "100%"
        elif ".000.000" in textPegi:
            b = textPegi.split('.000.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + ".000.000"
        elif "00.000" in textPegi:
            b = textPegi.split('00.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "0.000" in textPegi:
            b = textPegi.split('0.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
    except:
        potongan = ""
# #     print("================")
# # # #     # print("Kalimat\n : ", periodeTiket)
# # # #     # print("Start : ", start   )
# # # #     # print("Panjang Start : ", len(st))
# # # #     # print("Bulan : ", bulan)
    
#     print("judul : ", judulTiket)
#     print("Image : ", imageTiket)
# #     print("Start Date : ", start)
# #     print("End Date : ", aq)
# #     print("Lokasi : ", lokasi)
# #     print("Potongan : ", potongan)
# #     print("Maskapai : ", maskapai)
# #     print("Jenis Promo : ", jenis)
# #     print("Deskripsi : ", temaTiket)
# # # #     print("potongan : ", potongan)
# # #     print("Kategori : ", jenis)
#     print("Text : ", textPegi)
#     print("================")
#     # print("End : ", str(bu))
#     print("================")
#     print("Akomodasi : ", maskapai)
    # print("image: ", lokhot)
    # print("akomodasi: ", akom)
#     # db = mysql.connector.connect(
#     # host="127.0.0.1", user="root", password="", database="cenpro")
#     # cursor = db.cursor()
#     # sql = ("INSERT INTO promo (start_time) VALUES (%s)")
#     # val = (str(bu))
#     # cursor.execute(sql, val)
#     # db.commit()
#     # cursor.close()
#     # db.close()
    db = mysql.connector.connect(
    host="127.0.0.1", user="admin", password="=@!#254tecmint", database="centproDB")
    # host="127.0.0.1", user="root", password="", database="cenpro")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (name,location,img,description,link,id_website,start_date,end_date,category,discount,maskapai,lokasi_hotel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    # sql = ("INSERT INTO promo (judul,location,start_time,end_time) VALUES (%s, %s, %s, %s)")
    # val = (judulTiket, lokasi,start,aq)
    val = (judulTiket, lokasi, imageTiket, temaTiket, linknyaTiket,2,start,aq,jenis,potongan,maskapai,lokhot)
    cursor.execute(sql,val)
    db.commit()
    cursor.close()
    db.close()











# ###########Jenis dapaat, potongan Dapat, maskapai sudah dibuat tapi kosong, lokasi hotel dapat###########
# #     #Start dan End Dapat
for paz in itemsAirpaz:
    judulAirpaz = paz.find('span', 'link normal-b has-text-grey-darker').text
    try:
        subJudulAirpaz = paz.find('p', 'normal has-text-grey-dark is-ellipsis m-t-5').text
    except: subJudulAirpaz = ""
    durationAirpaz = paz.find('span', 'small-b has-text-grey-darker').text
    waktu = durationAirpaz.split('-')
    tahun = ""
    endd=""
    akhir = waktu[1]
    date_end = akhir.split(' ')
    hari = date_end[1]
    bulan = bulans[str(date_end[2]).lower()]
    tahun = date_end[3]
    endd = datetime.date(int(tahun), bulan, int(hari))        
    
    star = waktu[0]
    try:
        sta = star.split(' ')
        st = sta[10:]
        starta = ' '.join(map(str, st))
        bula = starta.split(' ')
        hariss = bula[0]
        bulansss = bulans[str(bula[1]).lower()]
        tahun = date_end[3]
        start = datetime.date(int(tahun), bulansss, int(hariss)) 
    except:
        start = " "
    
    
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
    potongan =""
    try:
        if "%" in judulAirpaz:
            b = judulAirpaz.split('%')
            d= b[0]
            angka = d[-2:]
            potongan = angka + "%"
        elif "%" in subJudulAirpaz:
            b = subJudulAirpaz.split('%')
            d= b[0]
            angka = d[-2:]
            potongan = angka + "%"
        elif ".000k" in judulAirpaz:
            b = judulAirpaz.split('.000k')
            d= b[0]
            angka = d[-1]
            potongan = angka + ".000.000"
        elif "00k" in judulAirpaz:
            b = judulAirpaz.split('00k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "0k" in judulAirpaz:
            b = judulAirpaz.split('0k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
        elif "k" in subJudulAirpaz:
            b = subJudulAirpaz.split('k')
            d= b[0]
            angka = d[-1]
            potongan = angka + ".000"
        elif "00k" in subJudulAirpaz:
            b = subJudulAirpaz.split('00k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "0k" in subJudulAirpaz:
            b = subJudulAirpaz.split('0k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
        elif ".000k" in textPegi:
            b = textPegi.split('.000k')
            d= b[0]
            angka = d[-1]
            potongan = angka + ".000.000"
        elif "00k" in textPegi:
            b = textPegi.split('00k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "0k" in textPegi:
            b = textPegi.split('0k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
    except :potongan =""
    maskapai = ""
    lokhot = ""
    for mas in pesaw:
        if mas.lower() in judulAirpaz.lower():
            maskapai = mas
        elif mas.lower() in tema.lower():
            maskapai = mas
    for hotl in hotels:
        if hotl.lower() in judulAirpaz.lower():
            lokhot = hotl
        elif hotl.lower() in tema.lower():
            lokhot = hotl
#     print("#############################")
#     # print("airpaz")
#     # print("Judul : ", judulAirpaz)
#     # print("Potongan : ", potongan)
#     # print("Duration : ", durationAirpaz)
#     print("Start : ", start)
#     print("End : ", endd)
#     # print("End : ", end)
#     # print("Link : ", linkAirpaz)    
#     # # print("Kalimat :\n ",textPegi)
#     # print("Image : ",imageAirpaz)
#     # print("Jenis : ", jenis)
#     # print("Lokasi : ", lokasi)
#     # print("Deskripsi : ", tema)
#     print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="admin", password="=@!#254tecmint", database="centproDB")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (name,location,img,description,link,id_website,start_date,end_date,category,discount,maskapai,lokasi_hotel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    val = (judulAirpaz, lokasi, imageAirpaz, tema, linkAirpaz, 4,start,endd,jenis,potongan,maskapai,lokhot)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    





# # Masih tahap explorasi untuk  date 


# # Start - End Date




# #####################Jenis dapat, Potongan gk dapat,  tidak memiliki maskapai dan lokasi hotel pada website################
# # Belum DAPAT START and Date

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
    potongan=""
    try:
        if ".000.000" in textPegi:
            b = textPegi.split('.000.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + ".000.000"
        elif "00.000" in textPegi:
            b = textPegi.split('00.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "49.000" in tema:
            b = tema.split('49.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "49.000"
        elif "00.000" in tema:
            b = tema.split('00.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "0.000" in textPegi:
            b = textPegi.split('0.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
        elif "00rb" in textPegi:
            b = textPegi.split('00.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "0rb" in textPegi:
            b = textPegi.split('0.000')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
        elif "0%" in textPegi:
            b = textPegi.split('0%')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0%"
        elif "0%" in textPegi:
            b = textPegi.split('0%')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0%"
        elif "100%" in textPegi :
            potongan = "100%"
    except:
        potongan=""
    for kota in kotas:
        if kota.lower() in judul.lower():
            lokasi = kota
            # print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota
#     # if 'http' not in img : img = 'https://www.pegipegi.com/promo/{}'.format(img)
#     print("#############################")
#     print("Citi")
#     print("Judul : ", judul)
#     # print("Text : ", textPegi)
#     print("lokasi : ", lokasi)
#     print("Image : ", img)
#     print("Potongan : ", potongan)
#     print("jenis : ", jenis)
#     print("Link : ", linka)
#     print("Tema : ", tema)
#     print("durasi : ", duration)
#     print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="admin", password="=@!#254tecmint", database="centproDB")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (name,location,img,description,link,id_website,category) VALUES (%s, %s, %s, %s, %s, %s, %s)")
    val = (judul, lokasi, img, tema, linka,7,jenis)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    
    
    
    
    
# ##################Potongan dapat , jenis dapat##############

  
# # End Time dapat , start tidak tersedia
########Date Time Clear###########
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
    
    dur = judulNusa
    dura = dur.split("s.d.")
    durat = dura[1]
    end = durat.replace(" | Terbang:","")
    endd = end.split(" ")
    enddd = datetime.date((int(endd[3])), int( bulans[str(endd[2]).lower()]), int(endd[1]))

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
    potongan = ""
    
    try:
        if "1.2" in judulNusa:
            potongan = "1.200.000"
        elif "1.125" in judulNusa:
            potongan = "1.125.000"
        elif "1.050" in judulNusa:
            potongan = "1.050.000"
        elif "1.5" in textPegi:
            potongan = "1.500.000"
        elif "1.125" in textPegi:
            potongan = "1.125.000"
        elif "1.050" in textPegi:
            potongan = "1.050.000"
    except: potongan=""

#     print("#############################")
#     print(enddd)
#     # print("Judul : ", judulNusa)
#     # print("Text : ", textPegi)
#     # print("image : ", imgNusa)
#     # print("lokasi : ", lokasi)
#     # print("Detail : ", linkNusa)
#     # print("Potongan : ", potongan)
#     # print("tema : ", temaNusa)

#     print("############################# \n")   
    db = mysql.connector.connect(
    host="127.0.0.1", user="admin", password="=@!#254tecmint", database="centproDB")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (name,location,img,description,link,id_website,end_date,category,discount,end_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    val = (judulNusa, lokasi, imgNusa, temaNusa, linkNusa, 5,end,jenis,potongan,enddd)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    
    
    












# ######Potongan harga dapat tapi jenis tidak dapat,maskapai dapat,akommodasi dan lokasi hotel kosong##########


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
        # tema = tem.replace()
    except:
        tema = "Tidak ada"
    duration = "Dapat dilihat di deskripsi"
    rPegi = requests.get(img, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')
    potongan = ""
    b = ""
    if ".000.000" in textPegi:
        b = textPegi.split('.000.000')
        d= b[0]
        angka = d[-1]
        potongan = angka + ".000.000"
    elif "00.000" in textPegi:
        b = textPegi.split('00.000')
        d= b[0]
        angka = d[-1]
        potongan = angka + "00.000"
    elif "50.000" in textPegi:
        b = textPegi.split('50.000')
        d= b[0]
        angka = d[-1]
        potongan = angka + "50.000"
    lokasi = ""
    for kota in kotas:
        if kota.lower() in judul.lower():
            lokasi = kota
            print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota
    maskapai = "garuda"

#     # imageAirpaz = paz.find('img')['data-src']
#     print("#############################")
#     print("Garuda")
#     # print("lokasi : ", lokasi)
#     print("Image : ", img)
#     print("Potongan : ", potongan)
#     print("Judul : ", judul)
#     print("kata : ", textPegi)
#     print("link : ", link)
#     print("deskripsi : ", tema)
#     print("Durasi : ", duration)
#     print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="admin", password="=@!#254tecmint", database="centproDB")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (name,location,img,description,link,id_website,discount) VALUES (%s, %s, %s, %s, %s, %s, %s)")
    val = (judul, lokasi, img, tema, link, 6,potongan)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()










# #####Jenis,Potongan DAPAT, maskapai sudah dapat, lokasi hotel sudah, akomodasi sudah###########

for tra in itemsTraveloka:
    try:
        judulTraveloka = tra.find('div', 'promo-thumb-desc').text
    except:
        judulTraveloka = "Tidak memiliki Judul"
    try:
        aq = tra["data-product"]
    except : aq=""
    akom = ""
    maskapai = ""
    if "flight" in aq:
        jenis = "flight"
    # elif " flight" in aq & "hotel" in aq:
    #     jenis = "hotel"
    elif " hotel" in aq:
        jenis = "hotel"
    elif " train" in aq:
        maskapai = "train"
        jenis = "akomodasi"
    elif " bus" in aq:
        maskapai = "bus"
        jenis = "akomodasi"
    elif " car" in aq:
        maskapai = "car"
        jenis = "akomodasi"
    else :
        jenis = ""
    
    start =""
    saa=""
    end=""
    special =" "
    try:
        durationTraveloka = tra.find('div', 'promo-thumb-duration').find('p').text
    except:
        durationTraveloka = ""
    
    try:
        special = durationTraveloka.replace("!"," ")
        if "Promo period:" in special:
            cleans = special.replace("Promo period: ","")
            special = cleans
            if "until" in special.lower():
                a = special.replace("until","")
                # akhirr = a.strip
                akhirrr = a.split(" ")
                bulansss = bulans[str(akhirrr[3]).lower()]
                end = datetime.date(int(akhirrr[4]), bulansss, int(akhirrr[2]))
                # end = akhirrr
                
            if "-" in special:
                special = special.split("-")
                getAwal = special[0]
                getAkhir = special[1]
                awalss = getAwal.strip().split(" ")
                enda = getAkhir.split(" ")
                bulansss = bulans[str(enda[2]).lower()]
                bulanssa = ""
                try:
                    bulanssa =  bulans[str(awalss[1]).lower()]
                except: bulanssa=""
                try:
                    if bulanssa != "":
                        start = datetime.date(int(enda[3]), bulanssa, int(awalss[0]))    
                    else:
                        start = datetime.date(int(enda[3]), bulansss, int(awalss[0]))
                except:
                    start = ""
                # try:
                #     start = 
                # except:start =""
                try:
                    end = datetime.date(int(enda[3]), bulansss, int(enda[1]))
                except: end=""
        if "Booking period:" in special:
            cleans = special.replace("Booking period: ","")
            special = cleans     
            if "until" in special.lower():
                a = special.replace("until","")
                # akhirr = a.strip
                akhirrr = a.split(" ")
                bulansss = bulans[str(akhirrr[3]).lower()]
                end = datetime.date(int(akhirrr[4]), bulansss, int(akhirrr[2]))          
            if "-" in special:
                special = special.split("-")
                getAwal = special[0]
                getAkhir = special[1]
                awalss = getAwal.strip().split(" ")
                enda = getAkhir.split(" ")
                bulansss = bulans[str(enda[2]).lower()]
                bulanssa = ""
                try:
                    bulanssa =  bulans[str(awalss[1]).lower()]
                except: bulanssa=""
                try:
                    if bulanssa != "":
                        start = datetime.date(int(enda[3]), bulanssa, int(awalss[0]))    
                    else:
                        start = datetime.date(int(enda[3]), bulansss, int(awalss[0]))
                except:
                    start = ""
                try:
                    end = datetime.date(int(enda[3]), bulansss, int(enda[1]))
                except: end=""
        if "Booking period :" in special:
            cleans = special.replace("Booking period : ","")
            special = cleans  
            if "until" in special.lower():
                a = special.replace("until","")
                # akhirr = a.strip
                akhirrr = a.split(" ")
                bulansss = bulans[str(akhirrr[3]).lower()]
                end = datetime.date(int(akhirrr[4]), bulansss, int(akhirrr[2]))
            if "-" in special:
                special = special.split("-")  
                getAwal = special[0]
                getAkhir = special[1]
                awalss = getAwal.strip().split(" ")
                enda = getAkhir.split(" ")  
                bulansss = bulans[str(enda[2]).lower()]
                bulanssa = ""
                try:
                    bulanssa =  bulans[str(awalss[1]).lower()]
                except: bulanssa=""
                try:
                    if bulanssa != "":
                        start = datetime.date(int(enda[3]), bulanssa, int(awalss[0]))    
                    else:
                        start = datetime.date(int(enda[3]), bulansss, int(awalss[0]))
                except:
                    start = ""        
                try:
                    end = datetime.date(int(enda[3]), bulansss, int(enda[1]))
                except: end=""
        
    except: special = " "
    # try:    
    #     san = durationTraveloka.split('\n')
    #     a = san[1]
    #     awal = san[1].split('-', 1)
    #     pisah = awal[0].split(':')
    #     hasil = pisah[1]
    #     if "until" in hasil.lower():
    #         saa = hasil.lower();
    #         z = saa.replace("until","")
    #         end = z
    #     else:
    #         print("ahir",a)
    # except : start =""
        
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
        imageTraveloka = ""
    
    rPegi = requests.get(imageTraveloka, headers=headers)
    imagPegi = Image.open(io.BytesIO(rPegi.content))
    textPegi = pytesseract.image_to_string(imagPegi, lang='eng')
    potongan = ""
    b=" "
    try:
        if "00k" in judulTraveloka:
            b = judulTraveloka.split('00k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "50k" in judulTraveloka:
            b = judulTraveloka.split('50k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "50.000"
        elif "20k" in judulTraveloka:
            b = judulTraveloka.split('20k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "20.000"
        elif "0k" in judulTraveloka:
            b = judulTraveloka.split('0k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
        elif "5k" in judulTraveloka:
            b = judulTraveloka.split('5k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "5.000"
        elif "100%" in judulTraveloka:
            potongan = "100%"
        elif "0%" in judulTraveloka:
            b = judulTraveloka.split('0%')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0%"
        elif "%" in judulTraveloka:
            b = judulTraveloka.split('%')
            d= b[0]
            angka = d[-1]
            potongan = angka + "%"
        
        elif "00k" in textPegi:
            b = textPegi.split('00k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "00.000"
        elif "50k" in textPegi:
            b = textPegi.split('50k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "50.000"
        elif "20k" in textPegi:
            b = textPegi.split('20k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "20.000"
        elif "0k" in textPegi:
            b = textPegi.split('0k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "0.000"
        elif "5k" in textPegi:
            b = textPegi.split('5k')
            d= b[0]
            angka = d[-1]
            potongan = angka + "5.000"
    except: potongan = ""
    lokasi = ""
    for kota in kotas:
        if kota.lower() in judulTraveloka.lower():
            lokasi = kota
            # print(lokasi)
        else:
            if kota.lower() in textPegi.lower():
                lokasi = kota
        if lokasi is None:
            lokasi = check_location(kotas, textPegi.lower())
    
    lokhot = ""
    for mas in pesaw:
        if mas.lower() in judulTraveloka.lower():
            maskapai = mas
        elif mas.lower() in temaTraveloka.lower():
            maskapai = mas
    for hotl in hotels:
        if hotl.lower() in judulTraveloka.lower():
            lokhot = hotl
        elif hotl.lower() in temaTraveloka.lower():
            lokhot = hotl
#     print("#############################")
# #     print("TRAVELOKA")
#     # print("Judul : ",judulTraveloka)
#     print("durasi : ", durationTraveloka)
# #     # print("Time : ", hasil)
# #     print("lokasi", lokasi)
# #     print("Potongan : ", potongan)
#     # print("Link Image : ",imageTraveloka)
# #     print("Jenis : ", jenis)
# #     print("Maskapai : ", maskapai)
# #     print("Kategori : ", jenis)
#     print("Special: ", special)
#     print("Date start: ", start)
#     print("Date end: ", end)
    # print("panjang : ", len(hasil))
    # print("Text From Image", textPegi)
    # print("kata : ", b)
    # print("Durasi : ", durationTraveloka)
    # # print("start : ", hasil)
    # # print("end : ", durationTraveloka)
    # print("Deskripsi : ",temaTraveloka)
    # print("Link Detail : ",linknyaTraveloka )
    # # print("Jenis Akomodasi : ", maskapai)
    # # print("Jenis : ", lokhot)
    # print("############################# \n")
    db = mysql.connector.connect(
    host="127.0.0.1", user="admin", password="=@!#254tecmint", database="centproDB")
    cursor = db.cursor()
    sql = ("INSERT INTO promo (name,location,img,description,link,id_website,discount,category,maskapai,lokasi_hotel,start_date,end_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    val = (judulTraveloka, lokasi, imageTraveloka, temaTraveloka, linknyaTraveloka, 3,potongan,jenis,maskapai,lokhot,start,end)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
