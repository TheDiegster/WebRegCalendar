import pandas as pd
from datetime import datetime as dt
from ics import Calendar, Event
import pytz
from pypdf import PdfReader
from ics.grammar.parse import ContentLine
# All the possible course codes at UCSD
rawCourseCodes = ["AAPI", "AAS", "AESE", "AIP", "ANAR", "ANBI", "ANES", "ANSC", "ANTH", "ASTR", "AUD", "AWP", "BENG", "BGGN", "BGJC", "BGRD", "BGSE", "BIBC", "BICD", "BIEB", "BILD", "BIMM", "BIOM", "BIPN", "BISP", "BNFO", "CAT", "CCE", "CCS", "CENG", "CGS", "CHEM", "CHIN", "CLAS", "CLIN", "CLRE", "CLSS", "CLX", "CMM", "COGR", "COGS", "COMM", "CONT", "CSE", "CSS", "DDPM", "DERM", "DOC", "DSC", "DSE", "DSGN", "EAP", "ECE", "ECON", "EDS", "EIGH", "EMED", "ENG", "ENVR", "ERC", "ESYS", "ETHN", "ETIM", "EXPR", "FILM", "FMPH", "FPM", "GLBH", "GMST", "GPCO", "GPEC", "GPGN", "GPIM", "GPLA", "GPPA", "GPPS", "GSS", "HDP", "HDS", "HIAF", "HIEA", "HIEU", "HIGL", "HIGR", "HILA", "HILD", "HINE", "HISA", "HISC", "HITO", "HIUS", "HLAW", "HMNR", "HUM", "ICEP", "INTL", "IRLA", "JAPN", "JWSP", "LATI", "LAWS", "LHCO", "LIAB", "LIDS", "LIEO", "LIFR", "LIGM", "LIGN", "LIHI", "LIHL", "LIIT", "LIPO", "LISL", "LISP", "LTAF", "LTAM", "LTCH", "LTCO", "LTCS", "LTEA", "LTEN", "LTEU", "LTFR", "LTGK", "LTGM", "LTIT", "LTKO", "LTLA", "LTRU", "LTSP", "LTTH", "LTWL", "LTWR", "MAE", "MATH", "MATS", "MBC", "MCWP", "MDE", "MED", "MGT", "MGTA", "MGTF", "MGTP", "MMW", "MSED", "MSP", "MUIR", "MUS", "NANO", "NEU", "NEUG", "OBG", "OPTH", "ORTH", "PATH", "PEDS", "PH", "PHAR", "PHB", "PHIL", "PHLH", "PHYA", "PHYS", "POLI", "PSY", "PSYC", "RAD", "RELI", "REV", "RMAS", "RMED", "SE", "SEV", "SIO", "SIOB", "SIOC", "SIOG", "SOCE", "SOCG", "SOCI", "SOCL", "SOMC", "SOMI", "SPPH", "SPPS", "SURG", "SXTH", "SYN", "TDAC", "TDDE", "TDDM", "TDDR", "TDGE", "TDGR", "TDHD", "TDHT", "TDMV", "TDPF", "TDPR", "TDPW", "TDTR", "TKS", "TMC", "TWS", "UROL", "USP", "VIS", "WARR", "WCWP", "WES"]
courseCodes = set(rawCourseCodes)
#reader = PdfReader("webregMain.pdf")
reader = PdfReader("SI2classes.pdf")
page = reader.pages[0]
rawData = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=1)
newlineCount = rawData.count('\n')
rawRows = rawData.split('\n')

#print(rawData)
# Only select rows containing course and schuedule information
start_index = 4 #should be 4
end_index = -1
selectRows = rawRows[start_index:end_index]

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
courseCodeIndices = courseCodeStartIndices + [lastRowIdx]
with open('testOutput.txt', 'w') as file:
    for row in selectRows:
        print(row, file=file)
#cols = ["Subject Course", "Title", "Section Code", "Type", "Instructor", "Grade Option", "Units", "Days", "Time", "BLDG", "Room", "Status", "Action"]
finalFormattedRows = []
for row in selectRows:
    charCounter = 0
    currString = ''
    subjectCourse = ''
    title = ''
    sectionCode = ''
    type = ''
    instructor = ''
    gradeOption = ''
    units = ''
    time = ''
    days = ''
    building = ''
    room = ''
    status = ''
    action = ''
    for char in row:
        charCounter += 1
        if charCounter > 5 and charCounter < 18:
            subjectCourse += char
        if charCounter > 18 and charCounter < 53:
            title += char
        if charCounter > 52 and charCounter < 60:
            sectionCode += char
        if charCounter > 59 and charCounter < 62:
            type += char
        if charCounter > 63 and charCounter < 88:
            instructor += char
        if charCounter > 85 and charCounter < 92:
            gradeOption += char
        if charCounter > 91 and charCounter < 98:
            units += char
        if charCounter > 98 and charCounter < 115:
            days += char
        if charCounter > 114 and charCounter < 129:
            time += char
        if charCounter > 128 and charCounter < 135:
            building += char
        if charCounter > 135 and charCounter < 143:
            room += char
        if charCounter > 144 and charCounter <= len(selectRows):
            status += char
    cols = [subjectCourse, title, sectionCode, type, instructor, gradeOption, units, days, time, building, room, status]
    cleanCols = []
    for element in cols:
        cleanCols.append(element.strip())
    finalFormattedRows.append(cleanCols)


