import pandas as pd
from itertools import zip_longest
from datetime import datetime as dt, timedelta
from ics import Calendar, Event
import pytz
from pypdf import PdfReader
from ics.grammar.parse import ContentLine
from pdfminer.high_level import extract_text
from pdfminer.layout import LTTextBox, LTTextLine, LAParams, LTTextContainer
import re

def processFaultyPdf(reader):
    page = reader.pages[0]
    rawData = page.extract_text(extraction_mode="plain")
    rawRows = rawData.split('\n')
    del rawRows[1:19]
    # insert empty lines to emulate regular pdf input that has two rows for column labels
    rawRows.insert(1, '')
    rawRows.insert(1, '')
    # Extract text from the PDF page by page while preserving layout
    selectRows = []
    for row in rawRows:
        modRow = row.replace('LE', 'LE ')
        modRow = re.sub(r'(\d{1,2}:\d{2}[ap]-\d{1,2}:\d{2}[ap])', r'\1 ', modRow)
        modRow = re.sub(r'(\d{1,2}/\d{1,2}/\d{2},)', r'\n\1', modRow)
        modRow = re.sub(r'(Enrolled)', r' \1', modRow)
        selectRows.append(modRow)
    return selectRows

def dataParser(pdfFile):
    dayMap = {0: 'MO', 1: 'TU', 2: 'WE', 3: 'TH', 4: 'FR', 5: 'SA', 6: 'SU'}
    dayMapTwo = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}
    instructionStartEndDates = {'Summer Session II 2023': ('20230807', '20230908'), 'Fall Quarter 2023': ('20230928', '20231208'), 'Winter Quarter 2024': ('20240108', '20240315'), 'Spring Quarter 2024': ('20240401', '20240607'), 'Summer Session I 2024': ('20240701', '20240802'), 'Summer Session II 2024': ('20240805', '20240906'), 'Fall Quarter 2024': ('20240926', '20241206'), 'Winter Quarter 2025': ('20250106', '20250314'), 'Spring Quarter 2025': ('20250331', '20250606') }
    def printData(data):
        for row in data:
            print(row)
    # All the possible course codes at UCSD
    rawCourseCodes = ["AAPI", "AAS", "AESE", "AIP", "ANAR", "ANBI", "ANES", "ANSC", "ANTH", "ASTR", "AUD", "AWP", "BENG", "BGGN", "BGJC", "BGRD", "BGSE", "BIBC", "BICD", "BIEB", "BILD", "BIMM", "BIOM", "BIPN", "BISP", "BNFO", "CAT", "CCE", "CCS", "CENG", "CGS", "CHEM", "CHIN", "CLAS", "CLIN", "CLRE", "CLSS", "CLX", "CMM", "COGR", "COGS", "COMM", "CONT", "CSE", "CSS", "DDPM", "DERM", "DOC", "DSC", "DSE", "DSGN", "EAP", "ECE", "ECON", "EDS", "EIGH", "EMED", "ENG", "ENVR", "ERC", "ESYS", "ETHN", "ETIM", "EXPR", "FILM", "FMPH", "FPM", "GLBH", "GMST", "GPCO", "GPEC", "GPGN", "GPIM", "GPLA", "GPPA", "GPPS", "GSS", "HDP", "HDS", "HIAF", "HIEA", "HIEU", "HIGL", "HIGR", "HILA", "HILD", "HINE", "HISA", "HISC", "HITO", "HIUS", "HLAW", "HMNR", "HUM", "ICEP", "INTL", "IRLA", "JAPN", "JWSP", "LATI", "LAWS", "LHCO", "LIAB", "LIDS", "LIEO", "LIFR", "LIGM", "LIGN", "LIHI", "LIHL", "LIIT", "LIPO", "LISL", "LISP", "LTAF", "LTAM", "LTCH", "LTCO", "LTCS", "LTEA", "LTEN", "LTEU", "LTFR", "LTGK", "LTGM", "LTIT", "LTKO", "LTLA", "LTRU", "LTSP", "LTTH", "LTWL", "LTWR", "MAE", "MATH", "MATS", "MBC", "MCWP", "MDE", "MED", "MGT", "MGTA", "MGTF", "MGTP", "MMW", "MSED", "MSP", "MUIR", "MUS", "NANO", "NEU", "NEUG", "OBG", "OPTH", "ORTH", "PATH", "PEDS", "PH", "PHAR", "PHB", "PHIL", "PHLH", "PHYA", "PHYS", "POLI", "PSY", "PSYC", "RAD", "RELI", "REV", "RMAS", "RMED", "SE", "SEV", "SIO", "SIOB", "SIOC", "SIOG", "SOCE", "SOCG", "SOCI", "SOCL", "SOMC", "SOMI", "SPPH", "SPPS", "SURG", "SXTH", "SYN", "TDAC", "TDDE", "TDDM", "TDDR", "TDGE", "TDGR", "TDHD", "TDHT", "TDMV", "TDPF", "TDPR", "TDPW", "TDTR", "TKS", "TMC", "TWS", "UROL", "USP", "VIS", "WARR", "WCWP", "WES"]
    courseCodes = set(rawCourseCodes)
    reader = PdfReader(pdfFile)
    page = reader.pages[0]
    rawData = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=1)
    # rawRows is what my new func should replace
    rawRows = rawData.split('\n')

    # if data is faulty this termAndYearSearch will produce a bad key
    termAndYearRegex = r'-\s([A-Za-z\s\d]+)'
    termAndYearSearch = re.search(termAndYearRegex, rawRows[1])
    pdfTypeTwoFlag = False
    if termAndYearSearch == None:
        pdfTypeTwoFlag = True
        termAndYearSearch = re.search(termAndYearRegex, rawRows[0])
    termAndYear = termAndYearSearch.group(1)
    try:
        testIndex = instructionStartEndDates[termAndYear]
    except KeyError:
        # If bad key was produced use function to produce fixed rawRows data
        rawRows = processFaultyPdf(reader)


    # Determines if we have a schuedule with scheduling conflicts -> different row selections

    # Note we need a condition that handles a single and multiple conflicts
    schueduleConflictRegex = r'You have scheduling con.icts!|You have a scheduling con.ict!'
    conflictingSchuedPDF = False
    confSchuedIdx = None
    for idx, row in enumerate(rawRows):
        schueduleConflictSearch = re.search(schueduleConflictRegex, row)
        if schueduleConflictSearch:
            conflictingSchuedPDF = True
            confSchuedIdx = idx
            break
    # Now run the search again either with good data or fixed data
    termAndYearRegex = r'-\s([A-Za-z\s\d]+)'
    termAndYearSearch = re.search(termAndYearRegex, rawRows[1])
    # a type 2 pdf is one where the print time stamp is not included as the first line
    pdfTypeTwoFlag = False
    if termAndYearSearch == None:
        pdfTypeTwoFlag = True
        termAndYearSearch = re.search(termAndYearRegex, rawRows[0])

    termAndYear = termAndYearSearch.group(1)
    instructionStartYear = int((instructionStartEndDates[termAndYear][0])[:4])
    instructionStartMonth = int((instructionStartEndDates[termAndYear][0])[4:6])
    instructionStartDay = int((instructionStartEndDates[termAndYear][0])[6:])

    instructionEndYear = int((instructionStartEndDates[termAndYear][1])[:4])
    instructionEndMonth = int((instructionStartEndDates[termAndYear][1])[4:6])
    instructionEndDay = int((instructionStartEndDates[termAndYear][1])[6:])

    dtInstructionStart = dt(instructionStartYear, instructionStartMonth, instructionStartDay)
    instructionStartWeekday = dayMap[dtInstructionStart.weekday()]
    # Only select rows containing course and schuedule information

    # for the case when time stamp is not first row of pdf file
    if pdfTypeTwoFlag == True:
        start_index = 3
    else:
        start_index = 4
    # for the case where there are schueduling conflicts
    if conflictingSchuedPDF == True:
        end_index = confSchuedIdx
        selectRows = rawRows[start_index:end_index]
    else:
        # must also check if "act.ucsd.edu" is the last line, sometimes it's not
        websiteStampRegex = r'act.ucsd.edu'
        websiteStampSearch = re.search(websiteStampRegex, rawRows[-1])
        if websiteStampSearch == None:
            selectRows = rawRows[start_index:]
        else:
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

    subCourseRegex = r'[A-Z]{3,4}\s\d+[A-Z]{0,2}'
    titleRegex = ''
    secCodeRegex = r'\s[A-Z]\d{2}\s'
    typeRegex = r'LE\s|DI\s|MI\s|FI\s|LA\s'
    instructorRegex = r'\s[A-Z][a-z]+,\s[A-Z][a-z]+\s'
    gradeOpRegex = ''
    unitsRegex = ''
    # 1:MWF option  2:TuTh option  3:Test Dates Option  4:Single day M or W or F  5:Single day Tu or Th  6:Two of MWF option  7:SummerClass Option  8:TBA option
    #              [  1  ] [ 2 ][                      3                         ][                              4                        ][     5     ][   6     ][   7  ][8]                                         
    daysRegex = r'[MWF]{3}|TuTh|(\s[MWF]\s|\s(Tu|Th)\s|\sSa\s)\d{2}\/\d{2}\/\d{4}|(\s[MWF]\s+(?=\d{1,2}:\d{2}[ap]-\d{1,2}:\d{2}[ap]|\bTBA\b)|\s(Tu|Th)\s)|(MW|WF|MF)|MTuWThF|TBA'
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

    def getCourseNames():
        courseNames = []
        for index in courseCodeStartIndices:
            courseNames.append(finalDataset[index][0])
        return courseNames

    def printCsvFormat():        
        for row in finalDataset:
            print(row)

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
            # shaves off 'a' from time string
            timeToConvert = timeToConvert[:-1] 
            timeToConvert = timeToConvert + "AM"
        if timeToConvert[-1] == 'p':
            # shaves off 'p' from time string
            timeToConvert = timeToConvert[:-1] 
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
            # shave off 'a' for am start time classes
            endTime = endTime[:-1] 
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

    def startDayOffset(startWeekday):
        instructionStart = dayMapTwo[instructionStartWeekday]
        weekdayStart = dayMapTwo[startWeekday]
        dayDiff = (weekdayStart - instructionStart) % 7
        return dayDiff

    # create datetime strings for DTSTART and DTEND fields for recurring events
    # i.e. LE, DI, LA
    def rEventDTs(row, offset):
        timeString = finalDataset[row][8]
        startTime, endTime = createStartAndEndTimes(timeString)
        startHour, startMinute = formatStartTime(startTime)

        # dt() auto zero pads 
        dtStart = dt(instructionStartYear, instructionStartMonth, instructionStartDay, int(startHour), int(startMinute))
        dtStartOffset = dtStart + timedelta(days=offset)
        startString = dtStartOffset.strftime('%Y%m%dT%H%M%S')

        endHour, endMinute = formatEndTime(endTime)
        # to create LE, DI, LAB. Make first event last until instructionStart, THEN have it repeat until instructionEnd
        dtEnd = dt(instructionStartYear, instructionStartMonth, instructionStartDay, int(endHour), int(endMinute))
        dtEndOffset = dtEnd + timedelta(days=offset)
        endString = dtEndOffset.strftime('%Y%m%dT%H%M%S')
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
        if rawData[0] == "S" or rawData[0] == "T":
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
        #print(course)
        #courseNamesItr += 1
        courseName = ''
        for row in courseRanges[course]:
            # col 3 = type information
            if finalDataset[row][3] == 'LE':
                rruleString = createRruleString(row)
                minOffset = 100000
                for day in rEventDays(finalDataset[row][7]):
                    newOffset = startDayOffset(day)
                    if newOffset < minOffset:
                        minOffset = newOffset
                startString, endString = rEventDTs(row, minOffset)

                # add all field information the lecture event
                lecture = Event()
                # Only update courseName when we are looking at a new course, takes care of multiple lecture events being created for the same course
                if finalDataset[row][0] == '':
                    courseName = courseName
                else:
                    courseName = finalDataset[row][0]
                lecture.name = courseName + " Lecture"
                lecture.created = dt.now(pytz.utc)
                lecture.extra.append(ContentLine(name="RRULE", value=rruleString))
                lecture.extra.append(ContentLine("DTSTART", {'TZID': ['America/Los_Angeles']}, startString))
                lecture.extra.append(ContentLine("DTEND", {'TZID': ['America/Los_Angeles']}, endString))
                #print('These are all the lectures ' + lecture.serialize() + '\n')
                c.events.add(lecture)

            if finalDataset[row][3] == 'DI' or finalDataset[row][3] == 'LA':
                if finalDataset[row][7] == 'TBA':
                    continue
                recurrEventType = finalDataset[row][3]
                rruleString = createRruleString(row)
                minOffset = 100000
                for day in rEventDays(finalDataset[row][7]):
                    newOffset = startDayOffset(day)
                    if newOffset < minOffset:
                        minOffset = newOffset
                startString, endString = rEventDTs(row, minOffset)

                # add all field information the discussion event
                discussion = Event()
                if recurrEventType == 'DI':
                    discussion.name = courseName + " Discussion"
                elif recurrEventType == 'LA':
                    discussion.name = courseName + " Lab"
                discussion.created = dt.now(pytz.utc)
                discussion.extra.append(ContentLine(name="RRULE", value=rruleString))
                discussion.extra.append(ContentLine("DTSTART", {'TZID': ['America/Los_Angeles']}, startString))
                discussion.extra.append(ContentLine("DTEND", {'TZID': ['America/Los_Angeles']}, endString))
                #print('These are all the discussions or midterms: ' + discussion.serialize())
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
        
#dataParser('examplePDFs/iz.pdf')