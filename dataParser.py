import pandas as pd
from itertools import zip_longest
from datetime import datetime as dt
from ics import Calendar, Event
import pytz
from pypdf import PdfReader
from ics.grammar.parse import ContentLine
import re

instructionStartEndDates = {'Summer Session II 2023': ('20230807', '20230908'), 'Fall Quarter 2023': ('20230928', '20231208'), 'Winter Quarter 2024': ('20240108', '20240315'), 'Spring Quarter 2024': ('20240401', '20240607'), 'Summer Session I 2024': ('20240701', '20240802'), 'Summer Session II 2024': ('20240805', '20240906'), 'Fall Quarter 2024': ('20240926', '20241206'), 'Winter Quarter 2025': ('20250106', '20250314'), 'Spring Quarter 2025': ('20250331', '20250606') }
def printData(data):
    for row in data:
        print(row)
# All the possible course codes at UCSD
rawCourseCodes = ["AAPI", "AAS", "AESE", "AIP", "ANAR", "ANBI", "ANES", "ANSC", "ANTH", "ASTR", "AUD", "AWP", "BENG", "BGGN", "BGJC", "BGRD", "BGSE", "BIBC", "BICD", "BIEB", "BILD", "BIMM", "BIOM", "BIPN", "BISP", "BNFO", "CAT", "CCE", "CCS", "CENG", "CGS", "CHEM", "CHIN", "CLAS", "CLIN", "CLRE", "CLSS", "CLX", "CMM", "COGR", "COGS", "COMM", "CONT", "CSE", "CSS", "DDPM", "DERM", "DOC", "DSC", "DSE", "DSGN", "EAP", "ECE", "ECON", "EDS", "EIGH", "EMED", "ENG", "ENVR", "ERC", "ESYS", "ETHN", "ETIM", "EXPR", "FILM", "FMPH", "FPM", "GLBH", "GMST", "GPCO", "GPEC", "GPGN", "GPIM", "GPLA", "GPPA", "GPPS", "GSS", "HDP", "HDS", "HIAF", "HIEA", "HIEU", "HIGL", "HIGR", "HILA", "HILD", "HINE", "HISA", "HISC", "HITO", "HIUS", "HLAW", "HMNR", "HUM", "ICEP", "INTL", "IRLA", "JAPN", "JWSP", "LATI", "LAWS", "LHCO", "LIAB", "LIDS", "LIEO", "LIFR", "LIGM", "LIGN", "LIHI", "LIHL", "LIIT", "LIPO", "LISL", "LISP", "LTAF", "LTAM", "LTCH", "LTCO", "LTCS", "LTEA", "LTEN", "LTEU", "LTFR", "LTGK", "LTGM", "LTIT", "LTKO", "LTLA", "LTRU", "LTSP", "LTTH", "LTWL", "LTWR", "MAE", "MATH", "MATS", "MBC", "MCWP", "MDE", "MED", "MGT", "MGTA", "MGTF", "MGTP", "MMW", "MSED", "MSP", "MUIR", "MUS", "NANO", "NEU", "NEUG", "OBG", "OPTH", "ORTH", "PATH", "PEDS", "PH", "PHAR", "PHB", "PHIL", "PHLH", "PHYA", "PHYS", "POLI", "PSY", "PSYC", "RAD", "RELI", "REV", "RMAS", "RMED", "SE", "SEV", "SIO", "SIOB", "SIOC", "SIOG", "SOCE", "SOCG", "SOCI", "SOCL", "SOMC", "SOMI", "SPPH", "SPPS", "SURG", "SXTH", "SYN", "TDAC", "TDDE", "TDDM", "TDDR", "TDGE", "TDGR", "TDHD", "TDHT", "TDMV", "TDPF", "TDPR", "TDPW", "TDTR", "TKS", "TMC", "TWS", "UROL", "USP", "VIS", "WARR", "WCWP", "WES"]
courseCodes = set(rawCourseCodes)
#reader = PdfReader("/home/diegom/CSProjects/WebRegCalendarTestData/webregMain.pdf")
reader = PdfReader("/home/diegom/CSProjects/WebRegCalendarTestData/SI2classes.pdf")
page = reader.pages[0]
rawData = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=1)
newlineCount = rawData.count('\n')
rawRows = rawData.split('\n')

