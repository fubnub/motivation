import praw
import json 
import urllib
import urllib.request
import random
import textwrap
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from xml.dom import minidom

url_lst = []
urls_used = []
list_of_quotes = []
quotes_used = [] 
hdr = {'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'}
name = 'redbot'

def store_as_list(json_file):
    assert type(json_file) == str, "Input must be the string name of the file."
    with open(json_file) as data:
        d = json.load(data)
        for elem in d["wallpapers"]:
            url_lst.append(elem["url"])

def getimg(count, endcount = len(url_lst)): 
    url = url_lst[count]
    req = urllib.request.Request(url, data = None, headers= hdr)
    urllib.request.urlretrieve(req, 'redbot/img/' + str(count) + '.jpg')

def dwnld(count):
    url = url_lst[count]
    req = urllib.request.Request(url, data = None, headers= hdr)
    resource = urllib.request.urlopen(req)
    output = open("file.jpg","wb")
    output.write(resource.read())
    output.close()

def add_text_overlay(txt):
    img=Image.open("file.jpg")
    width, height = img.size
    x,y = width//4, height//4
    font = ImageFont.truetype("/Users/peter/Desktop/code/redbot/fonts/RemachineScript.ttf", height//10)
    draw = ImageDraw.Draw(img)
    lst = txt.split()
    new_text = []
    running_total = 0
    for word in lst:
        if len(word) + running_total >= 40:
            new_text.append('\n')
        new_text.append(word)
    txt = ' '.join(new_text)
    draw.text((x-1, y-1), txt, font=font, fill=(255,255,255))
    draw.text((x+1, y-1), txt, font=font, fill=(255,255,255))
    draw.text((x-1, y+1), txt, font=font, fill=(255,255,255))
    draw.text((x+1, y-1), txt, font=font, fill=(255,255,255))
    draw.text((x, y),txt,(0,0,0),font=font)
    img.save("Result.jpg")

def get_quotes():
    xmldoc = minidom.parse('quotes1.xml')
    itemlist = xmldoc.getElementsByTagName('quote')
    first_quote = itemlist[0].firstChild.nodeValue[3:]
    first_letter = first_quote[0].upper()
    final_first_string = first_letter + first_quote[1:]
    list_of_quotes.append(final_first_string)
    for elem in range(1,len(itemlist)):
        list_of_quotes.append(itemlist[elem].firstChild.nodeValue)

def main():
    store_as_list('data.json')
    get_quotes()
    rand_int_img = random.randint(0,len(url_lst) - 1)
    rand_int_quote = random.randint(0, len(list_of_quotes) - 1)
    while len(list_of_quotes[rand_int_quote]) >= 40:
        rand_int_quote = random.randint(0, len(list_of_quotes) - 1)
    dwnld(rand_int_img)
    text = list_of_quotes[rand_int_quote]
    print(text)
    add_text_overlay(text)

if __name__ == "__main__":
    main()