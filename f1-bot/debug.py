import os, platform
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
	def Log(src, msg, color = Fore.LIGHTWHITE_EX):
		print(color + "> " + src + ": " + msg)
		return

	@staticmethod
	def Warning(src, msg, color = Fore.LIGHTYELLOW_EX):
		print(color + "> " + src + ": " + msg)
		return

	@staticmethod
	def Error(src, msg, color = Fore.LIGHTRED_EX):
		print(color + "> " + src + ": " + msg)
		return

	@staticmethod
	def Print(msg, color = Fore.LIGHTWHITE_EX):
		print(color + msg)
		return