termAndYearRegex = r'-\s([A-Za-z\s\d]+)'
termAndYear = re.search(termAndYearRegex, rawRows[1]).group(1)

instructionStartYear = int((instructionStartEndDates[termAndYear][0])[:4])
instructionStartMonth = int((instructionStartEndDates[termAndYear][0])[4:6])
instructionStartDay = int((instructionStartEndDates[termAndYear][0])[6:])

instructionEndYear = int((instructionStartEndDates[termAndYear][1])[:4])
instructionEndMonth = int((instructionStartEndDates[termAndYear][1])[4:6])
instructionEndDay = int((instructionStartEndDates[termAndYear][1])[6:])


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

# delete the word enrolled from relevant rows
splitdata = [[]]
numOfCourses = len(courseCodeStartIndices)
currCourseIdx = 0
for idx, row in enumerate(selectRows):
    words = row.split()
    if currCourseIdx < numOfCourses and idx == courseCodeStartIndices[currCourseIdx] :
        courseCodeRow = courseCodeStartIndices[currCourseIdx]
        currCourseIdx += 1
    if idx == courseCodeRow:
        words.pop(-1)
    splitdata.append(words)
splitdata.pop(0)






subCourseRegex = r'[A-Z]{3,4}\s\d+[A-Z]{0,1}'
titleRegex = ''
secCodeRegex = r'\s[A-Z]\d{2}\s'
typeRegex = r'LE\s|DI\s|MI\s|FI\s|LA\s'
instructorRegex = r'\s[A-Z][a-z]+,\s[A-Z][a-z]+\s'
gradeOpRegex = ''
unitsRegex = ''
# 1:MWF option  2:TuTh option  3:Test Dates Option  4:Single day M or W or F  5:Single day Tu or Th  6:Two of MWF option  7:SummerClass Option  8:TBA option
#              [  1  ] [ 2 ][                      3                         ][    4    ][     5     ][   6     ][   7  ][8]                                         
daysRegex = r'[MWF]{3}|TuTh|(\s[MWF]\s|\s(Tu|Th)\s|\sSa\s)\d{2}\/\d{2}\/\d{4}|(\s[MWF]\s|\s(Tu|Th)\s)|(MW|WF|MF)|MTuWThF|TBA'
timeRegex = r'\d{1,2}:\d{2}[ap]-\d{1,2}:\d{2}[ap]|TBA'
regexi = [subCourseRegex, titleRegex, secCodeRegex, typeRegex, instructorRegex, gradeOpRegex, unitsRegex, daysRegex, timeRegex]
finalDataset = [[]]
def parseData(data, regexi, output):
    for row in data:
        rowData = []
        for regex in regexi:
            if regex == '':
                rowData.append('')
                continue
            query = re.search(regex, row)
            if query != None:
                rowData.append(query.group().strip())
            else:
                rowData.append('')
        output.append(rowData)
    return output
# Had to pop off empty list in the beginning, not sure why empty list was being appended
parseData(selectRows, regexi, finalDataset).pop(0)

for idx, row in enumerate(splitdata):
    if len(row) < 2:
        finalDataset.append('')
        continue
    roomNum = row[-1]
    bldg = row[-2]
    bldgAndRoom = bldg + ' ' + roomNum
    finalDataset[idx].append(bldgAndRoom)

# finalDataset is now correct!

def getCourseNames():
    courseNames = []
    for index in courseCodeStartIndices:
        courseNames.append(finalDataset[index][0])
    return courseNames

#print(getCourseNames())
def printCsvFormat():        
    for row in finalDataset:
        print(row)

df = pd.DataFrame(finalDataset)
#printPdfFormat()
#printCsvFormat()
# TODO: prompt user for beginning/end of instruction date
# for now use hard coded start and end days

def createStartAndEndTimes(timeString):
    startTime = ''
    endTime = ''
    sawDash = False
    for char in timeString:
        if sawDash == True:
            endTime += char
            continue
        if char == '-':
            sawDash = True
            continue
        startTime += char
    return startTime, endTime

