import argparse
import requests

from urllib.request import urlopen
from PIL import Image

api_root = 'http://ws.audioscrobbler.com/2.0/'
img_missing = 'https://lastfm-img2.akamaized.net/i/u/174s/c6f59c1e5e7240a4c0d427abd71f3dbb'
thumb_size = 174

def get_urls(data):
	imgs = []
		
	for d in data:
		imgs.append(next(filter(lambda k: k['size'] == 'large', d['image'])))
	
	return list(map(lambda k: k['#text'], imgs))

def get_imgs_from_urls(data):
	imgs = []
	
	for url in data:
		uri = url
			
		if not uri:
			uri = img_missing
			
		with urlopen(uri) as f:
			img = Image.open(f)
			imgs.append(img)
	
	return imgs

def make_collage(key, username, period, size):
	params = {
		'user' : username,
		'method' : 'user.gettopalbums',
		'period' : period,
		'limit' : size[0]*size[1],
		'api_key' : key,
		'format' : 'json',
	}
	
	topAlbums = requests.get(api_root, params).json()
	
	if 'error' in topAlbums:
		print(topAlbums['message'])
		exit()
	
	topAlbums = topAlbums['topalbums']['album']
	
	if len(topAlbums) < size[0]*size[1]:
		print("Not enough scrobbles (expected %d, got %d). Try another period or size." % (size[0]*size[1], len(topAlbums)))
		exit()
	
	imgs = get_imgs_from_urls(get_urls(topAlbums))
	
	collage = Image.new('RGB', (thumb_size * size[1], thumb_size * size[0]))
	
	for i in range(size[0]):
		for j in range(size[1]):
			collage.paste(imgs[i*size[1] + j], (thumb_size * j, thumb_size * i))
		
	collage.save("collage_%s_%s_%dx%d.jpg" % (username, period, size[0], size[1]), "jpeg")

def validate_size(s):
	dim = s.split('x')
	
	if len(dim) != 2:
		raise argparse.ArgumentTypeError("Not a valid size format")
	
	try:
		r, c = int(dim[0]), int(dim[1])
	except ValueError:
		raise argparse.ArgumentTypeError("Not a valid size format")
	
	return [r, c]

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('-u', '--username', 
		help="LastFM username", 
		required=True)
	
	parser.add_argument('-k', '--key',
		help="LastFM api key",
		required=True)
		
	parser.add_argument('-p', '--period', 
		help="Scrobbling period", 
		choices=['7day', '1month', '3month', '6month', '12month', 'overall'],
		default='7day')
		
	parser.add_argument('-s', '--size', 
		help="Collage dimensions - format ROWSxCOLUMNS (3x3, 4x5, 2x7, etc)",
		type=validate_size,
		default=[3, 3],
		metavar="ROWSxCOLUMNS")
		
	args = parser.parse_args()
	
	make_collage(args.key, args.username, args.period, args.size)
