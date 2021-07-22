import re

sen1='hi 빅스비'
sen2='bye'
det=re.compile('^hi')
print(det.match(sen1))