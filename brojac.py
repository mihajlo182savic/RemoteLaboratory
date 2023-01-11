def brln(ime):
	fp=open(ime,"r")
	linija=""
	i=0
	while 1:
		linija=fp.readline()
		i=i+1	
		if not linija:
			break
	return i
