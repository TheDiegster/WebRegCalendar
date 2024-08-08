import pandas as pd
from datetime import datetime as dt
from ics import Calendar, Event
import pytz
from pypdf import PdfReader
from ics.grammar.parse import ContentLine
import re
# All the possible course codes at UCSD
rawCourseCodes = ["AAPI", "AAS", "AESE", "AIP", "ANAR", "ANBI", "ANES", "ANSC", "ANTH", "ASTR", "AUD", "AWP", "BENG", "BGGN", "BGJC", "BGRD", "BGSE", "BIBC", "BICD", "BIEB", "BILD", "BIMM", "BIOM", "BIPN", "BISP", "BNFO", "CAT", "CCE", "CCS", "CENG", "CGS", "CHEM", "CHIN", "CLAS", "CLIN", "CLRE", "CLSS", "CLX", "CMM", "COGR", "COGS", "COMM", "CONT", "CSE", "CSS", "DDPM", "DERM", "DOC", "DSC", "DSE", "DSGN", "EAP", "ECE", "ECON", "EDS", "EIGH", "EMED", "ENG", "ENVR", "ERC", "ESYS", "ETHN", "ETIM", "EXPR", "FILM", "FMPH", "FPM", "GLBH", "GMST", "GPCO", "GPEC", "GPGN", "GPIM", "GPLA", "GPPA", "GPPS", "GSS", "HDP", "HDS", "HIAF", "HIEA", "HIEU", "HIGL", "HIGR", "HILA", "HILD", "HINE", "HISA", "HISC", "HITO", "HIUS", "HLAW", "HMNR", "HUM", "ICEP", "INTL", "IRLA", "JAPN", "JWSP", "LATI", "LAWS", "LHCO", "LIAB", "LIDS", "LIEO", "LIFR", "LIGM", "LIGN", "LIHI", "LIHL", "LIIT", "LIPO", "LISL", "LISP", "LTAF", "LTAM", "LTCH", "LTCO", "LTCS", "LTEA", "LTEN", "LTEU", "LTFR", "LTGK", "LTGM", "LTIT", "LTKO", "LTLA", "LTRU", "LTSP", "LTTH", "LTWL", "LTWR", "MAE", "MATH", "MATS", "MBC", "MCWP", "MDE", "MED", "MGT", "MGTA", "MGTF", "MGTP", "MMW", "MSED", "MSP", "MUIR", "MUS", "NANO", "NEU", "NEUG", "OBG", "OPTH", "ORTH", "PATH", "PEDS", "PH", "PHAR", "PHB", "PHIL", "PHLH", "PHYA", "PHYS", "POLI", "PSY", "PSYC", "RAD", "RELI", "REV", "RMAS", "RMED", "SE", "SEV", "SIO", "SIOB", "SIOC", "SIOG", "SOCE", "SOCG", "SOCI", "SOCL", "SOMC", "SOMI", "SPPH", "SPPS", "SURG", "SXTH", "SYN", "TDAC", "TDDE", "TDDM", "TDDR", "TDGE", "TDGR", "TDHD", "TDHT", "TDMV", "TDPF", "TDPR", "TDPW", "TDTR", "TKS", "TMC", "TWS", "UROL", "USP", "VIS", "WARR", "WCWP", "WES"]
courseCodes = set(rawCourseCodes)
reader = PdfReader("webregMain.pdf")
#reader = PdfReader("SI2classes.pdf")
page = reader.pages[0]
rawData = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=1)
newlineCount = rawData.count('\n')
rawRows = rawData.split('\n')
#print(rawData)
# Only select rows containing course and schuedule information
start_index = 4 #should be 4
end_index = -1
selectRows = rawRows[start_index:end_index] # List of rows

# for row in selectRows:
#     if row[-1] == 

def printPdfFormat():
    for item in selectRows:
        print(item)

noLeadSpaceRows = [row.strip() for row in selectRows]
cleanedRows = [' '.join(row.split()) for row in noLeadSpaceRows]
courseCodeStartIndices = []
courseCode = ''
# Loop to check first word of every row, which implies check first collection of chars
for idx, row in enumerate(cleanedRows):
    # Loop to build possible course code at the beginning of each row
    for char in row:
        # as soon as we encounter the end of our first string, break
        if (char == ' '):
            break
        # otherwise continue creating the course code
        courseCode += char
    # if course code was found, store it
    if (courseCode in courseCodes):
        # save row indices that belong to a course
        courseCodeStartIndices.append(idx)
    # Reset courseCode string to prepare for another check next iteration
    # if we didn't find it then we still have to reset it
    courseCode = ''

lastRowIdx = len(cleanedRows)-1
courseCodeRanges = courseCodeStartIndices + [lastRowIdx]

#printPdfFormat()

# with open('testOutput.txt', 'w') as file:
#     for row in selectRows:
#         print(row, file=file)


#Extract time from selectRows
testRow = selectRows[0].split()
testRow = ','.join(testRow)

subCourseRegex = r'[A-Z]{3,4}\s\d+[A-Z]{0,1}'
titleRegex = r''
secCodeRegex = r''
typeRegex = r'LE\s|DI\s|MI\s|FI\s|LA\s'
instructorRegex = r'\s[A-Z][a-z]+,\s[A-Z][a-z]+\s'
gradeOpRegex = r''
unitsRegex = r''
# 1:MWF option  2:TuTh option  3:Test Dates Option  4:Single day M or W or F  5:Single day Tu or Th  6:Two of MWF option  7:SummerClass Option  8:TBA option
#              [  1  ] [ 2 ][                      3                         ][    4    ][     5     ][   6     ][   7  ][8]                                         
daysRegex = r'[MWF]{3}|TuTh|(\s[MWF]\s|\s(Tu|Th)\s|\sSa\s)\d{2}\/\d{2}\/\d{4}|(\s[MWF]\s|\s(Tu|Th)\s)|(MW|WF|MF)|MTuWThF|TBA'
timeRegex = r'\d{1,2}:\d{2}[ap]-\d{1,2}:\d{2}[ap]'
bldgRegex = r''
roomRegex = r''
regexi = [subCourseRegex, titleRegex, secCodeRegex, typeRegex, instructorRegex, gradeOpRegex, unitsRegex, daysRegex, timeRegex, bldgRegex, roomRegex]



regexi = [subCourseRegex, typeRegex, instructorRegex, daysRegex, timeRegex]
finalDataset = [[]]
def parseData(data, regexi, output):
    for row in data:
        rowData = []
        for regex in regexi:
            query = re.search(regex, row)
            if query != None:
                rowData.append(query.group().strip())
            else:
                rowData.append('')
        output.append(rowData)
    return output

def printData(data):
    for row in data:
        print(row)

parseData(selectRows, regexi, finalDataset)
#printData(finalDataset)


printPdfFormat()















#TODO: Extract Title,
# Characteristics: 1. String of words where each char starts with a capital letter
#2. the first word DOESN't have a , after it

#printPdfFormat()





# maybe start after first two words
# end before section code: Capital letter followed by 2 digits

# titleRegex = r'[A-Z]+\d+\s?     [A-Z][a-z]+'
# for row in selectRows:
#     title = re.search(titleRegex, row)
#     if title == None:
#         print('')
#     else:
#         print(title.group())
