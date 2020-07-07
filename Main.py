import sys

import os
import time
import json
from ftplib import FTP
from File import File
from ftplib import error_perm
from tempfile import TemporaryDirectory
from Aftp import Aftp

programDir = File(os.path.split(os.path.abspath(sys.argv[0]))[0])
configFile = programDir.child("config.json")

if not configFile.exists:
	o = {
		"host": "",
		"user": "",
		"passwd": "",
		"port": 0,
		"local": "",
		"remote": "",
		"time_format": "%y/%m/%d %H:%M",
		"build_info_file": "",
		"build_info_kw": "BUILD_INFO",
		"ignore_files": [
			".git",
			".gitignore",
		],
		"anykey_tip": "任意键继续.."
	}

	configFile.put(json.dumps(o, indent=4, ensure_ascii=False))

config = json.loads(configFile.content)
	
host = config["host"]
user = config["user"]
passwd = config["passwd"]
port = config["port"]

local = config["local"]
remote = config["remote"]

if len(host)==0 or len(user)==0 or len(passwd)==0 or port==0 or len(local)==0 or len(remote)==0:
	print("请完善config.json文件")
else:
	now = time.strftime(config["time_format"], time.localtime())

	with TemporaryDirectory() as td:
		srcDir = File(local).copyTo(td)

		biFile = srcDir.child(config["build_info_file"])

		if config["build_info_file"] != "" and biFile.exists:
			biFile.put(biFile.content.replace(config["build_info_kw"], now))

		with Aftp(host, port, user, passwd, config["ignore_files"]) as ftp:
			ftp.upload(srcDir.path, remote)

if len(config["anykey_tip"])>0:
	input(config["anykey_tip"])