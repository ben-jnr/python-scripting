#Only works for 4anime.to
#change url accordingly, without mentioning epsiode no
url =  "https://4anime.to/gintama-season-05-episode-"

import requests
from bs4 import BeautifulSoup
from clint.textui import progress
session = requests.Session()

#use start > 0 and end > 0 and start <= end
start = int(input("start\t: "))
end = int(input("end\t: "))	

if(start > 0 and end > 0 and start <= end):	
	for i in range(start,end+1):
		no = str(i)
		if(len(no) == 1):
			final_url = url + "0" + no
		else:
			final_url = url + no
		print("\naccessing url : " + final_url)
		r = session.get(final_url)
		soup = BeautifulSoup(r.text, 'html.parser')
		source = soup.find_all('source')
		if(source != []):
			img_link = source[0].get('src')
			print("starting download - episode : " + no)
			raw_image = session.get(img_link,stream=True)
			total_length = int(raw_image.headers['Content-Length'])
			with open(no + '.mp4', 'wb') as f:
				for chunk in progress.mill(raw_image.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
					if chunk:
		    				f.write(chunk)
		    				f.flush()
		else:
			print("episode not found")
else:
	print("provide meaningful values")
