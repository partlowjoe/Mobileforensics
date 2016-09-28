# Android Reversing and Forensics Framework (ARFF) 1.0
# Joe Partlow
#
#
# <Legal shite>
# Author assumes no responsiblity for (mis)use of this program. Arff is intended
# for use on a device you are permitted to analyze and does not have 
# forensically sound controls in place (yet) to be compliant for legal use.
# </Legal shite>
#
# Thanks to all the researchers that inspired this project including but not limited to: Andrew Hoog.
# Shout (bark) out to Mya :)
#
#
import sys,subprocess,platform,getopt,os,csv
def main(argv):
	nandfile = ""
	try:
		opts, args = getopt.getopt(argv,"hun:")
   	except getopt.GetoptError:
		print "Help and Options: arff.py -h"
      	sys.exit(2)
   	for opt, arg in opts:
		if opt in ("-h","-help"):
			print "Upgrade Only: arff.py -u"
			print "Parse Nanddump: arff.py -n <filename>"
			print "View Menu: arff.py"
 	  		sys.exit()
		elif opt == "-u":
			upgrade()
		elif opt == "-n":
			nandfile = arg
			nandump()
		else:
			menulist()
#################################  MAIN MENU   #############################
def menulist():
	print ""
	print "       __"
	print "      ()'`;"
	print "      /\|`   Android Reversing & Forensic"
	print "     /  |    Framework (ARFF) 1.0"
	print "   (/_)_|_"
	print ""
	print "1)   Verify USB connection to phone"
	print "4)   Decompile APK file"
	print "8)   Recompile APK file"
	print "2)   Parse APKs from memory dump"
	print "3)   Attempt root of device"
	print "6)   Device shell prompt"
	print "5)   Download all information from device"
	print "7)   Aquire/Process nanddump & dd files"
	print "11)  Analyze SQLite databases"
	print "9)   Download/install dependancies"
	print "10)  Image SD card"
	print "12)  Carve files from dd image"
	print "q)   Exit"
	print ""
	menu = raw_input("Enter your menu option: ")
	if menu == "1":
		checkusb()
	elif menu == "2":
		parseapk()
	elif menu == "3":
		rooter()
	elif menu == "4":
		unpackapk()
	elif menu == "8":
		makeapk()
	elif menu == "5":
		adbpull()
	elif menu == "6":
		shell()
	elif menu =="7":
		nanddump() 
	elif menu == "9":
		upgrade()
	elif menu == "10":
		imagesd()
	elif menu == "11":
		sqlitegrab()
	elif menu == "12":
		carver()
	elif menu.lower() == "q":
		sys.exit()
	else:
		print "Invalid option, please choose again."
		menulist()
################################  MENU FUNCTIONS  ######################################
def finisher():
	done = raw_input("(m)ain menu or (q)uit: ")
	if done.lower() == "q":
		print "Exiting..."
		sys.exit()
	else:
		menulist()
