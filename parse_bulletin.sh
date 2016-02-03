wget http://irc.gov.ua/upload/bulletin_340_35-2015.pdf
pdftotext -x 0 -y 55 -W 1000 -H 740 bulletin_340_35-2015.pdf
cat bulletin_340_35-2015.txt | python convert.py > bulletin_340_35-2015_converted.csv
