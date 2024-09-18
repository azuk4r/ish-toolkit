cp ht.py /usr/local/bin
cp getip.py /usr/local/bin
cp paypy.py /usr/local/bin
cp fmux.py /usr/local/bin
chmod +x /usr/local/bin/ht.py
chmod +x /usr/local/bin/getip.py
chmod +x /usr/local/bin/paypy.py
chmod +x /usr/local/bin/fmux.py
mv /usr/local/bin/ht.py /usr/local/bin/ht
mv /usr/local/bin/getip.py /usr/local/bin/getip
mv /usr/local/bin/paypy.py /usr/local/bin/paypy
mv /usr/local/bin/fmux.py /usr/local/bin/fmux
mkdir /etc/assisht
apk add python3 py3-pip
pip install requests colorama datetime
echo 'successful: full ish-toolkit instaled.'
