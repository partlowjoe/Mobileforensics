# iPhone/iPad Reversing and Forensics Framework (iRFF) 1.0
# Joe Partlow
#
#
# <Legal shite>
# Author assumes no responsiblity for (mis)use of this program. irff is intended
# for use on a device you are permitted to analyze and does not have 
# forensically sound controls in place (yet) to be compliant for legal use.
# </Legal shite>
#
# Thanks to all the researchers that inspired this project including but not limited too: Andrew Hoog, Satish Bommisetty.
# Shout (bark) out to Mya :)
#
#
import sys,subprocess,platform,getopt,os,csv
def main(argv):
	nandfile = ""
	try:
		opts, args = getopt.getopt(argv,"hun:")
   	except getopt.GetoptError:
		print "Help and Options: iarff.py -h"
      	sys.exit(2)
   	for opt, arg in opts:
		if opt in ("-h","-help"):
			print "Upgrade Only: irff.py -u"
			print "Parse Nanddump: irff.py -n <filename>"
			print "View Menu: irff.py"
 	  		sys.exit()
		elif opt == "-u":
			upgrade()
		elif opt == "-n":
			nandfile = arg
			nandump()
		else:
			menumaster()
#################################  MAIN MENU   #############################
def menumaster():
	print ""
	print "       __"
	print "      ()'`;"
	print "      /\|`   iPhone/iPad Reversing & Forensic"
	print "     /  |    Framework (iRFF) 1.0"
	print "   (/_)_|_"
	print ""
	print "1)  Run forensics from OSX"
	print "2)  Run forensics from Linux"
	print "q)  Exit"
	print ""
	menu = raw_input("Enter your menu option: ")
	if menu == "1":
		menulist()
	elif menu == "2":
		menulist_osx()
	elif menu.lower() == "q":
		sys.exit()
	else:
		print "Invalid option, please choose again."
		menulist()
#################################  OSX MENU   #############################
def menulist_osx():
	print "1)  Mount dmg image and run strings"
	print "2)  Download/install prereqs & Sogeti tools"
	print "3)  Create Ramdisk"
	print "4)  Attempt to root phone"
	print "5)  Analyze SQLite databases"
	print "6)  Carve files from dd image"
	print "7)  Extract files from rooted device"
	print "q)  Exit"
	print ""
	menu = raw_input("Enter your menu option: ")
	if menu == "1":
		mountdmg_osx()
	elif menu == "2":
		upgrade_osx()
	elif menu == "3":
		ramdisk_osx()
	elif menu == "4":
		rooter_osx()
	elif menu == "5":
		sqlitegrab_osx()
	elif menu == "6":
		carver_osx()
	elif menu == "7":
		extracter_osx()
	elif menu.lower() == "q":
		sys.exit()
	else:
		print "Invalid option, please choose again."
		menulist_osx()
################################  OSX MENU FUNCTIONS  ######################################
def finisher_osx():
	done = raw_input("(m)ain menu or (q)uit: ")
	if done.lower() == "q":
		print "Exiting..."
		sys.exit()
	else:
		menulist_osx()