def standardToMilitaryTime(timeToConvert):
    # add a 0 in front of PM start times
    if timeToConvert[1] == ':':
        timeToConvert = "0" + timeToConvert
    if timeToConvert[-1] == 'a':
        timeToConvert = timeToConvert[:-1] #shaves off 'a' from time string
        timeToConvert = timeToConvert + "AM"
    if timeToConvert[-1] == 'p':
        timeToConvert = timeToConvert[:-1] #shaves off 'p' from time string
        timeToConvert = timeToConvert + "PM"

    standardTime = dt.strptime(timeToConvert, '%I:%M%p')
    militaryTime = standardTime.strftime('%H:%M')
    return militaryTime

def formatStartTime(startTime):
    startHour = ''
    startMinute = ''
    if startTime[-1] == 'p':
        startTime = standardToMilitaryTime(startTime)
        startHour = startTime[:-3]
        startMinute = startTime[-2:]
    else:
        startHour = startTime[:-4]
        startTime = startTime[:-1] #shave off 'a' for am start time classes
        startMinute = startTime[-2:]
    return startHour, startMinute

def formatEndTime(endTime):
    endHour = ''
    endMinute = ''
    if endTime[-1] == 'p':
        endTime = standardToMilitaryTime(endTime)
        endHour = endTime[:-3]
        endMinute = endTime[-2:]
    else:
        endHour = endTime[:-4]
        endTime = endTime[:-1] # shave off 'a' for am start time classes
        endMinute = endTime[-2:]
    return endHour, endMinute

# INPUT: string of WebReg days of a certain event
# OUTPUT: string of WebReg days in .ics readable format
def rEventDays(days):
    formattedDays = []
    currDay = ''
    for char in days:
        currDay += char
        if currDay == 'M':
            formattedDays.append('MO')
            currDay = ''
        elif currDay == 'Tu':
            formattedDays.append('TU')
            currDay = ''
        elif currDay == 'W':
            formattedDays.append('WE')
            currDay = ''   
        elif currDay == 'Th':
            formattedDays.append('TH')
            currDay = ''
        elif currDay == 'F':
            formattedDays.append('FR')
            currDay = ''
    return formattedDays

# use .ics lib to create a calendar object in which events can go into
c = Calendar()


# hard coded lecture name, and start/end time
#lecture.name = finalDataset[0][0] + " Lecture"

# create datetime strings for DTSTART and DTEND fields for recurring events
# i.e. LE, DI, LA
def rEventDTs(row, startWeekday):
    offset = 0 
    if startWeekday == 'TU':
        offset = 1
    elif startWeekday == 'W':
        offset = 2
    elif startWeekday == 'TH':
        offset = 3
    elif startWeekday == 'F':
        offset = 4
    elif startWeekday == 'SA':
        offset = 5
    timeString = finalDataset[row][8]
    startTime, endTime = createStartAndEndTimes(timeString)
    startHour, startMinute = formatStartTime(startTime)
    # dt() auto zero pads 
    dtStart = dt(instructionStartYear, instructionStartMonth, instructionStartDay + offset, int(startHour), int(startMinute))
    startString = dtStart.strftime('%Y%m%dT%H%M%S')
    endHour, endMinute = formatEndTime(endTime)
    # to create LE, DI, LAB. Make first event last until instructionStart, THEN have it repeat until instructionEnd
    dtEnd = dt(instructionStartYear, instructionStartMonth, instructionStartDay + offset, int(endHour), int(endMinute))
    endString = dtEnd.strftime('%Y%m%dT%H%M%S')
    return startString, endString


def createRruleString(row):
    # recurring repeat until instruction end
    
    untilDt = dt(instructionEndYear, instructionEndMonth, instructionEndDay, 23, 59)
    pacific = pytz.timezone("America/Los_Angeles")
    untilPacDt = pacific.localize(untilDt)
    untilUtcDt = untilPacDt.astimezone(pytz.utc)
    untilString = untilUtcDt.strftime('UNTIL=%Y%m%dT%H%M%SZ')
    # create string for the BYDAY field
    formattedDays = rEventDays(finalDataset[row][7])
    byDayString = ','.join(formattedDays)

    # create final rruleString
    rruleString = "FREQ=WEEKLY;" + untilString + ";WKST=" + "SU" + ";BYDAY=" + byDayString

    return rruleString

