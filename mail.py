import smtplib
from account import*
from email.message import EmailMessage
from random import*
from imap_tools import MailBox


#메일 보내기
participates=['최유태', '정현진', '김진석', '이권행', '이경택']
#메일 보내는 틀 (smtp 라이브러리 이용 기본 틀)
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email_address, email_password)
    
    for participate in participates:
        msg=EmailMessage()
        msg["Subject"]='용선생의  롤특강 신청합니다.'
        msg['from']=email_address
        msg["To"]= 'ccyjun123@gmail.com'
        msg.set_content(participate+str(randint(1000,10000)))
        with open("캡처.png", "rb") as f:
            msg.add_attachment(f.read(), maintype='image', subtype='png')
        smtp.send_message(msg)


#메일 수신하기
mailbox= MailBox('imap.gmail.com', 993)
mailbox.login(email_address, email_password, initial_folder='INBOX')
par_lst=[]
for msg in mailbox.fetch(limit=5, reverse=True):
    participate_address=msg.from_
    participate_name=msg.text[:3]
    par={participate_address:participate_name}
    par_lst.append(par)
sam_lst=sample(par_lst, 3)
for i in range(3):
    par_lst.remove((sam_lst[i]))
left_lst=par_lst

#선정 메일 발신
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email_address, email_password)
    
    
    for idx,sam in enumerate(sam_lst):
        msg=EmailMessage()
        msg["Subject"]='파이썬 특강 신청 합격.'
        msg['from']=email_address
        msg["To"]= list(sam.keys())[0]
        msg.set_content((list(sam.values())[0])+'님 축하염 합격. 도구라인부터 차근차근 성장하세요 (선정순번:{})'.format(idx+1))
        
        smtp.send_message(msg)

#탈락 메일 발신
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email_address, email_password)
    
    
    for idx,left in enumerate(left_lst):
        msg=EmailMessage()
        msg["Subject"]='롤특강 신청 탈락'
        msg['from']=email_address
        msg["To"]= list(left.keys())[0]
        msg.set_content((list(left.values())[0])+'님 탈락임. 너무 허졉이라 받아줄수가없음(예비순번:{})'.format(idx+1))
        
        smtp.send_message(msg)

#선정 명단 엑셀 찍기
from openpyxl import Workbook

wb=Workbook()
ws=wb.active
tit=['순번','이메일','이름']
ws.append(tit)
for i in range(len(sam_lst)):
    name=list(sam_lst[i].keys())[0]
    address=list(sam_lst[i].values())[0]
    data=[i+1, name, address]
    ws.append(data)
wb.save('선발명단.xlsx')

