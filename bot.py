#!python3
# -*- coding: utf-8 -*-

import urllib.request,ssl,smtplib
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

__author__ = "Rodrigo F Lopes, Danilo Moschem | Globalsys Soluções em TI"
__version__ = "1.0.0"
__email__ = "rodrigo.lopes@globalsys.com.br, danilo.moschem@globalsys.com.br"


## FUNCAO PARA FORMATAR XML ##
def formating(xml):
	amarelo = "<status>Aviso </status>"
	vermelho = "<status>Para baixo </status>"
	azul = "<status>Pausado (pausado)</status>"
	vermelhoClaro = "<status>Para baixo (confirmado) </status>"
	xml_final = ""
	cont = 0
	form = xml[3:-1]

	for lines in form:
		if  amarelo in lines or vermelho in lines or azul in lines or vermelhoClaro in lines:
			res = form[cont-3:cont+5]
			for lines in res:
				if "<message>" in lines or "status_raw" in lines:
					pass
				else:
					xml_final = xml_final+"\n"+lines
		else:
			pass
		cont = cont + 1
	
	return xml_final


## FUNCAO PARA CONECTAR/BAIXAR XML DE UMA ARVORE DE SENSORES ##
def main(noc):
	tabela = urllib.request.Request("https://%s/api/table.xml?content=sensors&columns=group,device,sensor,status,message&username=prtgadmin&password=G!ob@l$2o17" % noc)
	gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	tabela_download = urllib.request.urlopen(tabela, context=gcontext)
	conv = tabela_download.read().decode('utf-8')
	
	return conv.splitlines()


## FUNCAO PARA ENVIAR EMAIL ##
def email(result):
	msg = EmailMessage()
	msg.set_content(result)

	msg = MIMEMultipart()
	msg['Subject'] = '[PRTG_BOT] Resumo de Acionadores'
	msg['From'] = "bot@globalsys.com.br"
	msg['To'] =  "dba@globalsys.com.br"
	file = open('sensores.html','rb')
	fileMsg = MIMEBase('html','html')
	fileMsg.set_payload(file.read())
	file.close()
	encoders.encode_base64(fileMsg)
	fileMsg.add_header('Content-Disposition','attachment;filename=sensores.html')
	msg.attach(fileMsg)

	s = smtplib.SMTP('smtp.globalsys.com.br', 587)
	s.login("prtg@globalsys.com.br", "Gsys@2010")
	s.send_message(msg)
	s.quit()


## FUNCAO PARA FORMATAR O EMAIL ##
def emailfor(result):
	final = "<html><header><meta charset=\"ISO-8859-1\"></header><body align = \"center\"><table border=\"1px\" bordercolor=\"#000\" >"
	cont = 0
	azul = "#00e9ff"
	branco = "#FFFFFF"
	color = ""
	for linha in result.splitlines():
		if cont%2==0:
			cor = azul
		else:
			cor = branco

		if "NOC" in linha:
			final = final + ("<tr bgcolor=#242cb7><td align = \"center\" colspan=\"5\"><b><font color='white'>%s</font></b></td></tr>" %linha)
			final = final + ("<tr bgcolor=#242cb7><td width=\"10%\"><font color='white'>Grupo</font></td><td width=\15%\"><font color='white'>Device</font></td><td width=\"12%\"><font color='white'>Sensor</font></td><td width=\"10%\"><font color='white'>Status\t</font></td><td align = \"center\" width=\"45%\"><font color='white'>Mensagem</font></td></tr>")
		elif "group" in linha:
			cont = cont + 1 
			grp0 = linha.split('>')
			grp1 = str(grp0[1]).strip()
			grp2 = grp1.split('<')
			grp3 = str(grp2[0]).strip()
			final = final + ("<tr bgcolor=%s><td>%s</td>" % (cor,grp3))
		elif "device" in linha:
			dev0 = linha.split('>')
			dev1 = str(dev0[1]).strip()
			dev2 = dev1.split('<')
			dev3 = str(dev2[0]).strip()
			final = final + ("<td>%s</td>" % dev3)
		elif "sensor" in linha:
			sen0 = linha.split('>')
			sen1 = str(sen0[1]).strip()
			sen2 = sen1.split('<')
			sen3 = str(sen2[0]).strip()
			final = final + ("<td>%s</td>" %sen3)
		elif "status" in linha:
			sta0 = linha.split('>')
			sta1 = str(sta0[1]).strip()
			sta2 = sta1.split('<')
			sta3 = str(sta2[0]).strip()

			if sta3 == "Pausado (pausado)":
					color = "#0021dd"
			elif sta3 == "Para baixo":
					color = "#dd0000"
			elif sta3 == "Aviso":
					color = "#f6ff00"
			elif sta3 == "Para baixo (confirmado)":
					color = "#e84040"
			final = final + ("<td bgcolor=%s>%s</td>" % (color,sta3))

		elif "message_raw" in linha:
			men0 = linha.split('>')
			men1 = str(men0[1]).strip()
			men2 = men1.split('<')
			men3 = str(men2[0]).strip()
			final = final + ("<td>%s</td></tr>" % men3)

	final = final + ("</table></body></html>")
	return final

## BAIXANDO XML DE TODOS OS NOCs ##
result = (" NOC 1 \n"+
          formating(main("10.10.1.26:443"))+"\n"+
          " NOC 2 \n"+
          formating(main("10.10.1.27:444"))+"\n"+
          " NOC 3 \n"+
          formating(main("10.10.1.28:446"))+"\n"+
          " NOC 4 \n"+
          formating(main("10.10.1.29:447"))+"\n"+
          " NOC 5 \n"+
          formating(main("10.10.1.30:448"))+"\n"+
          " NOC 6 \n"+
          formating(main("10.10.1.31:449"))+"\n"+
          " NOC 7 \n"+
          formating(main("10.10.1.32:450"))+"\n"+
          " NOC 8 \n"+
          formating(main("10.10.1.33:451"))+"\n")

## FORMATANDO E-MAIL EM HTML ##
text =  emailfor(result)

## ESCREVENDO HTML EM ARQUIVO ##
with open('sensores.html', 'w') as f:
   f.write(text)

## ENVIANDO E-MAIL COM HTML EM ANEXO ##
email(result)