def getCourseNames():
    courseNames = []
    for index in courseCodeStartIndices:
        courseNames.append(finalFormattedRows[index][0])
    return courseNames

#print(getCourseNames())
def printCsvFormat():        
    for row in finalFormattedRows:
        print(row)

df = pd.DataFrame(finalFormattedRows)
printPdfFormat()
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
    # add a 0 in front of AM start times
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
def formatDays(days):
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
#lecture.name = finalFormattedRows[0][0] + " Lecture"


# create datetime strings for DTSTART and DTEND fields
def createDtStrings(row):
    timeString = finalFormattedRows[row][8]
    startTime, endTime = createStartAndEndTimes(timeString)
    startHour, startMinute = formatStartTime(startTime)
    # TODO: get the actual date creation parts of this function to another func
    # in order to be able to use for the creation of test dt object
    dtStart = dt(2024, 1, 8, int(startHour), int(startMinute))
    startString = dtStart.strftime('%Y%m%dT%H%M%S')
    endHour, endMinute = formatEndTime(endTime)
    dtEnd = dt(2024, 1, 8, int(endHour), int(endMinute))
    endString = dtEnd.strftime('%Y%m%dT%H%M%S')
    return startString, endString


def createRruleString(row):
    # create datetime string for UNTIL field, currently using hard coded end of
    # instruction date.
    untilDt = dt(2024, 3, 15, 23, 59)
    pacific = pytz.timezone("America/Los_Angeles")
    untilPacDt = pacific.localize(untilDt)
    untilUtcDt = untilPacDt.astimezone(pytz.utc)
    untilString = untilUtcDt.strftime('UNTIL=%Y%m%dT%H%M%SZ')

    # create string for the BYDAY field
    formattedDays = formatDays(finalFormattedRows[row][7])
    byDayString = ','.join(formattedDays)

    # create final rruleString
    rruleString = "FREQ=WEEKLY;" + untilString + ";WKST=" + "SU" + ";BYDAY=" + byDayString

    return rruleString

# INPUT: a row of course test (Midterm or Final) data
# OUTPUT: formatted start and end DT objects for tests
def testDTs(row):
    rawData = finalFormattedRows[row][7]
    timeString = finalFormattedRows[row][8]
    if rawData[0] == "S":
        rawData = rawData[2:]
    # extract only date
    else:
        rawData = rawData[1:]
    year = int(rawData[7:])
    day = int(rawData[4:6])
    month = int(rawData[1:3])
    # DTSTART;TZID=America/Los_Angeles:20240108T120000
    # DTEND;TZID=America/Los_Angeles:20240108T125000
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
courseCodeIndices[len(courseCodeIndices) - 1] = courseCodeIndices[len(courseCodeIndices) - 1] + 1
for itrNum, course in enumerate(courseNames):
    courseRanges[course] = range(courseCodeIndices[itrNum], courseCodeIndices[itrNum + 1])

for course in courseRanges:
    #courseNamesItr += 1
    courseName = ''
    for row in courseRanges[course]:
        # col 3 = type information
        if finalFormattedRows[row][3] == 'LE':
            startString, endString = createDtStrings(row)
            rruleString = createRruleString(row)
            # add all field information the lecture event
            lecture = Event()
            lecture.name = finalFormattedRows[row][0] + " Lecture"
            courseName = finalFormattedRows[row][0]
            lecture.created = dt.now(pytz.utc)
            lecture.extra.append(ContentLine(name="RRULE", value=rruleString))
            lecture.extra.append(ContentLine("DTSTART", {'TZID': ['America/Los_Angeles']}, startString))
            lecture.extra.append(ContentLine("DTEND", {'TZID': ['America/Los_Angeles']}, endString))
            c.events.add(lecture)

        if finalFormattedRows[row][3] == 'DI':
            startString, endString = createDtStrings(row)
            rruleString = createRruleString(row)
            # add all field information the discussion event
            discussion = Event()
            discussion.name = courseName + " Discussion"
            discussion.created = dt.now(pytz.utc)
            discussion.extra.append(ContentLine(name="RRULE", value=rruleString))
            discussion.extra.append(ContentLine("DTSTART", {'TZID': ['America/Los_Angeles']}, startString))
            discussion.extra.append(ContentLine("DTEND", {'TZID': ['America/Los_Angeles']}, endString))
            c.events.add(discussion)

        if finalFormattedRows[row][3] == 'MI' or finalFormattedRows[row][3] == 'FI':
            testType = finalFormattedRows[row][3]
            startString, endString = createDtStrings(row)
            startString, endString = testDTs(row)
            test = Event()
            if testType == 'MI':
                test.name = courseName + " Midterm"
            elif testType == 'FI':
                test.name = courseName + " Final"
            test.created = dt.now(pytz.utc)
            test.extra.append(ContentLine("DTSTART", {'TZID': ['America/Los_Angeles']}, startString))
            test.extra.append(ContentLine("DTEND", {'TZID': ['America/Los_Angeles']}, endString))
            print('These are all the tests: ' + test.serialize())
            c.events.add(test)
        #print(finalFormattedRows[row])


printPdfFormat()
with open('newOutput.ics', 'w') as outputFile:
        outputFile.writelines(c.serialize_iter())