def upgrade_osx():
	print "Attempting prereq downloads and installation..."
	subprocess.call("tar xzvf sleuthkit-3.2.2.tar.gz, cd sleuthkit-3.2.2/, ./configure, make, make install, cd ..") 
	subprocess.call("curl -O http://networkpx.googlecode.com/files/ldid, chmod +x ldid, sudo mv ldid /usr/bin/"
	subprocess.call("curl -O -L https://github.com/downloads/osxfuse/osxfuse/OSXFUSE-2.3.4.dmg, hdiutil mount OSXFUSE-2.3.4.dmg"
	subprocess.call("sudo installer -pkg /Volumes/FUSE\ for\ OS\ X/Install\ OSXFUSE\ 2.3.pkg -target / hdiutil eject /Volumes/FUSE\ for\ OS\ X/"
	subprocess.call("sudo ARCHFLAGS='-arch i386 -arch x86_64' easy_install pycrypto, sudo easy_install M2crypto construct progressbar") 
	subprocess.call("hg clone https://code.google.com/p/iphone-dataprotection/, cd iphone-dataprotection, make -C img3fs/") 
	subprocess.call("curl -O -L https://sites.google.com/a/iphone-dev.com/files/home/redsn0w_mac_0.9.9b8.zip unzip redsn0w_mac_0.9.9b5.zip
	subprocess.call("cp redsn0w_mac_0.9.9b5/redsn0w.app/Contents/MacOS/Keys.plist .") 
	print "Finished Upgrade/installation."
	finisher_osx()
def mountdmg_osx():
	dmgfile = raw_input("Enter the dmg file name: ")
	subprocess.call("mmls $dmgfile") 
	startoffset = raw_input("Enter the offset above: ")
	print "Mounting dmg image..."
	offset = startoffset * 512 
	subprocess.call("mkdir -p ~/mnt/hfs") 
	subprocess.call("mount -t hfsplus -o ro,loop,offset=$offset $dmgfile ~/mnt/hfs/") 
	print "Getting filelist..."
	subprocess.call("fls -z CST6CDT-s 0 -m '/' -f hfs -r -i raw $dmgfile > /dmgfilelist/timeline.body")
	subprocess.call("mactime -b /dmgfilelist/timeline.body -z CST6CDT -d > /dmgfilelist/timeline.csv")
	print "Getting strings..."
	subprocess.call("strings $dmgfile > /dmgfilelist/strings.txt")
	subprocess.call("strings -e b $dmgfile > /dmgfilelist/strings_uni.txt")
	print "Analysis completed, reults in /dmgfilelist"
	finisher_osx()
def sqlitegrab_osx():
	sqldb = raw_input("Enter the database name: ")
	print "Analyzing SQLite database..."
	subprocess.call("strings --all --radix=x $sqldb > /sqlfiles/strings.txt")
	#put in sqlite3 commands to dump tables etc
	print "Database analysis finished, results in /sqlfiles." 	
	finisher_osx()
def ramdisk_osx():
	ipsw = raw_input("Enter the IPSW for your device: ")
	print "Creating Ramdisk ..."
	subprocess.call("python python_scripts/kernel_patcher.py $ipsw")
	subprocess.call("sh ./make_ramdisk_n88ap.sh")
	print "Ramdisk created."
	finisher_osx()
def carver_osx():
	dmgcarvfile = raw_input("Enter the dmg file name: ")
	print "Carving files from dd file..."
	subprocess.call("scalpel -c scalpel-iphone.conf $dmgcarvfile -o /dmgcarved")
	print "Files carved, results in /dmgcarved."
	finisher_osx()
def extracter_osx()
	subprocess.call("ssh -p 2222 root@localhost")
	print "Attempting to bruteforce key and extract contents..."
	subprocess.call("python python_scripts/demo_bruteforce.py")
	udid = raw_input("Enter the UDID: ")
	volid = raw_input("Enter the Volume ID: ")
	subprocess.call("python python_scripts/keychain_tool.py -d $udid/keychain-2.db $udid/$volid.plist")
	print "Dumping file system and decrypting and mounting file as dmg..."
	subprocess.call("./dump_data_partition.sh")
	subprocess.call("python python_scripts/emf_decrypter.py $udid/crackedFS.dmg")
	subprocess.call("Hdituil mount $udid/crackedFS.dmg")
	print "Recovering deleted files..."
	subprocess.call("python python_scripts/emf_undelete.py $udid/crackedFS.dmg")
	print "Finished recovering files."
	finisher_osx()
def rooter_osx():
	print "WARNING! This option will attempt to root the device!"
	root_dev = raw_input("Continue? (y/n): ")
	if root_dev.lower() == "y" or root_dev.lower() == "yes":
		print "1)  redsn0w"
		print "q)  Exit"
		print ""
		menu = raw_input("Enter the root method: ")
		if menu == "1":
			ipsw = raw_input("Enter the IPSW for your device: ")
			subprocess.call("./redsn0w_mac_0.9.9b5/redsn0w.app/Contents/MacOS/redsn0w -i $ipsw -r myramdisk.dmg -k kernelcache.release.n88.patched")
			print "Root complete, attempting connection..."
			subprocess.call("python usbmuxd-python-client/tcprelay.py -t 22:2222 1999:1999")
			print "Device rooted and listening on ssh:2222 root@localhost..."
			finisher_osx()
		elif menu.lower() == "q":
			finisher_osx()
		else:
			print "Invalid option, please choose again."
			rooter_osx()
	else:
		print "Rooting aborted, exiting..."
		finisher_osx()
#################################  LINUX MENU   #############################
def menulist():
	print "1)  Mount dmg image and run strings"
	print "2)  Download/install dependancies"
	print "3)  Carve files from dd image"
	print "5)  Analyze SQLite databases"
	print "q)  Exit"
	print ""
	menu = raw_input("Enter your menu option: ")
	if menu == "1":
		mountdmg()
	elif menu == "2":
		upgrade()
	elif menu == "3":
		carver()
	elif menu == "5":
		sqlitegrab()
	elif menu.lower() == "q":
		sys.exit()
	else:
		print "Invalid option, please choose again."
		menulist()
################################  LINUX MENU FUNCTIONS  ######################################
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
		subprocess.call("apt-get update, apt-get install strings scalpel ncurses-hexedit sqlite3") 
	elif "Red" in platform.linux_distribution() or "Cent" in platform.linux_distribution() or "Fedora" in platform.linux_distribution():
		subprocess.call("yum install strings scalpel ncurses-hexedit sqlite3") 
	else:
		print "Unable to determine package manager, exiting..."
		print "Please install the following programs for your distro: strings,scalpel,ncurses-hexedit,sqlite3"
	subprocess.call("wget http://joesserver/scalpel-iphone.conf"
	subprocess.call("wget http://joesserver/sleuthkit.tar.gz"
	subprocess.call("tar xzvf sleuthkit-3.2.2.tar.gz, cd sleuthkit-3.2.2/, ./configure, make, make install, cd ..") 
	print "Finished Upgrade/installation."
	finisher()
def mountdmg():
	dmgfile = raw_input("Enter the dmg file name: ")
	subprocess.call("mmls $dmgfile") 
	startoffset = raw_input("Enter the offset above: ")
	print "Mounting dmg image..."
	offset = startoffset * 512 
	subprocess.call("mkdir -p ~/mnt/hfs") 
	subprocess.call("mount -t hfsplus -o ro,loop,offset=$offset $dmgfile ~/mnt/hfs/") 
	print "Getting filelist..."
	subprocess.call("fls -z CST6CDT-s 0 -m '/' -f hfs -r -i raw $dmgfile > /dmgfilelist/timeline.body")
	subprocess.call("mactime -b /dmgfilelist/timeline.body -z CST6CDT -d > /dmgfilelist/timeline.csv")
	print "Getting strings..."
	subprocess.call("strings $dmgfile > /dmgfilelist/strings.txt")
	subprocess.call("strings -e b $dmgfile > /dmgfilelist/strings_uni.txt")
	print "Analysis completed, reults in /dmgfilelist"
	finisher()
def sqlitegrab():
	sqldb = raw_input("Enter the database name: ")
	print "Analyzing SQLite database..."
	subprocess.call("strings --all --radix=x $sqldb > /sqlfiles/strings.txt")
	#put in sqlite3 commands to dump tables etc
	print "Database analysis finished, results in /sqlfiles." 	
	finisher()
def carver():
	dmgcarvfile = raw_input("Enter the dmg file name: ")
	print "Carving files from dd file..."
	subprocess.call("scalpel -c scalpel-iphone.conf $dmgcarvfile -o /dmgcarved")
	print "Files carved, results in /dmgcarved."
	finisher()
###############################   START PROGRAM  #######################################
#  Poor attempt to provide command line option as well as menu :(
#if __name__ == "__main__":
#   main(sys.argv[2:])
menumaster()
