# -*- coding: utf-8 -*
# just an ugly script nothing else
import platform
import shutil
import sys
import os
from subprocess import call
from time import sleep

architecture = platform.uname().machine


def GenVersionFileForWin(version):
    return str('VSVersionInfo(\n' +
               f'ffi=FixedFileInfo(filevers=({version.replace("v", "").replace(".", ", ")}, 1), prodvers=({version.replace("v", "").replace(".", ", ")}, 0),mask=0x3f,flags=0x0,OS=0x4,fileType=0x1,subtype=0x0,date=(0, 0)),\n' +
               'kids=[\n' +
               'StringFileInfo(\n' +
               '[\n' +
               'StringTable(\n' +
               "u'040904B0',\n" +
               "[StringStruct(u'CompanyName', u''),StringStruct(u'FileDescription', u'Simple Discord bot, nothing else :)'),StringStruct(u'FileVersion', u'')," +
               "StringStruct(u'InternalName', u''),StringStruct(u'LegalCopyright', u''),StringStruct(u'OriginalFilename', u'f1_bot.py')," +
               f"StringStruct(u'ProductName', u'Discord Formula 1 ({architecture})')," +
               f"StringStruct(u'ProductVersion', u'{version.replace('v', '')}')])]),\n" +
               "VarFileInfo([VarStruct(u'Translation', [1033, 1200])])])")


def read_version():
    all = ""
    with open("f1_bot.py", 'r') as file:
        all = file.read()

    return all.split("VERSION")[1].split('"')[1]


if not os.path.exists('./temp'):
    os.mkdir("temp")

os.chdir("..")
version = read_version()

dirs = {
    "workpath": "Build/temp",
    "distpath": "Build/bin",
    "ico": "Build/icon.ico",
    "version-file": f"Build/temp/file_version_info_{architecture}({version}).txt"
}

commands = {
    "Linux": f'pyinstaller f1_bot.py -n "F1Bot" --onefile --workpath="./{dirs["workpath"]}/{platform.system()}_{architecture}" --distpath="./{dirs["distpath"]}/{platform.system()}_{architecture}"',
    "Windows": f'pyinstaller f1_bot.py -n "F1Bot" --onefile --workpath="./{dirs["workpath"]}/{platform.system()}_{architecture}" --distpath="./{dirs["distpath"]}/{platform.system()}_{architecture}" --win-private-assemblies -i "./{dirs["ico"]}" --version-file="./{dirs["version-file"]}"'
}

print("---------")
print("Platrom: " + platform.system() + " " + architecture)
print("Command: " + commands[platform.system()])
input("Press <Enter> key to continue...")

if platform.system() == "Windows":
    print("Creating version-file")
    with open(dirs["version-file"], 'w', encoding="utf-8") as out:
        out.write(GenVersionFileForWin(version))

print("Building binary...")
call(commands[platform.system()], shell=True)

print("Building binary - Done!")

os.chdir("..")

print("Copying LICENSE and README...")

shutil.copy2('LICENSE', f"./f1-bot/{dirs['distpath']}/{platform.system()}_{architecture}/")
shutil.copy2('README.md', f"./f1-bot/{dirs['distpath']}/{platform.system()}_{architecture}/")

print("Copying - Done!")
print("Creating archive...")

root_dir = os.getcwd()
if not os.path.exists(f"{root_dir}/f1-bot/Build/archive"):
    os.mkdir(f"{root_dir}/f1-bot/Build/archive")

os.chdir(f"./f1-bot/{dirs['distpath']}/{platform.system()}_{architecture}")
shutil.make_archive(f"{root_dir}/f1-bot/Build/archive/{platform.system()}_F1Bot_{version}_{architecture}", 'zip')

print("Build Done!")
sleep(1)
print("Cleaning...")

if os.path.exists(f"{root_dir}/f1-bot/Build/temp"):
    shutil.rmtree(f"{root_dir}/f1-bot/Build/temp")

if os.path.exists(f"{root_dir}/f1-bot/Core/__pycache__"):
    shutil.rmtree(f"{root_dir}/f1-bot/Core/__pycache__")

if os.path.exists(f"{root_dir}/f1-bot/__pycache__"):
    shutil.rmtree(f"{root_dir}/f1-bot/__pycache__")

if os.path.exists(f"{root_dir}/f1-bot/F1Bot.spec"):
    os.remove(f"{root_dir}/f1-bot/F1Bot.spec")

print("Cleaning Done!")
