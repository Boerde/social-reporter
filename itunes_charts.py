import urllib.request as ul
import xml.etree.ElementTree as ET
import config
import csv
from datetime import date


#create list
data = [0] * 2
data[0] = date.today()
#get xml from itunes
xml_data = ul.urlopen(config.url_to_podcast_chart)

#parse xml
tree = ET.parse(xml_data)
root = tree.getroot()
#find entrys
entrys = root.findall('{http://www.w3.org/2005/Atom}entry')

i = 0
#search for our id
for e in entrys:
	#counter for place
	i += 1
	if e.find("{http://www.w3.org/2005/Atom}id").attrib['{http://itunes.apple.com/rss}id'] == config.itunes_store_id:
		break
		print (e)
#print place
print (i)
with open('daily_podcast_charts.txt', 'a') as f:
	f.write(str(i) + '\n')

data[1] = str(i)
with open('daily_podcast_charts.csv', 'a') as f:
	data_writer = csv.writer(f)
	data_writer.writerow(data)
