# -*- coding: utf-8 -*-
import sys, os, platform
from colorama import init, Fore, Back, Style

init(autoreset=True)

class Debug(object):
	@staticmethod
	def Clear():
		if platform.system() == 'Windows':
			os.system("cls")
		else:
			os.system("clear")
		return

	@staticmethod
	def Pause():
		print(Style.RESET_ALL)
		input("Press <Enter> key to continue...")
		return

	@staticmethod
	def Exit():
		sys.exit()
		return

	@staticmethod
	def Log(src, msg):
		print(Fore.LIGHTWHITE_EX + "> " + src + ": " + str(msg))
		return

	@staticmethod
	def Warning(src, msg):
		print(Fore.LIGHTYELLOW_EX + "> " + src + ": " + str(msg))
		return

	@staticmethod
	def Error(src, msg):
		print(Fore.LIGHTRED_EX + "> " + src + ": " + str(msg))
		return

	@staticmethod
	def Print(msg, color = Fore.WHITE):
		if isinstance(msg, list):
			for m in msg:
				print(color + str(m))
		else:
			print(color + str(msg))
		return