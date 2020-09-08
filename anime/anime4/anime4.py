#Only works for 4anime.to

import requests
from bs4 import BeautifulSoup
from clint.textui import progress
import sys
session = requests.Session()

if(len(sys.argv) == 4):
	url = sys.argv[1]
	#use start > 0 and end > 0 and start <= end
	start = int(sys.argv[2])
	end = int(sys.argv[3])	
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
				    	for c in progress.mill(raw_image.iter_content(chunk_size=1024),expected_size=(total_length/1024) +1):
				    		if c:
				    			f.write(c)
				    			f.flush()
			else:
				print("episode not found")
		print("\nfinished\n")
	else:
		print("\nprovide meaningful values\n")
elif(len(sys.argv) < 4 ):
	print("\nprovide 3 arguments, use command")
	print("python3 anime4.py url starting-ep ending-ep\n")
else:
	print("\nonly 3 arguments allowed, use command")
	print("python3 anime4.py url starting-ep ending-ep\n")
