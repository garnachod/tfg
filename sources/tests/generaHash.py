import hashlib

if __name__ == '__main__':
	nombre = raw_input('dato a generar el sha-256: ')
   	h = hashlib.new('sha256')
   	h.update(nombre)
   	print h.hexdigest()