@echo off


:start
cls

set python_ver=36

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install pyscreenshot
pip install sounddevice
pip install pynput
pip install smtplib
pip install wave
pip install Pillow
pip install scipy

pause
exit