# INPUT: a row of course test (Midterm or Final) data
# OUTPUT: formatted start and end DT objects for tests
def testDTs(row):
    rawData = finalDataset[row][7]
    timeString = finalDataset[row][8]
    if rawData[0] == "S":
        rawData = rawData[2:]
    # extract only date
    else:
        rawData = rawData[1:]
    year = int(rawData[7:])
    day = int(rawData[4:6])
    month = int(rawData[1:3])
    startTime, endTime = createStartAndEndTimes(timeString)
    startHour, startMinute = formatStartTime(startTime)
    endHour, endMinute = formatEndTime(endTime)
    startDT = dt(year, month, day, int(startHour), int(startMinute))
    endDT = dt(year, month, day, int(endHour), int(endMinute))
    startString = startDT.strftime('%Y%m%dT%H%M%S')
    endString = endDT.strftime('%Y%m%dT%H%M%S')
    return startString, endString
# TODO: find a way to automate the creation of all events for ONE class
courseNames = getCourseNames()
courseRanges = {}
# add 1 to final index value in order to account for exclusive nature of range(Start, Stop)
courseCodeRanges[len(courseCodeRanges) - 1] = courseCodeRanges[len(courseCodeRanges) - 1] + 1
for itrNum, course in enumerate(courseNames):
    courseRanges[course] = range(courseCodeRanges[itrNum], courseCodeRanges[itrNum + 1])

for course in courseRanges:
    #courseNamesItr += 1
    courseName = ''
    for row in courseRanges[course]:
        # col 3 = type information
        if finalDataset[row][3] == 'LE':
            rruleString = createRruleString(row)
            startWeekday = rEventDays(finalDataset[row][7])[0]
            startString, endString = rEventDTs(row, startWeekday)
            # add all field information the lecture event
            lecture = Event()
            lecture.name = finalDataset[row][0] + " Lecture"
            courseName = finalDataset[row][0]
            lecture.created = dt.now(pytz.utc)
            lecture.extra.append(ContentLine(name="RRULE", value=rruleString))
            lecture.extra.append(ContentLine("DTSTART", {'TZID': ['America/Los_Angeles']}, startString))
            lecture.extra.append(ContentLine("DTEND", {'TZID': ['America/Los_Angeles']}, endString))
            c.events.add(lecture)

        if finalDataset[row][3] == 'DI':
            rruleString = createRruleString(row)
            startWeekday = rEventDays(finalDataset[row][7])[0]
            startString, endString = rEventDTs(row, startWeekday)
            # add all field information the discussion event
            discussion = Event()
            discussion.name = courseName + " Discussion"
            discussion.created = dt.now(pytz.utc)
            discussion.extra.append(ContentLine(name="RRULE", value=rruleString))
            discussion.extra.append(ContentLine("DTSTART", {'TZID': ['America/Los_Angeles']}, startString))
            discussion.extra.append(ContentLine("DTEND", {'TZID': ['America/Los_Angeles']}, endString))
            c.events.add(discussion)

        if finalDataset[row][3] == 'MI' or finalDataset[row][3] == 'FI':
            testType = finalDataset[row][3]
            startString, endString = testDTs(row)
            test = Event()
            if testType == 'MI':
                test.name = courseName + " Midterm"
            elif testType == 'FI':
                test.name = courseName + " Final"
            test.created = dt.now(pytz.utc)
            test.extra.append(ContentLine("DTSTART", {'TZID': ['America/Los_Angeles']}, startString))
            test.extra.append(ContentLine("DTEND", {'TZID': ['America/Los_Angeles']}, endString))
            #print('These are all the tests: ' + test.serialize())
            c.events.add(test)

with open('dataParserOutput.ics', 'w') as outputFile:
        outputFile.writelines(c.serialize_iter())


