import os, platform

class Console(object):
	"""Lets you see sharp :) v2.0.3"""

	class Color(object):
		"""Colors for console"""

		@staticmethod
		def RESET(): 
			if platform.system() == 'Windows':
				return "07"
			elif platform.system() == 'Linux':
				return "\033[0m"
			return
	
		class Foreground:
			"""Forground colors"""

			@staticmethod
			def BLACK(): 
				if platform.system() == 'Windows':
					return "0f"
				elif platform.system() == 'Linux':
					return "\033[30m"
				return
			@staticmethod
			def RED(): 
				if platform.system() == 'Windows':
					return "04"
				elif platform.system() == 'Linux':
					return "\033[31m"
				return
			@staticmethod
			def GREEN(): 
				if platform.system() == 'Windows':
					return "02"
				elif platform.system() == 'Linux':
					return "\033[32m"
				return
			@staticmethod
			def BLUE(): 
				if platform.system() == 'Windows':
					return "01"
				elif platform.system() == 'Linux':
					return "\033[34m"
				return
			@staticmethod
			def PURPLE(): 
				if platform.system() == 'Windows':
					return "05"
				elif platform.system() == 'Linux':
					return "\033[35m"
				return
			@staticmethod
			def CYAN(): 
				if platform.system() == 'Windows':
					return "03"
				elif platform.system() == 'Linux':
					return "\033[36m"
				return
			@staticmethod
			def YELLOW(): 
				if platform.system() == 'Windows':
					return "06"
				elif platform.system() == 'Linux':
					return "\033[93m"
				return
			@staticmethod
			def LIGHTGREY(): 
				if platform.system() == 'Windows':
					return "07"
				elif platform.system() == 'Linux':
					return "\033[37m"
				return
			@staticmethod
			def DARKGREY(): 
				if platform.system() == 'Windows':
					return "08"
				elif platform.system() == 'Linux':
					return "\033[90m"
				return
			@staticmethod
			def LIGHTRED(): 
				if platform.system() == 'Windows':
					return "0C"
				elif platform.system() == 'Linux':
					return "\033[91m"
				return
			@staticmethod
			def LIGHTGREEN(): 
				if platform.system() == 'Windows':
					return "0A"
				elif platform.system() == 'Linux':
					return "\033[92m"
				return
			@staticmethod
			def LIGHTBLUE(): 
				if platform.system() == 'Windows':
					return "09"
				elif platform.system() == 'Linux':
					return "\033[94m"
				return
			@staticmethod
			def LIGHTCYAN(): 
				if platform.system() == 'Windows':
					return "0B"
				elif platform.system() == 'Linux':
					return "\033[96m"
				return

		class Background:
			"""Backround colors"""

			@staticmethod
			def BLACK(): 
				if platform.system() == 'Windows':
					return "f0"
				elif platform.system() == 'Linux':
					return "\033[40m"
				return
			@staticmethod
			def RED(): 
				if platform.system() == 'Windows':
					return "40"
				elif platform.system() == 'Linux':
					return "\033[41m"
				return
			@staticmethod
			def GREEN(): 
				if platform.system() == 'Windows':
					return "20"
				elif platform.system() == 'Linux':
					return "\033[42m"
				return
			@staticmethod
			def BLUE(): 
				if platform.system() == 'Windows':
					return "10"
				elif platform.system() == 'Linux':
					return "\033[44m"
				return
			@staticmethod
			def PURPLE(): 
				if platform.system() == 'Windows':
					return "50"
				elif platform.system() == 'Linux':
					return "\033[45m"
				return
			@staticmethod
			def CYAN(): 
				if platform.system() == 'Windows':
					return "30"
				elif platform.system() == 'Linux':
					return "\033[46m"
				return
			@staticmethod
			def LIGHTGREY(): 
				if platform.system() == 'Windows':
					return "70"
				elif platform.system() == 'Linux':
					return "\033[47m"
				return

	@staticmethod
	def Clear():
		if platform.system() == 'Windows':
			os.system("cls")
		else:
			os.system("clear")
		return

	@staticmethod
	def Pause():
		input("Press <Enter> key to continue...")
		return

	@staticmethod
	def ResetConsole():
		if platform.system() == 'Windows':
			os.system("color " + Console.Color.RESET())
			Console.Clear()
		else:
			print(Console.Color.RESET())
			Console.Clear()
		return

	@staticmethod
	def ThrowErrorMessage(msg):
		Console.StartColor(Console.Color.Foreground.LIGHTRED())
		Console.WriteLine(">> " + msg)
		Console.Pause()
		Console.ResetConsole()
		return

	@staticmethod 
	def WriteLine(string, color=None):
		if color == None:
			print(string)
			return

		if platform.system() == 'Windows':
			os.system("color " + color)
			print(string)
			os.system("color " + Console.Color.RESET())
		else:
			print(str(color) + string + Console.Color.RESET())
		return

	@staticmethod
	def StartColor(font=None, background=None):
		if platform.system() == 'Windows':
			if background == None:
				os.system("color " + font)
			elif font == None:
				os.system("color " + background)
			else:
				os.system("color " + background[0] + font[1])
		else:
			if background == None:
				print(str(font))
			elif font == None:
				print(str(background))	
			else:
				print(str(font))
				print(str(background))	
		return

	@staticmethod
	def EndColor():
		if platform.system() == 'Windows':
			os.system("color " + Console.Color.RESET())
		else: 
			print(Console.Color.RESET())
		return

	