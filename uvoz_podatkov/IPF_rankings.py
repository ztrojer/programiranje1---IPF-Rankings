import requests
import re
import os
import csv

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


def download_url_to_string(url):
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


def save_frontpage(url, directory, filename):
    text = download_url_to_string(url)
    return save_string_to_file(text, directory, filename)


def read_file_to_string(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.'''
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


def page_to_ads(webpage):
    '''Split "page" to a list of advertisement blocks.'''
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


def get_dict_from_ad_block(block):
    sample = re.compile(
        r'.*?>(?P<uvrstitev>\d+?)<?/?[span]*?>?</td><td width="90%.*?'
        r'id="LifterID_(?P<ID_tekmovalca>\d+).*?'
        r'class="lifter-tostr"><a href="/lifters/[A-Z]+/.+\d+/">(?P<ime>[A-Z]+[a-z]*.+)</a></td><td class.*?'
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
      

def ads_from_file(directory, filename):
    '''Parse the ads in filename/directory into a dictionary list.'''
    webpage = read_file_to_string(directory, filename)
    #zamenjam em-dash za 0
    webpage1 = re.sub('&mdash;','0',str(webpage))
    list_of_ads = page_to_ads(webpage1)
    list_of_dicts = []
    for i in range(0, len(list_of_ads)):
        list_of_dicts.append(get_dict_from_ad_block(list_of_ads[i]))
    return list_of_dicts


def write_csv(fieldnames, rows, directory, filename):
    '''Write a CSV file to directory/filename. The fieldnames must be a list of
    strings, the rows a list of dictionaries each mapping a fieldname to a
    cell-value.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None


def write_ads_to_csv(list_of_dicts_ads, directory, filename):
    '''Write a CSV file containing one ad from "ads" on each row.'''
    fieldnames = ['uvrstitev', 'ID_tekmovalca', 'ime', 'razred', 'letnica_rojstva', 'drzava', 'teza', 'pocep', 'potisk_s_prsi', 'mrtvi_dvig', 'skupaj', 'tocke']
    write_csv(fieldnames, list_of_dicts_ads, directory, filename)
    return None


#save_frontpage(url_world_masters_MM1, directory_name, html_world_masters_MM1)
#a = page_to_ads(read_file_to_string(directory_name,html_world_masters_MM1))
#seznam_slovarjev1 = ads_from_file(directory_name, html_world_masters_MM1)
#write_ads_to_csv(seznam_slovarjev1, directory_name, csv_filename_MM1)

#save_frontpage(url_world_masters_MM2, directory_name, html_world_masters_MM2)
#a = page_to_ads(read_file_to_string(directory_name,html_world_masters_MM2))
#seznam_slovarjev2 = ads_from_file(directory_name, html_world_masters_MM2)
#write_ads_to_csv(seznam_slovarjev2, directory_name, csv_filename_MM2)

#save_frontpage(url_world_masters_MM3, directory_name, html_world_masters_MM3)
#a = page_to_ads(read_file_to_string(directory_name,html_world_masters_MM3))
#seznam_slovarjev3 = ads_from_file(directory_name, html_world_masters_MM3)
#write_ads_to_csv(seznam_slovarjev3, directory_name, csv_filename_MM3)

#save_frontpage(url_world_masters_MM4, directory_name, html_world_masters_MM4)
#a = page_to_ads(read_file_to_string(directory_name,html_world_masters_MM4))
#seznam_slovarjev4 = ads_from_file(directory_name, html_world_masters_MM4)
#write_ads_to_csv(seznam_slovarjev4, directory_name, csv_filename_MM4)

#save_frontpage(url_world_masters_WM1, directory_name, html_world_masters_WM1)
#a = page_to_ads(read_file_to_string(directory_name,html_world_masters_WM1))
#seznam_slovarjev5 = ads_from_file(directory_name, html_world_masters_WM1)
#write_ads_to_csv(seznam_slovarjev5, directory_name, csv_filename_WM1)

#save_frontpage(url_world_masters_WM2, directory_name, html_world_masters_WM2)
#a = page_to_ads(read_file_to_string(directory_name,html_world_masters_WM2))
#seznam_slovarjev6 = ads_from_file(directory_name, html_world_masters_WM2)
#write_ads_to_csv(seznam_slovarjev6, directory_name, csv_filename_WM2)

#save_frontpage(url_world_masters_WM3, directory_name, html_world_masters_WM3)
#a = page_to_ads(read_file_to_string(directory_name,html_world_masters_WM3))
#seznam_slovarjev7 = ads_from_file(directory_name, html_world_masters_WM3)
#write_ads_to_csv(seznam_slovarjev7, directory_name, csv_filename_WM3)

#save_frontpage(url_world_masters_WM4, directory_name, html_world_masters_WM4)
#a = page_to_ads(read_file_to_string(directory_name,html_world_masters_WM4))
#seznam_slovarjev8 = ads_from_file(directory_name, html_world_masters_WM4)
#write_ads_to_csv(seznam_slovarjev8, directory_name, csv_filename_WM4)