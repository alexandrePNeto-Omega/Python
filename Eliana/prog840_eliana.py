# -*- coding: iso-8859-1 -*-
__cvsinfo__ = ''
__author__	= 'Alexandre Philippus Neto'
__exename__ = ('main', 'manutencao')
__title__   = 'Prog Eliana'
__descr__   = '''Prog responsavel por gerar o relatorio da Eliana'''

from datetime import date
from lzt.lztdatetime import *
from lzt.lztutil import *
from classe.estoque import Estoque
from classe.config import Config
from util.asfind import *
from manutencao.manut_prog import ManutProgBase

import os

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from classe.pessoa import Pessoa

from util.workspace	import ws

PAGE_HEIGHT = 293.5 * mm
PAGE_WIDTH = 209.5 * mm

class ManutProg(ManutProgBase, LztGtkApp):
	def __init__(self, ws):
		ManutProgBase.__init__(self, ws)
		self.ws = ws
		self.db = ws.db
		self.L = LinasStruct(ws)
		self.PMT = PdfMailTo(ws)
		
	# def run(self, console=True):
	# 	PMT = PdfMailTo(self.ws)
	# 	L = LinasStruct(self.ws)
	# 	file_list = []
	# 	empresa_list = L.retorno_empresas()
	# 	empresa_list_local = []

	# 	filename = tempfile.mktemp("TODAS_EMPS_rel_"+now().strftime("%d-%m-%Y_%H-%M-%S")+".pdf")
	# 	report = Canvas(filename)

	# 	pdf = PdfMakeBuild(self.ws)
	# 	pdf.do_header_pdf(report)

	# 	for empresa_dict in empresa_list:
	# 		file_list.append(self.pdf_empresa(empresa_dict))
	# 		empresa_list_local += [empresa_dict]

	# 	pdf.write_lines_pdf(empresa_list_local, report)

	# 	report.showPage()
	# 	report.save()
	# 	file_list.append(filename)
	# 	PMT.send_mail(file_list)

	# 	return True

	# def pdf_empresa(self, empresa_dict):
	# 	tempFile = tempfile.mktemp(str(empresa_dict.get('nome')) + "_rel.pdf")
	# 	report = Canvas(tempFile)
	# 	pdf = PdfMakeBuild(self.ws)
	# 	pdf.do_header_pdf(report)
	# 	pdf.write_lines_pdf([empresa_dict], report)
	# 	report.showPage()
	# 	report.save()
	# 	return tempFile

##########################################################################################################
	def run(self, console=True):
		#	Objetivo: Rodar o prog

		empresa_list_local = []
		empresa_list = self.L.retorno_empresas()
		for empresa_dict in empresa_list:
			# self.pdf_empresa(empresa_dict)
			empresa_list_local += [empresa_dict]

		#	Empresas separadas			
		report = Canvas("TODAS_AS_EMPRESA_rel.pdf")
		pdf = PdfMakeBuild(self.ws)
		pdf.do_header_pdf(report)
		pdf.write_lines_pdf(empresa_list_local, report)
		report.showPage()
		report.save()

		#	Consolidados
		report_consolidado = Canvas("TODAS_AS_EMPRESA_CONSOLIDADO_rel.pdf")
		pdf = PdfMakeBuild(self.ws)
		pdf.do_header_pdf(report_consolidado)
		pdf.wirte_lines_pdf_consolidado(empresa_list_local, report_consolidado)
		report_consolidado.showPage()
		report_consolidado.save()

		return True
	
	def pdf_empresa(self, empresa_dict):
		report = Canvas(str(empresa_dict.get('nome')) + "_rel.pdf")
		pdf = PdfMakeBuild(self.ws)
		pdf.do_header_pdf(report)
		pdf.write_lines_pdf([empresa_dict], report)
		report.showPage()
		report.save()
##########################################################################################################

class PdfMailTo:
	#	Responsábilidade:	Enviar o email para o usuário final.

	def __init__(self, ws):
		self.ws = ws
		self.db = ws.db
		self.C = Config(ws)
		self.P = Pessoa(self.ws)
		self.attach_list = []
		self.erro = ""

	def send_mail(self, arq_name_list):
		
		for arq in arq_name_list:
			self.attach_list.append((arq))

		msg_body = "Olá, segue em anexo o relatório de <strong>Faturamento \\ Volume \\ Margem</strong> consolidados<br />\
			Gerado em: " + str(now().strftime("%d/%m/%Y - %H:%M:%S")) + ", por Autosystem PRO.\
			"

		email_from_a = self.C.get_config_empresa(ws.info['empresa']['grid'], "internet_smtp_user")

		self.P.envia_email(email_from_a, "suporte9@omegaautomacao.com", "Relatório de Faturamento \\ Volume \\ Margem consolidados", msg_body, self.attach_list, msg_type=2, confirm_read=False)