def upgrade():
	print "Attempting prereq downloads and installation..."
	if "Ubuntu" in platform.linux_distribution() or "Debian" in platform.linux_distribution():
		subprocess.call("apt-get update, apt-get install strings scalpel nc ncurses-hexedit sqlite3") 
	elif "Red" in platform.linux_distribution() or "Cent" in platform.linux_distribution():
		subprocess.call("yum install strings scalpel nc ncurses-hexedit sqlite3") 
	else:
		print "Unable to determine package manager, exiting..."
		print "Please install the following programs for your distro: strings,scalpel,nc,ncurses-hexedit,sqlite3"
	subprocess.call("wget http://miui.connortumbleson.com/other/apktool/apktool_1.5.0.jar")
	subprocess.call("wget http://miui.connortumbleson.com/other/apktool/aapt/linux/aapt")	
	subprocess.call("wget http://signapk.googlecode.com/files/signapk-0.3.1.tar.bz2"
	subprocess.call("wget http://joesserver/scalpel-android.conf"
	subprocess.call("mkdir -p /dc3ddsrc, cd /dc3ddsrc") 
	subprocess.call("wget http://cdnetworks-us-2.dl.sourceforge.net/project/dc3dd/dc3dd/7.0.0/dc3dd-7.0.0.tar.gz") 
	subprocess.call("tar xzf dc3dd-7.0.0.tar.gz, cd dc3dd-7.0.0/, ./configure, make, make install, cd ..") 
	print "Finished Upgrade/installation."
	finisher()
def shell():
	print "Attempting shell on device, make sure USB debugging is on or device is rooted..."
	subprocess.call("adb shell")
	finisher()
def checkusb():
	print "Checking/resetting USB connection..."
	subprocess.call("adb kill-server, adb devices, lsusb -v") 
	finisher()
def imagesd():
	subprocess.call("dmesg | grep 'sd' ") 
	capturedev = raw_input("Enter the device to capture: ")
	print "Starting Image of SD card..."
	subprocess.call("dc3dd if=$capturedev of=/dc3dd/$capturedev.dc3dd verb=on hash=sha256 hlog=/dc3dd/$capturedev.hashlog log=/dc3dd/$capturedev.log rec=off")
	Print "Imaging completed, results in /dc3dd."
	finisher()
def adbpull():
	print "Starting information pull..."
	print "Make sure USB debugging is on or device is rooted for best results."
	subprocess.call("adb pull /data adbpull")
	subprocess.call("adb pull /data/data adbpull")
	subprocess.call("adb pull /proc adbpull")
	subprocess.call("adb pull /dev adbpull")
	subprocess.call("adb pull /cache adbpull")
	subprocess.call("adb pull /app-cache adbpull")
	subprocess.call("adb pull /mnt/asec adbpull")
	subprocess.call("adb pull /mnt/sdcard adbpull")
	subprocess.call("adb pull /mnt/emmc adbpull")
	subprocess.call("adb pull /sys adbpull")
	print "Device data extracted, results in /adbpull"
	finisher()
def unpackapk():
	apk_unpack = raw_input("Enter the APK path/file name: ")
	apk_framework = raw_input("Enter the framework path/file name (ENTER if none): ")
	if len(apk_framework) < 6:
		subprocess.call("apktool if $apk_framework")
		print "Using APK framework..."
	else:
		print "Skipping APK framework..."
	print "Starting APK decompile..."
	subprocess.call("apktool d $apk_unpack /apkexpand")
	print "APK decompiled, results in /apkexpand"
	finisher()
def makeapk():
	apk_pack = raw_input("Enter the APK path/folder name: ")
	apk_name = raw_input("Enter finished APK path/file name: ")
	apk_signed = apk_name.replace(".apk","_signed.apk")
	print "Compiling APK..."
	subprocess.call("apktool b $apk_pack")
	print "Signing APK..."
	subprocess.call("java -jar signapk.jar certificate.pem key.pk8 $apk_name $apk_signed")
	print "APK compiled and signed."
	finisher()
def nanddump():
	print "Aquiring/analyzing nanddump and dd over netcat..."
	nanddump = raw_input("Enter the nanddump file name: ")
	ddfile = raw_input("Enter the dd file name: ")
	subprocess.call("adb shell mount")
	subprocess.call("cat /proc/mtd")
	mtd = raw_input("Enter the mtd name: ")
	subprocess.call("adb push tools/ /dev/tools")
	subprocess.call("adb forward tcp:31337 tcp:31337")
	subprocess.call("adb forward tcp:31338 tcp:31338")
	subprocess.call("nc 127.0.0.1 31337 > $nanddump.nanddump")
	subprocess.call("nc 127.0.0.1 31338 > dd of=$ddfile.dd bs=4096")
	subprocess.call("adb shell")
	subprocess.call("chmod 755 /dev/tools/*")
	subprocess.call("/dev/tools/nanddump /dev/mtd/mtd8ro | /dev/tools/nc -l -p 31337")
	subprocess.call("dd if=/dev/mtd/$mtd bs=4096 | /dev/tools/nc -l -p 31338")
	subprocess.call("strings --all --radix=x $ddfile.dd > /ddfiles/strings.txt")
	subprocess.call("strings --all --radix=x --encoding=b $ddfile.dd > /ddfiles/web-encode.txt")
	subprocess.call("strings --all --radix=x --encoding=1 $ddfile.dd > /ddfiles/gps-encode.txt")
	print "dd analysis finished, results in /ddfiles." 	
	subprocess.call("strings --all --radix=x $nanddump | grep maps.google.com > /nandfiles/mapinfo.txt")
	print "nanddump analysis finished, results in /nandfiles." 
	print "Removing OOB data from nanddump for file carving..."	


	print "OOB data removed from nanddump, result in <nanddump>.dd"
	finisher()
def sqlitegrab():
	sqldb = raw_input("Enter the database name: ")
	print "Analyzing SQLite database..."
	subprocess.call("strings --all --radix=x $sqldb > /sqlfiles/strings.txt")
	#put in sqlite3 commands to dump tables etc
	print "Database analysis finished, results in /sqlfiles." 	
	finisher()
def parseapk():
	print "Parsing APKs from memory dump..."
	#put in zipfinder.py code here
	print "APKs parsed, results in /apkfiles."
	finisher()
def carver():
	print "Carving files from dd file..."
	ddfile = raw_input("Enter the dd file name: ")
	subprocess.call("scalpel -c scalpel-android.conf $ddfile -o /ddcarved")
	print "Files carved, results in /ddcarved."
	finisher()
def rooter():
	print "WARNING! This option will attempt to root the device!"
	root_dev = raw_input("Continue? (y/n): ")
	if root_dev.lower() == "y" or root_dev.lower() == "yes":
		print "Attempting device root.."
		#put in 1337 hax0r stuff here!!!!!!!!!! 
		finisher()
	else:
		print "Rooting aborted, exiting..."
		finisher()
###############################   START PROGRAM  #######################################
#  Poor attempt to provide command line option as well as menu :(
#if __name__ == "__main__":
#   main(sys.argv[2:])
menulist()
