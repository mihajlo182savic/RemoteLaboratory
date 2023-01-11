from flask import Flask,render_template,redirect,url_for,request,abort
ad = Flask(__name__)
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import time as t
import xlsxwriter
import brojac as b
import serial
i=5
P12=14
P21=15
P22=18
P11=17
P13=24
Ref=25
GPIO.setup( P12, GPIO.OUT)
GPIO.setup( P11, GPIO.OUT)
GPIO.setup( P13, GPIO.OUT)
GPIO.setup( P21, GPIO.OUT)
GPIO.setup( P22, GPIO.OUT)
GPIO.setup( Ref, GPIO.OUT)
GPIO.output(Ref,1)
workbook = xlsxwriter.Workbook('rezultati.xlsx')
worksheet=workbook.add_worksheet()
mejl = ""

	
#def cit():
#	locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3','/dev/ttyACM0']
#	for device in locations:
#		try:
#			print "Trying...",device
#			ser = serial.Serial(device, 9600)
#			break
#		except:
#			print "Failed to connect on",device
#
#	return 1
	

def mer(naziv, dev):
	j=10

	connected = False	
	device=dev

	try:
		print "Trying...",device
		ser = serial.Serial(device, 9600)
	except:
		print "Failed to connect on",device
		

		

	#ser. write('7')
	while not connected:
		serin = ser.read()
		connected = True

	## open text file to store the current   
	text_file = open(naziv, 'w+')
	## read serial data from arduino and 
	## write it to the text file 'position.txt'
	while j:
		if ser.inWaiting():
			x=ser.read()
			print(x) 
			text_file.write(x)
			if x=="\n":
		     		#text_file.seek(0)
		     		text_file.truncate()
				j=j-1
		text_file.flush()


	text_file.close()
	ser.close()
	return 1

#def nadji(fpp):
#	i=0
#	s=0
#	while 1:
#		linija=fpp.readline()
#		if(linija == "?\n"):
#			s=i
#		i=i+1
#		if not linija:
#			break	
#	print s
#	fpp.seek(0)
#	return s
#def cit(f, poz):
#	f.seek(0)
#	p=False
#	k=0
#	i=0
#	linija=""
#	n=""
#	st=""
#	sn=""
#	print "pozicija"
#	print poz
#	while 1:
#			linija=f.readline()

			
#			if not linija:
#				break
#			if linija=="?\n":
#				if p==False:
#					if k==1:
#						napon1=linija
#					if k==2:
#						struja1=linija
#					if k==3:					
#						snaga1=linija
#						p=True

#				if p==True:
#					p=False
#					k=0
#					if(i==poz):
#						n=napon1
#						st=struja1
#						sn=snaga1
#						p=True
#			i=i+1
#			k=k+1
#	print n
#	print st
#	print sn
#	return n, st, sn
			
