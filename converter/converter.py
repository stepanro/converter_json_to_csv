import argparse
import re
from chardet.universaldetector import UniversalDetector
import xml.etree.ElementTree as ET
import csv
	
	
class XmlToStlConverter:
	def __init__(self, column_name):
		self.data = dict()
		self.column_name = column_name
		self.temp_list = list()
	
	def detect_encoding(self, path_input_file):
		with open(file=path_input_file, mode='rb') as temp_xml:
			detector = UniversalDetector()
			for line in temp_xml.readlines():
				detector.feed(line)
				if detector.done:
					break
			detector.close()
			encoding = detector.result['encoding']
					
		self.data['encoding'] = encoding
	
		# with open(file=f"{self.data['path_dir_input_file']}{self.data['name_out_csv_file']}", 
		#           mode='a', encoding=self.data['encoding']) as temp_csv:
		#     temp_csv.write(self.data['name_in_xml_file'] + ';')
	
	def arguments_parser(self):
		parser = argparse.ArgumentParser()
		parser.add_argument(dest='path_input_file', type=str, help='path of the input file')
		args = parser.parse_args()
		path_input_file = args.path_input_file
		self.data['path_input_file'] = path_input_file
		pattern = r'(.+)(?<=\/)'
		path_dir_input_file = re.findall(pattern, path_input_file)
		if not (path_dir_input_file):
			path_dir_input_file = ''
		else:
			path_dir_input_file = path_dir_input_file[0]
		self.data['path_dir_input_file'] = path_dir_input_file 
		pattern = r'(?<=\/)(.+)(?<=\.xml)'
		name_in_xml_file = re.findall(pattern, path_input_file)
		if not (name_in_xml_file):
			name_in_xml_file = path_input_file
		else:
			name_in_xml_file = name_in_xml_file[0]
		self.data['name_in_xml_file'] = name_in_xml_file
		pattern = r'(?<=\.)(.+)'
		name_out_csv_file = re.sub(pattern, 'csv', name_in_xml_file)
		self.data['name_out_csv_file'] = name_out_csv_file
		
		return path_input_file
	
	def scanner(self):
		# with open(file=self.data['path_input_file'], mode='r', encoding=self.data['encoding']) as temp_xml:
		#     count_column_name = len(self.column_name)
		#     for line in temp_xml.readlines():
		#         for column_count, pattern in enumerate(self.column_name.values()):
		#             answer_regular = re.findall(pattern, line)
		#             if answer_regular:
		#                 with open(file=f"{self.data['path_dir_input_file'] + self.data['name_out_csv_file']}", 
		#                           mode='a', encoding=self.data['encoding']) as temp_csv:
							
		#                     if column_count + 1 < count_column_name:
		#                         end_text = ';'
		#                     else:
		#                         print(column_count)
		#                         end_text = '\n'
		#                     text = f"{answer_regular[0][1]}{end_text}"
		#                     temp_csv.write(text)   
		#             else:
		#                 pass

		print(self.data['path_input_file'])
		tree = ET.parse(self.data['path_input_file'])
		root = tree.getroot()
	
		for child in root:
			for i in child:
				for c in i:
					for v in c:
						if v.tag == 'ДатаФайл':
							self.temp_list.append(self.data['name_in_xml_file'])
							self.temp_list.append(v.text)
							self.temp_list.append(self.data['encoding'])
							with open(file=f"{self.data['path_dir_input_file']}{self.data['name_out_csv_file']}", 
							  mode='a', encoding=self.data['encoding']) as temp_csv:
								writer = csv.writer(temp_csv, delimiter=';')
								writer.writerow(self.temp_list)
						
							self.temp_list = list()
							
				if i.tag == 'Плательщик':
					for j in i:
						if j.text == 'ЛицСч':
							id_number = j.text
						if j.text == 'ФИО':
							full_name = j.text
						if j.text == 'Адрес':
							address = j.text
						if j.text == 'Период':
							period = j.text
						if j.text == 'Сумма':
							amount_money = j.text

						
						self.temp_list.append(j.text)
					with open(file=f"{self.data['path_dir_input_file']}{self.data['name_out_csv_file']}", 
							  mode='a', encoding=self.data['encoding']) as temp_csv:
						writer = csv.writer(temp_csv, delimiter=';')
						writer.writerow(self.temp_list)
	
					self.temp_list = list()
					