class PdfMakeBuild:
	#	Responsábilidade:	Montar o PDF como um todo, criando linhas e tudo que vai aparecer no layout

	def __init__(self, ws):
		self.ws = ws
		self.db = ws.db
		self.line_y = PAGE_HEIGHT
		self.line_x = PAGE_WIDTH
		self.num_pages = 1
		self.L = LinasStruct(ws)

	def wirte_lines_pdf_consolidado(self, empresa_list, report):
		self.do_footer_pdf(report)
		
		self.draw_title_rel(report, "FATURAMENTO")
		list_fat_consolidado = []
		self.draw_words_title_column(report, 10 * mm, self.line_y, "Empresa")
		for e in empresa_list:
			result_faturamento_list = self.L.get_faturamento_consolidado(e['grid'])
			self.draw_words_by_line_column_consoli(report, [self.sub_total_empresa_dict(result_faturamento_list, e['nome'])], "R$")
			list_fat_consolidado.append(self.sub_total_empresa_dict(result_faturamento_list, e['nome']))
		self.draw_words_subtotal(report, list_fat_consolidado, "R$")

		self.draw_title_rel(report, "VOLUME")
		list_vol_consolidado = []
		self.draw_words_title_column(report, 10 * mm, self.line_y, "Empresa")
		for e in empresa_list:
			result_faturamento_list = self.L.get_volume_consolidado(e['grid'])
			self.draw_words_by_line_column_consoli(report, [self.sub_total_empresa_dict(result_faturamento_list, e['nome'])], "L")
			list_vol_consolidado.append(self.sub_total_empresa_dict(result_faturamento_list, e['nome']))
		self.draw_words_subtotal(report, list_vol_consolidado, "L")

		self.draw_title_rel(report, "MARGEM BRUTA")
		list_mg_consolidado = []
		self.draw_words_title_column(report, 10 * mm, self.line_y, "Empresa")
		for e in empresa_list:
			result_faturamento_list = self.L.get_margem_bruta_consolidado(e['grid'])
			self.draw_words_by_line_column_consoli(report, [self.sub_total_empresa_dict(result_faturamento_list, e['nome'])], "R$")
			list_mg_consolidado.append(self.sub_total_empresa_dict(result_faturamento_list, e['nome']))
		self.draw_words_subtotal(report, list_mg_consolidado, "R$")

		## -- GRUPO -- ##

		report.line(5 * mm, self.line_y, (PAGE_WIDTH  - 5 * mm), self.line_y)
		self.line_y -= 6 * mm

		fat_list_all = []
		self.draw_title_rel(report, "FATURAMENTO")
		self.draw_words_title_column(report, 10 * mm, self.line_y, "Grupo de produto")
		for e in empresa_list:
			list_con_fat = self.L.get_faturamento_consolidado(e["grid"])
			veirfica_fat = self.verifica_nome_list_com_dict("nome", list_con_fat, fat_list_all)
			if veirfica_fat is not None:
				for vv_fat in veirfica_fat:
					if vv_fat.get("nome") != "Erro":
						fat_list_all.append(
							self.L.monta_loop_dict([vv_fat.get("nome"), vv_fat.get("dia"), vv_fat.get("mes"), vv_fat.get("ano"),\
									vv_fat.get("a_dia"), vv_fat.get("a_mes"), vv_fat.get("a_ano")]))			
		self.draw_words_by_line_column_consoli(report, fat_list_all, "R$")
		self.draw_words_subtotal(report, fat_list_all, "R$")

		vol_list_all = []
		self.draw_title_rel(report, "VOLUME")
		self.draw_words_title_column(report, 10 * mm, self.line_y, "Grupo de produto")
		for e in empresa_list:
			list_con_vol = self.L.get_volume_consolidado(e["grid"])
			veirfica_vol = self.verifica_nome_list_com_dict("nome", list_con_vol, vol_list_all)
			if veirfica_vol is not None:
				for vv_vol in veirfica_vol:
					if vv_vol.get("nome") != "Erro":
						vol_list_all.append(
							self.L.monta_loop_dict([vv_vol.get("nome"), vv_vol.get("dia"), vv_vol.get("mes"), vv_vol.get("ano"),\
									vv_vol.get("a_dia"), vv_vol.get("a_mes"), vv_vol.get("a_ano")]))
		self.draw_words_by_line_column_consoli(report, vol_list_all, "L")
		self.draw_words_subtotal(report, vol_list_all, "L")

		mg_list_all = []
		self.draw_title_rel(report, "MARGEM BRUTA")
		self.draw_words_title_column(report, 10 * mm, self.line_y, "Grupo de produto")
		for e in empresa_list:
			list_con_mg = self.L.get_margem_bruta_consolidado(e["grid"])
			verifica_mg = self.verifica_nome_list_com_dict("nome", list_con_mg, mg_list_all)
			if verifica_mg is not None:
				for vv_mg in verifica_mg:
					if vv_mg.get("nome") != "Erro":
						mg_list_all.append(self.L.monta_loop_dict([vv_mg.get("nome"), vv_mg.get("dia"), vv_mg.get("mes"), vv_mg.get("ano"),\
							vv_mg.get("a_dia"), vv_mg.get("a_mes"), vv_mg.get("a_ano")]))
		self.draw_words_by_line_column_consoli(report, mg_list_all, "R$")
		self.draw_words_subtotal(report, mg_list_all, "R$")

	def write_lines_pdf(self, empresa_list, report):
		self.do_footer_pdf(report)

		for item in empresa_list:
			#	Nome da empresa que está sendo gerado o relatório
			self.draw_empresa_nome(report, (5 * mm), self.line_y, item['nome'])

			#	Relatório numº 1
			result_faturamento_list = self.L.get_faturamento_consolidado(item['grid'])
			self.draw_title_rel(report, "FATURAMENTO")
			self.draw_words_by_line_column(report, result_faturamento_list, "R$")
			self.draw_words_subtotal(report, result_faturamento_list, "R$")

			#	Relatório numº 2
			result_volume_list = self.L.get_volume_consolidado(item['grid'])
			self.draw_title_rel(report, "VOLUME")
			self.draw_words_by_line_column(report, result_volume_list, "L")
			self.draw_words_subtotal(report, result_volume_list, "L")

			#	Relatório numº 3
			result_volume_list = self.L.get_margem_bruta_consolidado(item['grid'])
			self.draw_title_rel(report, "MARGEM BRUTA")
			self.draw_words_by_line_column(report, result_volume_list, "R$")
			self.draw_words_subtotal(report, result_volume_list, "R$")

			#	Espaçamento para a próxima empresa
			self.line_y -= 5
	
	#	Util

	def verifica_more_page(self, report):
		if self.line_y < 15 * mm:
			report.showPage()
			self.line_y = (PAGE_HEIGHT - 5 * mm)
			self.do_footer_pdf(report)
			self.num_pages += 1

	def sub_rel_consolidado(self, report, result_dict):

		return 0.0

	def sub_total_empresa_dict(self, result_list, empresa_nome):
		sum_ano = 0.0
		sum_mes = 0.0
		sum_dia = 0.0
		sum_ano_a = 0.0
		sum_mes_a = 0.0
		sum_dia_a = 0.0

		for result_dict in result_list:
			sum_ano += self.L.convert_float(result_dict.get('ano'))
			sum_mes += self.L.convert_float(result_dict.get('mes'))
			sum_dia += self.L.convert_float(result_dict.get('dia'))
			sum_ano_a += self.L.convert_float(result_dict.get('a_ano'))
			sum_mes_a += self.L.convert_float(result_dict.get('a_mes'))
			sum_dia_a += self.L.convert_float(result_dict.get('a_dia'))

		return self.L.monta_loop_dict([empresa_nome, sum_dia, sum_mes, sum_ano,\
								sum_dia_a, sum_mes_a, sum_ano_a])

	def verifica_nome_list_com_dict(self, param, list_con_fat, fat_list_all):
		list_of_names = []
		for i, list_one in enumerate(list_con_fat):
			if list_one.get(str(param)) not in fat_list_all:
				list_of_names.append(list_con_fat[i])

		if not list_of_names:
			return []
		return list_of_names

	#	Draws auxiliares

	def do_header_pdf(self, report):
		#	Objetivo:	Criar o cabeçalho para o PDF
		#	Parâmetros:	O PDF do gerando
		#	Retorno:

		report.setFont("Helvetica", 8)
		#	Data
		report.drawString((PAGE_WIDTH  - 34.5 * mm), (self.line_y - 1.5 * mm), now().strftime("%d/%m/%Y as %H:%M:%S"))

		#	Empresa
		nome_empresa = ws.info['empresa']['nome']
		report.drawString(((PAGE_WIDTH - PAGE_WIDTH)  + 5 * mm), (self.line_y - 1.5 * mm), nome_empresa)

		#	Título
		title_rel = "REL. TESTE P/ ELIANA TITULO"
		report.setFont("Helvetica-Bold", 15)
		report.drawCentredString(305, (self.line_y - 11.5 * mm), title_rel)

		#	Linha
		report.setFont("Courier", 10)
		report.line(5 * mm, (self.line_y - 4.5 * mm), (PAGE_WIDTH  - 5 * mm), (self.line_y - 4.5 * mm))

		#	Tamanho do header
		self.line_y -= 18.5 * mm

	def do_footer_pdf(self, report):
		#	Objetivo:	Criar o rodapé da página para cada que passar
		#	Parâmetros: report => pdf, page => número da página ao qual se econtra
		#	Retorno:

		#	Linha
		report.setFont("Courier", 10)
		report.line(5 * mm, 8 * mm, (PAGE_WIDTH  - 5 * mm), 8 * mm)
		
		report.setFont("Helvetica", 8)
		#	Nº da pag
		string_footer = "Pag. " + str(self.num_pages)
		report.drawString((PAGE_WIDTH  - 15 * mm), 3.4 * mm, string_footer)

		#	Mensagem do footer
		msg_footer = "Relatorio gerado por Autosystem PRO."
		report.drawString((5 * mm), 3.4 * mm, msg_footer)
		
		self.num_pages += int(1)

	def draw_empresa_nome(self, report, y, x, empresa_nome):
		#	Objetivo:	Escrever o nome para o titulo do relatórios
		#	Parâmetros:	report => pdf gerado, x-y => posição, empresa_nome => nome da empresa
		
		self.verifica_more_page(report)
		report.setFont("Helvetica-Bold", 10)
		report.drawString(y, x, empresa_nome)
		self.line_y -= 4 * mm

	def draw_title_rel(self, report, title):
		#	Objetivo:	Escrever titulo de cada subrelatório
		#	Parâmetros:	report => pdf gerado, x-y => posição, titulo => titulo do subrel
		#	Retorno:	O esoaço que ele ocupa

		self.verifica_more_page(report)
		self.draw_title_rel_acumulado(report, (142 * mm), self.line_y,  title)
		report.setFont("Helvetica-Bold", 7)
		report.drawString((10 * mm), self.line_y + 0.3 * mm, title)
		self.line_y -= 5 * mm

	def draw_title_rel_acumulado(self, report, x, y, title):
		report.setFont("Helvetica-Bold", 7)
		report.drawString((x + 0.5 * mm), y + 0.3 * mm, str(title + " ACUMULADO"))

	def draw_words_title_column(self, report, x, y, nome):
		#	Objetivo:	Escrever titulo de cada coluna na tabela
		#	Parâmetros:	report => pdf gerado, x-y => eixos

		self.verifica_more_page(report)
		self.draw_table_title_column(report, x, self.line_y)

		y = self.line_y + 0.9 * mm	
		x += 0.5 * mm

		report.setFont("Helvetica-Bold", 7)	
		report.setFillColorRGB(0, 0, 0, alpha=1)
		report.drawString(x, y, str(nome))
		x += 49.3 * mm
		report.drawString(x, y, "Ano - " + date(day= (now().day - 1), month= now().month, year=(now().year - 1)).strftime("%d/%m/%Y"))
		x += 26 * mm
		report.drawString(x, y, "Mes - " + date(day= (now().day - 1), month= (now().month - 1), year=now().year).strftime("%d/%m/%Y"))
		x += 26 * mm
		report.drawString(x, y, "Dia - " + (now() - 1).strftime("%d/%m/%Y"))
		x += 31 * mm

		report.drawString(x, y, "Ano - " + date(day= (now().day - 1), month= now().month, year=(now().year - 1)).strftime("%m/%Y"))
		x += 21 * mm
		report.drawString(x, y, "Mes - " + date(day= (now().day - 1), month= (now().month - 1), year=now().year).strftime("%m/%Y"))
		x += 21 * mm
		report.drawString(x, y, "Ate dia - " + (now() - 1).strftime("%d/%m"))
		self.line_y -= 3 * mm

	def draw_words_by_line_column(self, report, result_faturamento_list, um_title):
		#	Objetivo:	Criar e gerar todos o relatório de faturamento e volume de cada empresa
		#	Parâmetros: report => pdf, reulst_deposito_list => a lista de retorno que ele deve 
		#	desenhar, y => a posição de início no eixo y

		count_less_x_title = 10 * mm
		line = 0

		self.draw_words_title_column(report, count_less_x_title, self.line_y, "Grupo de produto")

		for result in result_faturamento_list:
			report.setFont("Helvetica", 7)
			column_x = 10 * mm

			gp_nome = ""
			if result.get('nome').decode("latin-1") == "Erro":
				gp_nome = "Sem nenhum movimento registrado"
			else:
				gp_nome = result.get('nome').decode("latin-1")

			report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm), gp_nome)
			column_x += 49.3 * mm
			report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('ano'))).rjust(2))))
			column_x += 25.9 * mm
			report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('mes'))).rjust(2))))
			column_x += 25.9 * mm
			report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('dia'))).rjust(2))))
			column_x += 30.9 * mm
			report.drawString(column_x, (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('a_ano'))).rjust(2))))
			column_x += 21 * mm
			report.drawString(column_x, (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('a_mes'))).rjust(2))))
			column_x += 21 * mm
			report.drawString(column_x, (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('a_dia'))).rjust(2))))

			self.draw_table_by_line_column(report, self.line_y, line)

			self.verifica_more_page(report)
			self.line_y -= 3 * mm
			line += 1

	def draw_words_by_line_column_consoli(self, report, result_faturamento_list, um_title):
		#	Objetivo:	Criar e gerar todos o relatório de faturamento e volume de cada empresa
		#	Parâmetros: report => pdf, reulst_deposito_list => a lista de retorno que ele deve 
		#	desenhar, y => a posição de início no eixo y
		
		print(result_faturamento_list)

		line = 0
		for result in result_faturamento_list:
			report.setFont("Helvetica", 7)
			column_x = 10 * mm

			gp_nome = ""
			if result.get('nome').decode("latin-1") == "Erro":
				gp_nome = "Sem nenhum movimento registrado"
			else:
				gp_nome = result.get('nome').decode("latin-1")

			report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm), gp_nome)
			column_x += 49.3 * mm
			report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('ano'))).rjust(2))))
			column_x += 25.9 * mm
			report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('mes'))).rjust(2))))
			column_x += 25.9 * mm
			report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('dia'))).rjust(2))))
			column_x += 30.9 * mm
			report.drawString(column_x, (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('a_ano'))).rjust(2))))
			column_x += 21 * mm
			report.drawString(column_x, (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('a_mes'))).rjust(2))))
			column_x += 21 * mm
			report.drawString(column_x, (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(self.L.convert_float(result.get('a_dia'))).rjust(2))))

			self.draw_table_by_line_column(report, self.line_y, line)

			print(gp_nome)
			print(TFloatDef.format(self.L.convert_float(result.get('a_dia'))).rjust(2))

			self.verifica_more_page(report)
			self.line_y -= 3 * mm
			line += 1
	
	def draw_words_subtotal(self, report, result_faturamento_list, um_title):
		#	Objetivo:	Criar e gerar todo o subtotal para cada relatório
		#	Parâmetros: report => pdf, reulst_deposito_list => a lista de retorno que ele deve, um_title => unidade de medida

		column_x = 10 * mm
		sum_ano = 0.0
		sum_mes = 0.0
		sum_dia = 0.0
		sum_ano_a = 0.0
		sum_mes_a = 0.0
		sum_dia_a = 0.0

		self.verifica_more_page(report)

		for result_dict in result_faturamento_list:
			sum_ano += self.L.convert_float(result_dict.get('ano'))
			sum_mes += self.L.convert_float(result_dict.get('mes'))
			sum_dia += self.L.convert_float(result_dict.get('dia'))
			sum_ano_a += self.L.convert_float(result_dict.get('a_ano'))
			sum_mes_a += self.L.convert_float(result_dict.get('a_mes'))
			sum_dia_a += self.L.convert_float(result_dict.get('a_dia'))

		report.setFont("Helvetica-Bold", 7)
		report.drawString((column_x + 32.5 * mm), (self.line_y + 0.5 * mm), "SUB TOTAL:")
		column_x += 49.3 * mm
		report.setFont("Helvetica", 7)
		self.draw_table_subtotal(report, column_x, self.line_y)
		report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(sum_ano).rjust(2))))
		column_x += 25.9 * mm
		report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm), str(str(um_title) + " " + str(TFloatDef.format(sum_mes).rjust(2))))
		column_x += 25.9 * mm
		report.drawString((column_x + 0.5 * mm), (self.line_y + 0.5 * mm),  str(str(um_title) + " " + str(TFloatDef.format(sum_dia).rjust(2))))
		column_x += 30.9 * mm
		report.drawString(column_x, (self.line_y + 0.5 * mm),  str(str(um_title) + " " + str(TFloatDef.format(sum_ano_a).rjust(2))))
		column_x += 20.9 * mm
		report.drawString(column_x, (self.line_y + 0.5 * mm),  str(str(um_title) + " " + str(TFloatDef.format(sum_mes_a).rjust(2))))
		column_x += 21 * mm
		report.drawString(column_x, (self.line_y + 0.5 * mm),  str(str(um_title) + " " + str(TFloatDef.format(sum_dia_a).rjust(2))))

		self.line_y -= 5 * mm

	def draw_table_title_column(self, report, x, y):
		#	Objetivo:	Criar a tabela para os titulos das colunas
		#	Parâmetros:	report => pdf gerado, x-y => eixos

		box_title = report.beginPath()
		report.setLineWidth(0.5)
		report.setFillColorRGB(0, 0, 0, alpha=0.5)
		box_title.rect(x - 0.5 * mm, y, 49.3 * mm, 3.5 * mm)
		x += 49.3 * mm
		box_title.rect(x - 0.5 * mm, y, 26 * mm, 3.5 * mm)
		x += 26 * mm
		box_title.rect(x - 0.5 * mm, y, 26 * mm, 3.5 * mm)
		x += 26 * mm
		box_title.rect(x - 0.5 * mm, y, 26 * mm, 3.5 * mm)
		x += 31.2 * mm
		box_title.rect(x - 1 * mm, y, 21 * mm, 3.5 * mm)
		x += 21 * mm
		box_title.rect(x - 1 * mm, y, 21 * mm, 3.5 * mm)
		x += 21 * mm
		box_title.rect(x - 1 * mm, y, 21 * mm, 3.5 * mm)
		report.drawPath(box_title, fill=1, stroke=1)

	def draw_table_by_line_column(self, report, y, line):
		#	Objetivo:	Criar a tabela para os lina das colunas
		#	Parâmetros:	report => pdf gerado, y => eixo, qtd_lines => qtd de linhas que deve ter
		
		report.setLineWidth(0.5)

		colunm_x = 10 * mm
		box_line = report.beginPath()
		if (line % 2) == 0:
			report.setFillColorRGB(0, 0, 0, alpha=0)
		else:
			report.setFillColorRGB(0, 0, 0, alpha=0.1)

		box_line.rect(colunm_x - 0.5 * mm, y, 49.3 * mm, 3 * mm)
		colunm_x += 49.3 * mm
		box_line.rect(colunm_x - 0.5 * mm, y, 26 * mm, 3 * mm)
		colunm_x += 26 * mm
		box_line.rect(colunm_x - 0.5 * mm, y, 26 * mm, 3 * mm)
		colunm_x += 26 * mm
		box_line.rect(colunm_x - 0.5 * mm, y, 26 * mm, 3 * mm)
		colunm_x += 31.2 * mm
		box_line.rect(colunm_x - 1 * mm, y, 21 * mm, 3 * mm)
		colunm_x += 21 * mm
		box_line.rect(colunm_x - 1 * mm, y, 21 * mm, 3 * mm)
		colunm_x += 21 * mm
		box_line.rect(colunm_x - 1 * mm, y, 21 * mm, 3 * mm)
		report.drawPath(box_line, fill=1, stroke=1)
		report.setFillColorRGB(0, 0, 0, alpha=1)
	
	def draw_table_subtotal(self, report, x, y):
		#	Objetivo:	Criar a tabela para os lina das colunas
		#	Parâmetros:	report => pdf gerado, y => eixo, qtd_lines => qtd de linhas que deve ter
		
		report.setLineWidth(0.5)
		box_line = report.beginPath()
		report.setFillColorRGB(0, 0, 0, alpha=0)

		box_line.rect(x - 0.5 * mm, y, 26 * mm, 3 * mm)
		x += 26 * mm
		box_line.rect(x - 0.5 * mm, y, 26 * mm, 3 * mm)
		x += 26 * mm
		box_line.rect(x - 0.5 * mm, y, 26 * mm, 3 * mm)
		x += 31.2 * mm
		box_line.rect(x - 1 * mm, y, 21 * mm, 3 * mm)
		x += 21 * mm
		box_line.rect(x - 1 * mm, y, 21 * mm, 3 * mm)
		x += 21 * mm
		box_line.rect(x - 1 * mm, y, 21 * mm, 3 * mm)
		report.drawPath(box_line, fill=1, stroke=1)
		report.setFillColorRGB(0, 0, 0, alpha=1)

