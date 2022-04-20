@echo off
cd D:\Git\IPTV-THAI
set t=%date%_%time%
set d=%t:~10,4%-%t:~4,2%-%t:~7,2%_%t:~15,2%-%t:~18,2%-%t:~21,2%

git.exe add .

git.exe commit -am "auto commit and push on %d%"

git.exe push origin master

pause