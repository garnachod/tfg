from annoy import AnnoyIndex

if __name__ == '__main__':
	u = AnnoyIndex(50)
	u.load('/media/dani/data/trainedVecsTBYUser/test.ann') # super fast, will just mmap the file
	print(u.get_nns_by_item(1, 50))