class LinasStruct:
	#	Responsábilidade:	Realizar a comunição com o banco de dados e criar utiliários
	#	retornando as linhas e as seperando po empresa

	def __init__(self, ws):
		self.ws = ws
		self.db = ws.db	

	def retorno_empresas(self):
		return self.db.dictresult("select nome, grid from empresa where codigo != 100 order by codigo")
	
	def get_faturamento_consolidado(self, empresa):
		#	Objetivo:	Buscar um relatório de faturamento da empresa.
		#	Parâmetros:	empresa_grid => grid da empresa
		#	Retorno:	Dicionário com todos os retornos do select
		
		fat_list = []
		fat_list_c = []
		faturamento_list = []
		today = str('\''+(now() - 1).strftime("%Y-%m-%d")+'\'')

		grupo_dict_list = self.db.dictresult('''
			SELECT grid, nome FROM grupo_produto
			WHERE flag = \'A\' ORDER BY nome''')
		
		combus_dict_list = self.db.dictresult('''
			SELECT grid, nome FROM produto 
			WHERE grupo = 192 AND flag = \'A\'
			ORDER BY nome''')

		for grupo_dict in grupo_dict_list:
			if int(grupo_dict.get('grid') == 192):
				for combus_dict in combus_dict_list:
					val_list = []
					
					dia = self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data = %s
						AND l.empresa = %s
						AND l.operacao = \'V\'''' % (combus_dict.get('grid'), today, empresa))
					val_list.append(self.verf_valor_zero(dia[0].get('sum')))

					mes = self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data = (%s::date - interval \'1 month\')::date
						AND l.operacao = \'V\'
						AND l.empresa = %s''' % (combus_dict.get('grid'), today, empresa))
					val_list.append(self.verf_valor_zero(mes[0].get('sum')))

					ano = self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data = (%s::date - interval '1 year')::date
						AND l.operacao = \'V\'
						AND l.empresa = %s''' % (combus_dict.get('grid'), today, empresa))
					val_list.append(self.verf_valor_zero(ano[0].get('sum')))

					a_dia = self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data BETWEEN (DATE_TRUNC('month', %s::date))::date AND
							((DATE_TRUNC('month', %s::date)::date + interval '1 month') - interval '1 day')::date
						AND l.operacao = \'V\'
						AND l.empresa = %s''' % (combus_dict.get('grid'), today, today, empresa))
					val_list.append(self.verf_valor_zero(a_dia[0].get('sum')))

					a_mes = self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data BETWEEN (DATE_TRUNC('month', %s::date)::date - interval '1 month')::date AND
							((DATE_TRUNC('month', %s::date - interval '1 month')::date + interval '1 month') - interval '1 day')::date
						AND l.operacao = \'V\'
						AND l.empresa = %s''' % (combus_dict.get('grid'), today, today, empresa))
					val_list.append(self.verf_valor_zero(a_mes[0].get('sum')))

					a_ano = self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data BETWEEN (DATE_TRUNC('month', %s::date)::date - interval '1 year')::date AND
							((DATE_TRUNC('month', %s::date - interval '1 year')::date + interval '1 month') - interval '1 day')::date
						AND l.operacao = \'V\'
						AND l.empresa = %s''' % (combus_dict.get('grid'), today, today, empresa))
					val_list.append(self.verf_valor_zero(a_ano[0].get('sum')))

					if not True in val_list:
						continue

					build_list = [combus_dict.get('nome'),
						dia[0].get('sum'),
						mes[0].get('sum'),
						ano[0].get('sum'),
						a_dia[0].get('sum'),
						a_mes[0].get('sum'),
						a_ano[0].get('sum')]
					
					fat_list_c.append(self.monta_loop_dict(build_list))
			else:
				val_list = []
				dia = self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data = %s
					AND l.empresa = %s
					AND l.operacao = \'V\'''' % (grupo_dict.get('grid'), today, empresa))
				val_list.append(self.verf_valor_zero(dia[0].get('sum')))

				mes = self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data = (%s::date - interval \'1 month\')::date
					AND l.operacao = \'V\'
					AND l.empresa = %s''' % (grupo_dict.get('grid'), today, empresa))
				val_list.append(self.verf_valor_zero(mes[0].get('sum')))

				ano = self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data = (%s::date - interval '1 year')::date
					AND l.operacao = \'V\'
					AND l.empresa = %s''' % (grupo_dict.get('grid'), today, empresa))
				val_list.append(self.verf_valor_zero(ano[0].get('sum')))
				
				a_dia = self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data BETWEEN (DATE_TRUNC('month', %s::date))::date AND
						((DATE_TRUNC('month', %s::date)::date + interval '1 month') - interval '1 day')::date
					AND l.operacao = \'V\'
					AND l.empresa = %s''' % (grupo_dict.get('grid'), today, today, empresa))
				val_list.append(self.verf_valor_zero(a_dia[0].get('sum')))

				a_mes = self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data BETWEEN (DATE_TRUNC('month', %s::date)::date - interval '1 month')::date AND
						((DATE_TRUNC('month', %s::date - interval '1 month')::date + interval '1 month') - interval '1 day')::date
					AND l.operacao = \'V\'
					AND l.empresa = %s''' % (grupo_dict.get('grid'), today, today, empresa))
				val_list.append(self.verf_valor_zero(a_mes[0].get('sum')))

				a_ano = self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data BETWEEN (DATE_TRUNC('month', %s::date)::date - interval '1 year')::date AND
						((DATE_TRUNC('month', %s::date - interval '1 year')::date + interval '1 month') - interval '1 day')::date
					AND l.operacao = \'V\'
					AND l.empresa = %s''' % (grupo_dict.get('grid'), today, today, empresa))
				val_list.append(self.verf_valor_zero(a_ano[0].get('sum')))
				
				if not True in val_list:
					continue

				build_list = [grupo_dict.get('nome'), dia[0].get('sum'), mes[0].get('sum'), ano[0].get('sum'), a_dia[0].get('sum'), a_mes[0].get('sum'), a_ano[0].get('sum')]
				fat_list.append(self.monta_loop_dict(build_list))

		for fat in fat_list:
			faturamento_list.append(fat)
		for fat in fat_list_c:
			faturamento_list.append(fat)
		
		if faturamento_list:
			return faturamento_list
		else:
			return [{"nome": "Erro"}]

	def get_volume_consolidado(self, empresa):
		#	Objetivo:	Buscar um relatório de faturamento da empresa.
		#	Parâmetros:	empresa_grid => grid da empresa
		#	Retorno:	Dicionário com todos os retornos do select

		volume_list = []
		today = str('\''+(now() - 1).strftime("%Y-%m-%d")+'\'')

		combus_dict_list = self.db.dictresult('''
			SELECT grid, nome FROM produto 
			WHERE grupo = 192 AND flag = \'A\'
			ORDER BY nome''')

		for combus_dict in combus_dict_list:
			val_list = []

			dia = self.db.dictresult('''
				SELECT SUM(l.quantidade) FROM lancto l
				JOIN produto p ON p.grid = l.produto
				WHERE p.grid = %s
				AND l.data = %s
				AND l.empresa = %s
				AND l.operacao = \'V\'''' % (combus_dict.get('grid'), today, empresa))
			val_list.append(self.verf_valor_zero(dia[0].get('sum')))

			mes = self.db.dictresult('''
				SELECT SUM(l.quantidade) FROM lancto l
				JOIN produto p ON p.grid = l.produto
				WHERE p.grid = %s
				AND l.data = (%s::date - interval \'1 month\')::date
				AND l.operacao = \'V\'
				AND l.empresa = %s''' % (combus_dict.get('grid'), today, empresa))
			val_list.append(self.verf_valor_zero(mes[0].get('sum')))

			ano = self.db.dictresult('''
				SELECT SUM(l.quantidade) FROM lancto l
				JOIN produto p ON p.grid = l.produto
				WHERE p.grid = %s
				AND l.data = (%s::date - interval '1 year')::date
				AND l.operacao = \'V\'
				AND l.empresa = %s''' % (combus_dict.get('grid'), today, empresa))
			val_list.append(self.verf_valor_zero(ano[0].get('sum')))

			a_dia = self.db.dictresult('''
				SELECT SUM(l.quantidade) FROM lancto l
				JOIN produto p ON p.grid = l.produto
				WHERE p.grid = %s
				AND l.data BETWEEN (DATE_TRUNC('month', %s::date))::date AND
					((DATE_TRUNC('month', %s::date)::date + interval '1 month') - interval '1 day')::date
				AND l.operacao = \'V\'
				AND l.empresa = %s''' % (combus_dict.get('grid'), today, today, empresa))
			val_list.append(self.verf_valor_zero(a_dia[0].get('sum')))

			a_mes = self.db.dictresult('''
				SELECT SUM(l.quantidade) FROM lancto l
				JOIN produto p ON p.grid = l.produto
				WHERE p.grid = %s
				AND l.data BETWEEN (DATE_TRUNC('month', %s::date)::date - interval '1 month')::date AND
					((DATE_TRUNC('month', %s::date - interval '1 month')::date + interval '1 month') - interval '1 day')::date
				AND l.operacao = \'V\'
				AND l.empresa = %s''' % (combus_dict.get('grid'), today, today, empresa))
			val_list.append(self.verf_valor_zero(a_mes[0].get('sum')))

			a_ano = self.db.dictresult('''
				SELECT SUM(l.quantidade) FROM lancto l
				JOIN produto p ON p.grid = l.produto
				WHERE p.grid = %s
				AND l.data BETWEEN (DATE_TRUNC('month', %s::date)::date - interval '1 year')::date AND
					((DATE_TRUNC('month', %s::date - interval '1 year')::date + interval '1 month') - interval '1 day')::date
				AND l.operacao = \'V\'
				AND l.empresa = %s''' % (combus_dict.get('grid'), today, today, empresa))
			val_list.append(self.verf_valor_zero(a_ano[0].get('sum')))

			if not True in val_list:
					continue
			
			build_list = [combus_dict.get('nome'),
				 	dia[0].get('sum'),
					mes[0].get('sum'),
					ano[0].get('sum'),
					a_dia[0].get('sum'),
					a_mes[0].get('sum'),
					a_ano[0].get('sum')]
			
			volume_list.append(self.monta_loop_dict(build_list))

		if volume_list:
			return volume_list
		else:
			return [{"nome": "Erro"}]
	
	def get_margem_bruta_consolidado(self, empresa):
		#	Objetivo:	Buscar um relatório de faturamento da empresa.
		#	Parâmetros:	empresa_grid => grid da empresa
		#	Retorno:	Dicionário com todos os retornos do select

		mg_list = []
		mg_list_c = []
		marge_list = []

		#	Datas
		today = str('\'' + now().strftime("%Y-%m-%d") + '\'')
		data_d = Date((now().year), (now().month), (now().day - 1))
		today_d = str('\'' + (now() - 1).strftime("%Y-%m-%d") + '\'')
		sm_d = str('\'' + MonthStart(now()).strftime("%Y-%m-%d") + '\'')
		em_d = str('\'' + MonthEnd(now()).strftime("%Y-%m-%d") + '\'')

		date_m = Date((now().year), (now().month - 1), (now().day - 1))
		today_m = str('\'' + date_m.strftime("%Y-%m-%d") + '\'')
		sm_m = str('\'' + MonthStart(date_m).strftime("%Y-%m-%d") + '\'')
		em_m = str('\'' + MonthEnd(date_m).strftime("%Y-%m-%d") + '\'')

		date_y = Date((now().year - 1), (now().month), (now().day - 1))
		today_y = str('\'' + date_y.strftime("%Y-%m-%d") + '\'')
		sm_y = str('\'' + MonthStart(date_y).strftime("%Y-%m-%d") + '\'')
		em_y = str('\'' + MonthEnd(date_y).strftime("%Y-%m-%d") + '\'')

		grupo_dict_list = self.db.dictresult('''
			SELECT grid, nome FROM grupo_produto
			WHERE flag = \'A\' ORDER BY nome''')
		
		combus_dict_list = self.db.dictresult('''
			SELECT grid, nome FROM produto 
			WHERE grupo = 192 AND flag = \'A\'
			ORDER BY nome''')

		for grupo_dict in grupo_dict_list:
			if int(grupo_dict.get('grid') == 192):
				for combus_dict in combus_dict_list:
					E = Estoque(self.ws, empresa)
					val_list = []

					dia_venda_sum = self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data = %s
						AND l.empresa = %s
						AND l.operacao = \'V\'''' % (combus_dict.get('grid'), today_d, empresa))
					val_list.append(self.verf_valor_zero(dia_venda_sum[0].get('sum')))
					
					mes_venda_sum =	self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data = %s
						AND l.empresa = %s
						AND l.operacao = \'V\'''' % (combus_dict.get('grid'), today_m, empresa))
					val_list.append(self.verf_valor_zero(mes_venda_sum[0].get('sum')))

					ano_venda_sum =	self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data = %s
						AND l.empresa = %s
						AND l.operacao = \'V\'''' % (combus_dict.get('grid'), today_y, empresa))
					val_list.append(self.verf_valor_zero(ano_venda_sum[0].get('sum')))

					dia_venda_sum_a = self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data BETWEEN %s AND %s
						AND l.empresa = %s
						AND l.operacao = \'V\'''' % (combus_dict.get('grid'), sm_d, em_d, empresa))
					val_list.append(self.verf_valor_zero(dia_venda_sum_a[0].get('sum')))

					mes_venda_sum_a = self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data BETWEEN %s AND %s
						AND l.empresa = %s
						AND l.operacao = \'V\'''' % (combus_dict.get('grid'), sm_m, em_m, empresa))
					val_list.append(self.verf_valor_zero(mes_venda_sum_a[0].get('sum')))

					ano_venda_sum_a = self.db.dictresult('''
						SELECT SUM(l.valor) FROM lancto l
						JOIN produto p ON p.grid = l.produto
						WHERE p.grid = %s
						AND l.data BETWEEN %s AND %s
						AND l.empresa = %s
						AND l.operacao = \'V\'''' % (combus_dict.get('grid'), sm_y, em_y, empresa))
					val_list.append(self.verf_valor_zero(ano_venda_sum_a[0].get('sum')))

					if not True in val_list:
						continue

					if self.convert_float(dia_venda_sum[0].get('sum')) !=  0.0:
						dia_custo_sum = self._sum_get_cmv_combus(combus_dict.get('grid'), empresa, data_d, data_d)
					else:
						dia_custo_sum = 0.0
					dia = self.convert_float(dia_venda_sum[0].get('sum')) - dia_custo_sum

					if self.convert_float(mes_venda_sum[0].get('sum')) != 0.0:
						mes_custo_sum = self._sum_get_cmv_combus(combus_dict.get('grid'), empresa, date_m, date_m)
					else:
						mes_custo_sum = 0.0
					mes = self.convert_float(mes_venda_sum[0].get('sum')) - mes_custo_sum

					if self.convert_float(ano_venda_sum[0].get('sum')) != 0.0:
						ano_custo_sum = self._sum_get_cmv_combus(combus_dict.get('grid'), empresa, date_y, date_y)
					else:
						ano_custo_sum = 0.0
					ano = self.convert_float(ano_venda_sum[0].get('sum')) - ano_custo_sum

					if self.convert_float(dia_venda_sum_a[0].get('sum')):
						dia_custo_sum_a = self._sum_get_cmv_combus(combus_dict.get('grid'), empresa, MonthStart(data_d), MonthEnd(data_d))
					else:
						dia_custo_sum_a = 0.0
					a_dia = self.convert_float(dia_venda_sum_a[0].get('sum')) - dia_custo_sum_a

					if self.convert_float(mes_venda_sum_a[0].get('sum')) != 0.0:
						mes_custo_sum_a = self._sum_get_cmv_combus(combus_dict.get('grid'), empresa, MonthStart(date_m), MonthEnd(date_m))
					else:
						mes_custo_sum_a = 0.0
					a_mes = self.convert_float(mes_venda_sum_a[0].get('sum')) - mes_custo_sum_a

					if self.convert_float(ano_venda_sum_a[0].get('sum')) != 0.0:
						ano_custo_sum_a = self._sum_get_cmv_combus(combus_dict.get('grid'), empresa, MonthStart(date_y), MonthEnd(date_y))
					else:
						ano_custo_sum_a = 0.0
					a_ano = self.convert_float(ano_venda_sum_a[0].get('sum')) - ano_custo_sum_a

					build_list = [combus_dict.get('nome'),
						dia, mes, ano,
						a_dia, a_mes, a_ano]

					mg_list_c.append(self.monta_loop_dict(build_list))		
			else:
				val_list = []
				dia_venda_sum = self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data = %s
					AND l.empresa = %s
					AND l.operacao = \'V\'''' % (grupo_dict.get('grid'), today_d, empresa))
				val_list.append(self.verf_valor_zero(dia_venda_sum[0].get('sum')))

				mes_venda_sum =	self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data = %s
					AND l.empresa = %s
					AND l.operacao = \'V\'''' % (grupo_dict.get('grid'), today_m, empresa))
				val_list.append(self.verf_valor_zero(mes_venda_sum[0].get('sum')))

				ano_venda_sum =	self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data = %s
					AND l.empresa = %s
					AND l.operacao = \'V\'''' % (grupo_dict.get('grid'), today_y, empresa))
				val_list.append(self.verf_valor_zero(ano_venda_sum[0].get('sum')))

				dia_venda_sum_a = self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data BETWEEN %s AND %s
					AND l.empresa = %s
					AND l.operacao = \'V\'''' % (grupo_dict.get('grid'), sm_d, em_d, empresa))
				val_list.append(self.verf_valor_zero(dia_venda_sum_a[0].get('sum')))

				mes_venda_sum_a = self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data BETWEEN %s AND %s
					AND l.empresa = %s
					AND l.operacao = \'V\'''' % (grupo_dict.get('grid'), sm_m, em_m, empresa))
				val_list.append(self.verf_valor_zero(mes_venda_sum_a[0].get('sum')))
				
				ano_venda_sum_a = self.db.dictresult('''
					SELECT SUM(l.valor) FROM lancto l
					JOIN produto p ON p.grid = l.produto
					WHERE p.grupo = %s
					AND l.data BETWEEN %s AND %s
					AND l.empresa = %s
					AND l.operacao = \'V\'''' % (grupo_dict.get('grid'), sm_y, em_y, empresa))
				val_list.append(self.verf_valor_zero(ano_venda_sum_a[0].get('sum')))

				if not True in val_list:
					continue
					
				if self.convert_float(dia_venda_sum[0].get('sum')) !=  0.0:
					dia_custo_sum = self._sum_get_cmv_grupo(grupo_dict.get('grid'), empresa, data_d, data_d)
				else:
					dia_custo_sum = 0.0
				dia = self.convert_float(dia_venda_sum[0].get('sum')) - dia_custo_sum

				if self.convert_float(mes_venda_sum[0].get('sum')) != 0.0:
					mes_custo_sum = self._sum_get_cmv_grupo(grupo_dict.get('grid'), empresa, date_m, date_m)
				else:
					mes_custo_sum = 0.0
				mes = self.convert_float(mes_venda_sum[0].get('sum')) - mes_custo_sum

				if self.convert_float(ano_venda_sum[0].get('sum')) != 0.0:
					ano_custo_sum = self._sum_get_cmv_grupo(grupo_dict.get('grid'), empresa, date_y, date_y)
				else:
					ano_custo_sum = 0.0
				ano = self.convert_float(ano_venda_sum[0].get('sum')) - ano_custo_sum

				if self.convert_float(dia_venda_sum_a[0].get('sum')):
					dia_custo_sum_a = self._sum_get_cmv_grupo(grupo_dict.get('grid'), empresa, MonthStart(data_d), MonthEnd(data_d))
				else:
					dia_custo_sum_a = 0.0
				a_dia = self.convert_float(dia_venda_sum_a[0].get('sum')) - dia_custo_sum_a

				if self.convert_float(mes_venda_sum_a[0].get('sum')) != 0.0:
					mes_custo_sum_a = self._sum_get_cmv_grupo(grupo_dict.get('grid'), empresa, MonthStart(date_m), MonthEnd(date_m))
				else:
					mes_custo_sum_a = 0.0
				a_mes = self.convert_float(mes_venda_sum_a[0].get('sum')) - mes_custo_sum_a

				if self.convert_float(ano_venda_sum_a[0].get('sum')) != 0.0:
					ano_custo_sum_a = self._sum_get_cmv_grupo(grupo_dict.get('grid'), empresa, MonthStart(date_y), MonthEnd(date_y))
				else:
					ano_custo_sum_a = 0.0
				a_ano = self.convert_float(ano_venda_sum_a[0].get('sum')) - ano_custo_sum_a

				build_list = [grupo_dict.get('nome'),
					dia, mes, ano,
					a_dia, a_mes, a_ano]

				mg_list.append(self.monta_loop_dict(build_list))

		for mg in mg_list:
			marge_list.append(mg)
		for mg in mg_list_c:
			marge_list.append(mg)

		if marge_list:
			return marge_list
		else:
			return [{"nome": "Erro"}]
	
	#	Util
	
	def verf_valor_zero(self, param):
		if param:
			return True
		return False
	
	def _sum_get_cmv_grupo(self, grupo, empresa, data_ini, data_fim):
		cmv_final = 0.0
		d_ini = str('\'' + data_ini.strftime("%Y-%m-%d") + '\'')
		d_fim = str('\'' + data_fim.strftime("%Y-%m-%d") + '\'')

		produto_dict_list = self.db.dictresult('''
		SELECT grid, nome FROM produto 
			WHERE grupo = %s''' % grupo)
		
		for produto_dict in produto_dict_list:
			cmv = self.db.dictresult('''SELECT get_cmv(%s, %s, %s, %s, null)''' % (empresa, produto_dict.get('grid'), d_ini, d_fim))
			cmv_final += self.convert_float(cmv[0].get('get_cmv'))
		return cmv_final

	def _sum_get_cmv_combus(self, produto, empresa, data_ini, data_fim):
		d_ini = str('\'' + data_ini.strftime("%Y-%m-%d") + '\'')
		d_fim = str('\'' + data_fim.strftime("%Y-%m-%d") + '\'')
		cmv = self.db.dictresult('''SELECT get_cmv(%s, %s, %s, %s, null)''' % (empresa, produto, d_ini, d_fim))
		return self.convert_float(cmv[0].get('get_cmv'))

	def monta_loop_dict(self, list):
		#	Objetivo:	Criar um dict de acordo com os dados passados
		#	Parâmetros:	list => lista do dados
		#	Retorno:	Dicionário com todos os retornos de acordo com a lista
		return {'nome': list[0], 
			'dia': list[1],
			'mes': list[2],
			'ano': list[3],
			'a_dia': list[4],
			'a_mes': list[5],
			'a_ano': list[6]}

	def convert_float(self, param):
		if param:
			return param
		else:
			return float(0.0)
		
if __name__ == '__main__':
	from util.workspace	import ws
	ws.connect_db()
	ws.user.load_info(-1)
	os.environ['ASMODULE'] = 'main'
	ManutProg(ws).run(console=True)
