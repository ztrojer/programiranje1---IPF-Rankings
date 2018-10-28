import requests
import re
import os
import csv


def prenesi_url(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Napaka!')
        return None
    return r.text


def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


def shrani_stran(url, directory, filename):
    text = prenesi_url(url)
    return save_string_to_file(text, directory, filename)


def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


def razdeli_na_dele(webpage):
    sample1 = re.compile(
        r'</td><td class="center" id="Place_\d+"><a name=".\d+"></a'
    )
    sample2 = re.compile(
        r'</td></tr><tr id="resrow\d+"><td cl<a href="/lifters'
    )
    list = re.split(sample1, webpage)
    last = list[-1]
    last = re.split(sample2, last)
    list[-1] = last[0]
    return list[1:]


def poisci_podatke(block):
    sample = re.compile(
        r'.*?>(?P<uvrstitev>(\d+?|DQ))<?/?[span]*?>?</td><td width="90%.*?'
        r'id="LifterID_(?P<ID_tekmovalca>\d+).*?'
        r'class="lifter-tostr"><a href="/lifters/[A-Z]+/.+\d+/">(?P<ime>\w+[a-z]*.+)</a></td><td class.*?'
        r'id="Age_\d+"><span title=".+">(?P<razred>M\d+)</span>.*?'
        r'id="BirthYear_\d+">(?P<letnica_rojstva>\d{4})</td><td.*?'
        r'href="/locations/[A-Z]+/" title="(?P<drzava>[A-Z]+.*)"><span class.*?'
        r'<td id="Weight_\d+">(?P<teza>\d+\.\d+)</td>.*?'
        r'>(?P<pocep>(0|\d+?.?\d+?))<?[sup]*?.*?>?<?/?[span]*?>?</span></td><td class="center" id="Bench_\d+".*?'
        r'>(?P<potisk_s_prsi>(0|\d+?.?\d+?))<?[sup]*?.*?>?<?/?[span]*?>?</span></td><td class="center" id="Dead_\d+">.*?'
        r'>(?P<mrtvi_dvig>(0|\d+?.?\d+?))<?[sup]*?.*?>?<?/?[span]*?>?</span></td><td class="center" id="Total_\d+".*?'
        r'>(?P<skupaj>(0|\d+?.?\d+?))<?[sup]*?.*?>?<?/?[span]*?>?</span></td><td class="center" id="Points_\d+".*?'
        r'>(?P<tocke>(0|\d+?.?\d+?))<?/?[span]*?>?</td><td class="center" id="Team_\d+.*?',
        re.DOTALL
    )
    for expression in sample.finditer(block):
        dict = expression.groupdict()
    return dict

def pridobi_slovar(directory, filename):
    webpage = read_file_to_string(directory, filename)
    #zamenjam em-dash za 0
    webpage1 = re.sub('&mdash;','0',str(webpage))
    list_of_ads = razdeli_na_dele(webpage1)
    list_of_dicts = []
    for i in range(0, len(list_of_ads)):
        list_of_dicts.append(poisci_podatke(list_of_ads[i]))
    return list_of_dicts


def zapisi_csv(fieldnames, rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None


def zapisi_podatke_v_csv(list_of_dicts_ads, directory, filename):
    fieldnames = ['uvrstitev', 'ID_tekmovalca', 'ime', 'razred', 'letnica_rojstva', 'drzava', 'teza', 'pocep', 'potisk_s_prsi', 'mrtvi_dvig', 'skupaj', 'tocke']
    zapisi_csv(fieldnames, list_of_dicts_ads, directory, filename)
    return None

directory_name = 'uvoz_podatkov'

url_world_masters_MM1 = ('http://en.allpowerlifting.com/results/IPF/2018/world-masters-powerlifting-championships/')
html_world_masters_MM1 = 'world_masters_MM1.html'
csv_filename_MM1 = 'world_masters_MM1.csv'

url_world_masters_MM2 = ('http://en.allpowerlifting.com/results/IPF/2018/world-masters-powerlifting-championships/mm2/')
html_world_masters_MM2 = 'world_masters_MM2.html'
csv_filename_MM2 = 'world_masters_MM2.csv'

url_world_masters_MM3 = ('http://en.allpowerlifting.com/results/IPF/2018/world-masters-powerlifting-championships/mm3/')
html_world_masters_MM3 = 'world_masters_MM3.html'
csv_filename_MM3 = 'world_masters_MM3.csv'

url_world_masters_MM4 = ('http://en.allpowerlifting.com/results/IPF/2018/world-masters-powerlifting-championships/mm4/')
html_world_masters_MM4 = 'world_masters_MM4.html'
csv_filename_MM4 = 'world_masters_MM4.csv'

url_world_masters_WM1 = ('http://en.allpowerlifting.com/results/IPF/2018/world-masters-powerlifting-championships/wm1/')
html_world_masters_WM1 = 'world_masters_WM1.html'
csv_filename_WM1 = 'world_masters_WM1.csv'

url_world_masters_WM2 = ('http://en.allpowerlifting.com/results/IPF/2018/world-masters-powerlifting-championships/wm2/')
html_world_masters_WM2 = 'world_masters_WM2.html'
csv_filename_WM2 = 'world_masters_WM2.csv'

url_world_masters_WM3 = ('http://en.allpowerlifting.com/results/IPF/2018/world-masters-powerlifting-championships/wm3/')
html_world_masters_WM3 = 'world_masters_WM3.html'
csv_filename_WM3 = 'world_masters_WM3.csv'

url_world_masters_WM4 = ('http://en.allpowerlifting.com/results/IPF/2018/world-masters-powerlifting-championships/wm4/')
html_world_masters_WM4 = 'world_masters_WM4.html'
csv_filename_WM4 = 'world_masters_WM4.csv'

url_6th_world_classic_MM1 = ('http://en.allpowerlifting.com/results/IPF/2018/6th-world-classic-championships/mm1/')
html_6th_world_classic_MM1 = '6th_world_classic_MM1.html'
csv_6th_world_classic_MM1 = '6th_world_classic_MM1.csv'

url_6th_world_classic_MM2 = ('http://en.allpowerlifting.com/results/IPF/2018/6th-world-classic-championships/mm2/')
html_6th_world_classic_MM2 = '6th_world_classic_MM2.html'
csv_6th_world_classic_MM2 = '6th_world_classic_MM2.csv'

url_6th_world_classic_MM3 = ('http://en.allpowerlifting.com/results/IPF/2018/6th-world-classic-championships/mm3/')
html_6th_world_classic_MM3 = '6th_world_classic_MM3.html'
csv_6th_world_classic_MM3 = '6th_world_classic_MM3.csv'

url_6th_world_classic_MM4 = ('http://en.allpowerlifting.com/results/IPF/2018/6th-world-classic-championships/mm4/')
html_6th_world_classic_MM4 = '6th_world_classic_MM4.html'
csv_6th_world_classic_MM4 = '6th_world_classic_MM4.csv'

url_6th_world_classic_MM4 = ('http://en.allpowerlifting.com/results/IPF/2018/6th-world-classic-championships/mm4/')
html_6th_world_classic_MM4 = '6th_world_classic_MM4.html'
csv_6th_world_classic_MM4 = '6th_world_classic_MM4.csv'

url_6th_world_classic_WM1 = ('http://en.allpowerlifting.com/results/IPF/2018/6th-world-classic-championships/wm1/')
html_6th_world_classic_WM1  = '6th_world_classic_WM1.html'
csv_6th_world_classic_WM1  = '6th_world_classic_WM1.csv'

url_6th_world_classic_WM2 = ('http://en.allpowerlifting.com/results/IPF/2018/6th-world-classic-championships/wm2/')
html_6th_world_classic_WM2  = '6th_world_classic_WM2.html'
csv_6th_world_classic_WM2 = '6th_world_classic_WM2.csv'

url_6th_world_classic_WM3 = ('http://en.allpowerlifting.com/results/IPF/2018/6th-world-classic-championships/wm3/')
html_6th_world_classic_WM3  = '6th_world_classic_WM3.html'
csv_6th_world_classic_WM3 = '6th_world_classic_WM3.csv'

url_6th_world_classic_WM4 = ('http://en.allpowerlifting.com/results/IPF/2018/6th-world-classic-championships/wm4/')
html_6th_world_classic_WM4  = '6th_world_classic_WM4.html'
csv_6th_world_classic_WM4 = '6th_world_classic_WM4.csv'

#shrani_stran(url_world_masters_MM1, directory_name, html_world_masters_MM1)
#seznam_slovarjev1 = pridobi_slovar(directory_name, html_world_masters_MM1)
#zapisi_podatke_v_csv(seznam_slovarjev1, directory_name, csv_filename_MM1)

#shrani_stran(url_world_masters_MM2, directory_name, html_world_masters_MM2)
#seznam_slovarjev2 = pridobi_slovar(directory_name, html_world_masters_MM2)
#zapisi_podatke_v_csv(seznam_slovarjev2, directory_name, csv_filename_MM2)

#shrani_stran(url_world_masters_MM3, directory_name, html_world_masters_MM3)
#seznam_slovarjev3 = pridobi_slovar(directory_name, html_world_masters_MM3)
#zapisi_podatke_v_csv(seznam_slovarjev3, directory_name, csv_filename_MM3)

#shrani_stran(url_world_masters_MM4, directory_name, html_world_masters_MM4)
#seznam_slovarjev4 = pridobi_slovar(directory_name, html_world_masters_MM4)
#zapisi_podatke_v_csv(seznam_slovarjev4, directory_name, csv_filename_MM4)

#shrani_stran(url_world_masters_WM1, directory_name, html_world_masters_WM1)
#seznam_slovarjev5 = pridobi_slovar(directory_name, html_world_masters_WM1)
#zapisi_podatke_v_csv(seznam_slovarjev5, directory_name, csv_filename_WM1)

#shrani_stran(url_world_masters_WM2, directory_name, html_world_masters_WM2)
#seznam_slovarjev6 = pridobi_slovar(directory_name, html_world_masters_WM2)
#zapisi_podatke_v_csv(seznam_slovarjev6, directory_name, csv_filename_WM2)

#shrani_stran(url_world_masters_WM3, directory_name, html_world_masters_WM3)
#seznam_slovarjev7 = pridobi_slovar(directory_name, html_world_masters_WM3)
#zapisi_podatke_v_csv(seznam_slovarjev7, directory_name, csv_filename_WM3)

#shrani_stran(url_world_masters_WM4, directory_name, html_world_masters_WM4)
#seznam_slovarjev8 = pridobi_slovar(directory_name, html_world_masters_WM4)
#zapisi_podatke_v_csv(seznam_slovarjev8, directory_name, csv_filename_WM4)

#shrani_stran(url_6th_world_classic_MM1, directory_name, html_6th_world_classic_MM1)
#seznam_slovarjev9 = pridobi_slovar(directory_name, html_6th_world_classic_MM1)
#zapisi_podatke_v_csv(seznam_slovarjev9, directory_name, csv_6th_world_classic_MM1)

#shrani_stran(url_6th_world_classic_MM2, directory_name, html_6th_world_classic_MM2)
#seznam_slovarjev10 = pridobi_slovar(directory_name, html_6th_world_classic_MM2)
#zapisi_podatke_v_csv(seznam_slovarjev10, directory_name, csv_6th_world_classic_MM2)

#shrani_stran(url_6th_world_classic_MM3, directory_name, html_6th_world_classic_MM3)
#seznam_slovarjev11 = pridobi_slovar(directory_name, html_6th_world_classic_MM3)
#zapisi_podatke_v_csv(seznam_slovarjev11, directory_name, csv_6th_world_classic_MM3)

#shrani_stran(url_6th_world_classic_MM4, directory_name, html_6th_world_classic_MM4)
#seznam_slovarjev12 = pridobi_slovar(directory_name, html_6th_world_classic_MM4)
#zapisi_podatke_v_csv(seznam_slovarjev12, directory_name, csv_6th_world_classic_MM4)

#shrani_stran(url_6th_world_classic_WM1, directory_name, html_6th_world_classic_WM1)
#seznam_slovarjev13 = pridobi_slovar(directory_name, html_6th_world_classic_WM1)
#zapisi_podatke_v_csv(seznam_slovarjev13, directory_name, csv_6th_world_classic_WM1)

#shrani_stran(url_6th_world_classic_WM2, directory_name, html_6th_world_classic_WM2)
#seznam_slovarjev14 = pridobi_slovar(directory_name, html_6th_world_classic_WM2)
#zapisi_podatke_v_csv(seznam_slovarjev14, directory_name, csv_6th_world_classic_WM2)

#shrani_stran(url_6th_world_classic_WM3, directory_name, html_6th_world_classic_WM3)
#seznam_slovarjev15 = pridobi_slovar(directory_name, html_6th_world_classic_WM3)
#zapisi_podatke_v_csv(seznam_slovarjev15, directory_name, csv_6th_world_classic_WM3)

#shrani_stran(url_6th_world_classic_WM4, directory_name, html_6th_world_classic_WM4)
#seznam_slovarjev16 = pridobi_slovar(directory_name, html_6th_world_classic_WM4)
#zapisi_podatke_v_csv(seznam_slovarjev16, directory_name, csv_6th_world_classic_WM4)