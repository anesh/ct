import csv
import xlsxwriter

f1 = file('2020fw.csv', 'r')
f2 = file('2019fw.csv', 'r')

c1 = csv.reader(f1)
c2 = csv.reader(f2)

book = xlsxwriter.Workbook('results.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["rulename","from zone","to zone","addtional comments","reviewd action","rule description","result"]
for col, text in enumerate(header):
	sheet.write(0, col, text, header_format)


oldlist = list(c2)
xrow=0
for sourceip_row in c1:
    row = 1
    xrow= xrow+1
    found = False
    for old_row in oldlist:
        if sourceip_row[9] == old_row[3] and sourceip_row[14] == old_row[6] and sourceip_row[17] == old_row[9]:
	    sheet.write(xrow,0,old_row[16])
	    sheet.write(xrow,1,old_row[14])
	    sheet.write(xrow,2,old_row[15])
            sheet.write(xrow,3,old_row[13])
	    sheet.write(xrow,4,old_row[12])
	    sheet.write(xrow,5,old_row[24])
	    sheet.write(xrow,6,'FOUND in 2019 sheet (row ' + str(row) + ')')
	    found = True
	row = row + 1
    if not found:
	sheet.write(xrow,0,sourceip_row[9])
	sheet.write(xrow,1,'NOT found in 2019 sheet')

f1.close()
f2.close()
book.close()
