import urllib.request as ul
import re
import config
import sys
from datetime import date
from datetime import timedelta

def print_row(i):
	procent = round ((int(follower[i])/int(row[i]) - 1) ,3)
	#format outpu
	output = (row_names[i] +" {:,d}" + ' ' + "{:+.1%}" + '\n').format(int(follower[i]), procent) 
	#because of the german '.'
	print(output.replace(',', '.'))

#create list
follower = [0] * 11

if len(sys.argv) < 5:
	sys.stderr.write("Pls give 4 Arguments!\n 1. website visits Konstanz\n 2.website visits Düsseldorf\n 3. email recipients Konstanz\n 4. email recipients Düsseldorf\n 5. Podcast downloads!\n")
	sys.exit(-1)

#add date
follower[0] = date.today()

#website Konstanz
follower[1] = sys.argv[1]
#website Düsseldorf 
follower[2] = sys.argv[2]

#email Konstanz
follower[3] = sys.argv[3]

#email Düsseldorf
follower[4] = sys.argv[4]

#facebook
hp = ul.urlopen("http://graph.facebook.com/hillsong.germany")
res = re.findall('"likes":\d+', hp.read().decode("utf-8"))
follower[5] = re.findall('\d+.?\d+', res[0])[0].replace(".", "")

#twitter
hp = ul.urlopen(config.url_twitter_acc)
#res = re.findall('followers_count.*\d+.?\d+', hp.read().decode("utf-8"))
#print(hp.read().decode("utf-8"));
res = re.findall('follower.*\d*.?\d+', hp.read().decode("utf-8"))
#print(res)
follower[6] = re.findall('\d+.?\d+', res[0])[0].replace(".", "")
#print(int(follower['twitter']))

#Instagramm
hp = ul.urlopen(config.url_instagram_acc)
res = re.findall('followed_by":\d*', hp.read().decode("utf-8"))
follower[7] = re.findall('\d+.?\d+', res[0])[0].replace(".", "")
#print(int(follower['instagram']))

#gplus
hp = ul.urlopen(config.url_gplus_acc)
res = re.findall('\d* Personen', hp.read().decode("utf-8"))
follower[8] = re.findall('\d+.?\d+', res[0])[0].replace(".", "")
#print(int(follower['gplus']))

#podcast Downloads
follower[9] = sys.argv[5]

#itunes charts
with open ('daily_podcast_charts.txt') as f:
	tmp = 0
	i = 0
	#get all recorded numbers and sum them up
	for number in f:
		tmp += int(number)
		i += 1
	#get the mean out of them
	mean = tmp / i
	follower[10] = int(mean)
	

import csv
#get values of the week before
with open ('social_data.csv', 'r') as f:
	c_reader = csv.reader(f, delimiter=',')
	i = 0
	#get to last line
	for row in c_reader:
		if i == 0:
			row_names = row
		i +=1
		continue
now = date.today()
print("HILLSONG GERMANY ONLINE - REPORT " + str(now.year))
print('')
print("Calender Week " + str(now.strftime('%U')) + ' (' + str((now - timedelta(7)).strftime('%d.%m.')) + ' - ' + str((now - timedelta(1)).strftime('%d.%m.')) + ')')
print('')
#website Konstanz
print_row(1)
#website Düsseldorf
print_row(2)
#email Konstanz
print_row(3)
#email Düsseldorf
print_row(4)
#facebook
print_row(5)
#twitter
print_row(6)
#instagram
print_row(7)
#gplus
print_row(8)
#podcast
print_row(9)
#itunes charts
print (row_names[10],' #',follower[10], ' (Last week #',row[10],')',sep="")

with open('social_data.csv', 'a') as f:
	data_writer = csv.writer(f)
	data_writer.writerow(follower)

