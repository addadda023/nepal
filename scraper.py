from bs4 import BeautifulSoup
import urllib2
import os, csv
import re

# This functions returns a coordinate in degrees from deg-min-sec
def coordinate(a):
	x = len(a)
	if x == 3:
		return a[0]+(a[1]+a[2]/60.0)/60.0
	elif x == 2:
		return a[0]+a[1]/60.0
	elif x == 1:
		return a[0]

#list_of_dist = "Achham District","Arghakhanchi District"

# list of districts
list_of_dist = "Achham District","Arghakhanchi District","Baglung District","Baitadi District","Bajhang District","Bajura District","Banke District","Bara District","Bardiya District","Bhaktapur District","Bhojpur District, Nepal","Chitwan District","Dadeldhura District","Dailekh District","Dang Deukhuri District","Darchula District","Dhading District","Dhankuta District","Dhanusa District","Dolakha District","Dolpa District","Doti District","Gorkha District","Gulmi District","Humla District","Ilam District","Jajarkot District","Jhapa District","Jumla District","Kailali District","Kalikot District","Kanchanpur District","Kapilvastu District","Kaski District","Kathmandu District","Kavrepalanchok District","Khotang District","Lalitpur District, Nepal","Lamjung District","Mahottari District","Makwanpur District","Manang District, Nepal","Morang District","Mugu District","Mustang District","Myagdi District","Nawalparasi District","Nuwakot District","Okhaldhunga District","Palpa District","Panchthar District","Parbat District","Parsa District","Pyuthan District","Ramechhap District","Rasuwa District","Rautahat District","Rolpa District","Rukum District","Rupandehi District","Salyan District,  Nepal","Sankhuwasabha District","Saptari District","Sarlahi District","Sindhuli District","Sindhupalchowk District","Siraha District","Solukhumbu District","Sunsari District","Surkhet District","Tanahun District","Taplejung District","Terhathum District","Udayapur District"

os.chdir("path/to/your/folder/")

with open("nepal_lat_long.csv", "wb") as toWrite:
	writer = csv.writer(toWrite, delimiter=",")
	writer.writerow(["District", "Latitude", "Longitude"])
	
	for district in list_of_dist:
		district1 = district.replace(" ","_")
		link = "https://en.wikipedia.org/wiki/" + district1
		print link
		request = urllib2.Request(link)
		
		# Response has UTF-8 charset header,
		# and HTML body which is UTF-8 encoded
		request.add_header('Accept-Encoding','utf-8')
		response = urllib2.urlopen(request)
		
		# Parse with BeautifulSoup
		soup = BeautifulSoup(response,"html.parser")
		# Get latitude and longitude
		lat = soup.find_all("span",class_="latitude")
		lon = soup.find_all("span",class_="longitude")
		
		# Get text from lat and lon
		# This text has unicode codes (for degree, min and second symbol)
		lat_dist = lat[0].get_text()
		lon_dist = lon[0].get_text()
		
		# Remove the unicode symbols
		# The string is still type unicode
		# The output is a list
		lat_process = re.sub(r'[^\x00-\x7F]+',' ', lat_dist)
		latitude = [int(s) for s in lat_process.split() if s.isdigit()]
		lon_process = re.sub(r'[^\x00-\x7F]+',' ', lon_dist)
		longitude = [int(s) for s in lon_process.split() if s.isdigit()]
		
		# Write the District, Latitude and Longitude in the file
		writer.writerow([district,coordinate(latitude),coordinate(longitude)])
		