try:
	#import serial

		#workbook = xlsxwriter.Workbook('reyultati.xlsx')
		#worksheet=workbook.add_worksheet()
		#worksheet.set_column('A:A', 20)
	#connected = False

	#locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3','/dev/ttyACM0']

	#for device in locations:
	#    try:
	#      	 print "Trying...",device
	#        ser = serial.Serial(device, 9600)
	#        break
	#   except:
	#	print "Failed to connect on",device
	#while not connected:
	#    serin = ser.read()
	#    connected = True
	#@ad.route('/rey')
	#def Reyultati():
	#	if ser.inWaiting():
	#		x=ser.read()
	#		print(x) 
	#		worksheet.write(0,0,x)
	#	workbook.close()
	#	ser.close()
	#
	class Reflektor(object):
		def __init__(self):
			self.upaljena = False
	 
		def upali(self, pin):
		
			GPIO.output(pin,0)
			self.upaljena = True
	       
		def ugasi(self, pin):
		
			GPIO.output(pin,1)
			self.upaljena = False

	class Relej(object):
		def __init__(self):
			self.upaljen=False
		def Ugasi(self):
			GPIO.output(P11,1)
			GPIO.output(P12,1)
			GPIO.output(P13,1)
			GPIO.output(P21,1)
			GPIO.output(P22,1)
			t.sleep(2)
	       
	ref=Reflektor()
	rel=Relej()
	@ad.route("/")
	def main():
		#print "Sine neko ti je usao na sajt"

		return render_template('login.html')

	@ad.route("/toAdmin",methods=['POST'])
	def pocetna():
		global mejl
		mejl = request.form['ime']
		print mejl
		if len(mejl) < 10:
			return render_template('login.html')
		else:
			if mejl[len(mejl)-10:] == '@gmail.com':
				u = open("mejlovi.txt",'a')
				u.write(mejl+"\n")
				u.close()
				return render_template('index.html')
			else:
				return render_template('login.html')
	@ad.route("/vezba1")
	def v1():
		print "vezba 1"
		GPIO.output(25,0)
		rel.Ugasi()
		ref.upali(P22)
		print "Upaljen P22"
		ref.upali(P12)
		print "Upaljen P12"
		
		return render_template('prva_vezba.html')

	@ad.route("/vezba1V")
	def v1V():
		q = mer("struja.txt",'/dev/ttyACM1') 
		print "vezba 1V"
		rel.Ugasi()
		ref.upali(P21)
		print "Upaljen P21"
		ref.upali(P12)
		print "Upaljen P12"
		#f=open("Merenje.txt", 'r')
	#	content=f.read()
		#print(content)
		#f.closed
		return render_template('prva_vezbaV.html')#content=content)

	@ad.route("/vezba2")
	def v2():
		print "vezba 2"
		rel.Ugasi()
		ref.upali(P22)
		print "Upaljen P22"
		ref.upali(P11)

		print "Upaljen P11"
		
		return render_template('druga_vezba.html')

	@ad.route("/vezba2V")
	def v2V():
		q = mer("struja.txt",'/dev/ttyACM1') 
		print "vezba 2V"
		rel.Ugasi()
		ref.upali(P21)
		print "Upaljen P21"
		ref.upali(P11)

		print "Upaljen P11"
		return render_template('druga_vezbaV.html')

	@ad.route("/vezba3")
	def v3():
		print "vezba 3"
		rel.Ugasi()
		ref.upali(P22)
		print "Upaljen P22"
		ref.upali(P13)
		print "Upaljen P13"
		ref.upali(P12)

		print "Upaljen P12"
		return render_template('treca_vezba.html')

	@ad.route("/vezba3V")
	def v3V():
		q = mer("struja.txt",'/dev/ttyACM1') 
		print "vezba 3V"
		rel.Ugasi()
		ref.upali(P21)
		print "Upaljen P21"
		ref.upali(P12)
		print "Upaljen P12"
		ref.upali(P13)
		print "Upaljen P13"
		return render_template('treca_vezbaV.html')

	@ad.route("/nazad1")
	def nazad1():
		global worksheet
		q = mer("napon.txt",'/dev/ttyACM0') 

		f=open("struja.txt", "r")
		print "rezultati\n"
		#rel.Ugasi()
		d=open("text.txt",'w+')


		i=0
		napon="0.00"
		struja="0.00"
		snaga="snaga"
	

		fp=open("napon.txt", "r")
		f.seek(0)
		n=(b.brln("struja.txt"))-4
		m=(b.brln("napon.txt"))-4


		while 1:
			linija=f.readline()
			print linija
			if not linija:
				break
			print len(linija)-3
			if (i<n-1):	
	#			if(linija[len(linija)-3]=='V'):
	#				napon=linija
				if(linija[len(linija)-3]=='A'):
					struja=linija
				#if(linija[len(linija)-3]=='W'):
				#	snaga=linija
			i=i+1
		i=0
		while 1:
			linija=fp.readline()
			print linija
			if not linija:
				break
			print linija[len(linija)-3]
			if (i<m-1):
				print linija[len(linija)-3]	
				if(linija[len(linija)-3]=='V'):
					napon=linija
			#	if(linija[len(linija)-3]=='A'):
			#		struja=linija
				#if(linija[len(linija)-3]=='W'):
				#	snaga=linija
			i=i+1

		snaga=str(round((float(napon[:len(napon)-5])*float(struja[:len(struja)-6])),3))+" mW"
		f.close()
		fp.close()
		d.write(napon+""+struja+""+snaga+"\n")
		d.close()
		worksheet.write(0,0,"Broj merenja")
		worksheet.write(0,1,"Napon (V)")
		worksheet.write(0,2,"Struja (mA)")
		worksheet.write(0,3,"Snaga (mW)")
		worksheet.write(1,0,"1.")
		worksheet.write(1,1,napon[:-3])
		worksheet.write(1,2,struja[:-4])
		worksheet.write(1,3,snaga[:-2]+"")
	
		rel.Ugasi()

		return render_template('results.html', napon=napon, struja=struja, snaga=snaga)
		
	#-----------------------------------------------------------------------------

	@ad.route("/nazad2")
	def nazad2():
		global worksheet
		q = mer("napon.txt",'/dev/ttyACM0') 

		f=open("struja.txt", "r")
		print "rezultati\n"
		#rel.Ugasi()
		d=open("text.txt",'a')


		i=0
		napon="0.00"
		struja="0.00"
		snaga="snaga"
	

		fp=open("napon.txt", "r")
		f.seek(0)
		n=(b.brln("struja.txt"))-4
		m=(b.brln("napon.txt"))-4


		while 1:
			linija=f.readline()
			print linija
			if not linija:
				break
			print len(linija)-3
			if (i<n-1):	
	#			if(linija[len(linija)-3]=='V'):
	#				napon=linija
				if(linija[len(linija)-3]=='A'):
					struja=linija
				#if(linija[len(linija)-3]=='W'):
				#	snaga=linija
			i=i+1
		i=0
		while 1:
			linija=fp.readline()
			print linija
			if not linija:
				break
			print linija[len(linija)-3]
			if (i<m-1):
				print linija[len(linija)-3]	
				if(linija[len(linija)-3]=='V'):
					napon=linija
			#	if(linija[len(linija)-3]=='A'):
			#		struja=linija
				#if(linija[len(linija)-3]=='W'):
				#	snaga=linija
			i=i+1

		snaga=str(round((float(napon[:len(napon)-5])*float(struja[:len(struja)-6])),3))+" mW"
		f.close()
		fp.close()
		d.write(napon+""+struja+""+snaga+"\n")
		d.close()
		worksheet.write(2,0,"2.")
		worksheet.write(2,1,napon[:-3])
		worksheet.write(2,2,struja[:-4])
		worksheet.write(2,3,snaga[:-2])


		rel.Ugasi()	
	
		return render_template('results1.html', napon=napon, struja=struja, snaga=snaga)

	#-----------------------------------------------------------------------------

	@ad.route("/nazad3")
	def nazad3():
		global worksheet, workbook
		q = mer("napon.txt",'/dev/ttyACM0') 
		f=open("struja.txt", "r")
		print "rezultati\n"
		#rel.Ugasi()
		d=open("text.txt",'a')


		i=0
		napon="0.00"
		struja="0.00"
		snaga="snaga"
	

		fp=open("napon.txt", "r")
		f.seek(0)
		n=(b.brln("struja.txt"))-4
		m=(b.brln("napon.txt"))-4


		while 1:
			linija=f.readline()
			print linija
			if not linija:
				break
			print len(linija)-3
			if (i<n-1):	
	#			if(linija[len(linija)-3]=='V'):
	#				napon=linija
				if(linija[len(linija)-3]=='A'):
					struja=linija
				#if(linija[len(linija)-3]=='W'):
				#	snaga=linija
			i=i+1
		i=0
		while 1:
			linija=fp.readline()
			print linija
			if not linija:
				break
			print linija[len(linija)-3]
			if (i<m-1):
				print linija[len(linija)-3]	
				if(linija[len(linija)-3]=='V'):
					napon=linija
			#	if(linija[len(linija)-3]=='A'):
			#		struja=linija
				#if(linija[len(linija)-3]=='W'):
				#	snaga=linija
			i=i+1

		snaga=str(round((float(napon[:len(napon)-5])*float(struja[:len(struja)-6])),3))+" mW"
		f.close()
		fp.close()
		d.write(napon+""+struja+""+snaga+"\n")
		d.close()
		worksheet.write(3,0,"3.")
		worksheet.write(3,1,napon[:-3])
		worksheet.write(3,2,struja[:-4])
		worksheet.write(3,3,snaga[:-2])
	


		rel.Ugasi()
			
		return render_template('results2.html', napon=napon, struja=struja, snaga=snaga)

	#-------------------------------------------------------------------------------------------

	@ad.route("/nazad")
	def nazad():
		print "rezultati\n"
		rel.Ugasi()
		fp=open("text.txt", 'r')
		napon=fp.readline()
		print ("napon="+napon)
		struja=fp.readline()
		snaga=fp.readline()
		napon1=fp.readline()
		struja1=fp.readline()
		snaga1=fp.readline()
		napon2=fp.readline()
		struja2=fp.readline()
		snaga2=fp.readline()
		workbook.close()
		fp.close()

		rel.Ugasi()
	
		return render_template('results3.html', napon=napon, struja=struja, snaga=snaga, napon1=napon1, struja1=struja1, snaga1=snaga1, napon2=napon2, struja2=struja2, snaga2=snaga2)

	#-----------------------------------------------------------------------------------------------
	@ad.route("/sending")
	def send():
		global mejl
		import smtplib
		from email.mime.text import MIMEText
		from email.mime.multipart import MIMEMultipart
		from email.mime.base import MIMEBase
		from email import encoders

		email_user = 'pilab.etspupin@gmail.com'
		email_password = '0pi2lab1ets'
		email_send = mejl

		subject = 'Rezultati'

		msg = MIMEMultipart()
		msg['From'] = email_user
		msg['To'] = email_send
		msg['Subject'] = subject
		
		GPIO.output(25,1)
		body = 'Rezultati merenja sa solarnim panelima'
		msg.attach(MIMEText(body,'plain'))

		filename='/home/pi/Desktop/SolarniKofer/rezultati.xlsx'
		attachment  = open(filename,'rb')

		part = MIMEBase('application','octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition',"attachment; filename= "+filename)

		msg.attach(part)
		text = msg.as_string()
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.starttls()
		server.login(email_user,email_password)


		server.sendmail(email_user,email_send,text)
		attachment.close()	
		server.quit()
	
		return render_template('login.html')
	

	if __name__ == '__main__':
		ad.run( host='0.0.0.0' , port=1000 , debug=True, threaded=True)


except KeyboardInterrupt:
	workbook.close()


