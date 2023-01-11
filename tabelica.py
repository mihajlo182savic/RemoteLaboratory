import xlsxwriter
workbook = xlsxwriter.Workbook('reyultati.xlsx')
worksheet=workbook.add_worksheet()
worksheet.set_column('A:A', 20)
worksheet.write(0,0,"nesto")
worksheet.write(1,0,"nesto1")
worksheet.write(2,0,"nesto2")
workbook.close()

