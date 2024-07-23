import pandas as pd
from datetime import datetime as dt
from ics import Calendar, Event
import pytz
from pypdf import PdfReader
from ics.grammar.parse import ContentLine
# All the possible course codes at UCSD
rawCourseCodes = ["AAPI", "AAS", "AESE", "AIP", "ANAR", "ANBI", "ANES", "ANSC", "ANTH", "ASTR", "AUD", "AWP", "BENG", "BGGN", "BGJC", "BGRD", "BGSE", "BIBC", "BICD", "BIEB", "BILD", "BIMM", "BIOM", "BIPN", "BISP", "BNFO", "CAT", "CCE", "CCS", "CENG", "CGS", "CHEM", "CHIN", "CLAS", "CLIN", "CLRE", "CLSS", "CLX", "CMM", "COGR", "COGS", "COMM", "CONT", "CSE", "CSS", "DDPM", "DERM", "DOC", "DSC", "DSE", "DSGN", "EAP", "ECE", "ECON", "EDS", "EIGH", "EMED", "ENG", "ENVR", "ERC", "ESYS", "ETHN", "ETIM", "EXPR", "FILM", "FMPH", "FPM", "GLBH", "GMST", "GPCO", "GPEC", "GPGN", "GPIM", "GPLA", "GPPA", "GPPS", "GSS", "HDP", "HDS", "HIAF", "HIEA", "HIEU", "HIGL", "HIGR", "HILA", "HILD", "HINE", "HISA", "HISC", "HITO", "HIUS", "HLAW", "HMNR", "HUM", "ICEP", "INTL", "IRLA", "JAPN", "JWSP", "LATI", "LAWS", "LHCO", "LIAB", "LIDS", "LIEO", "LIFR", "LIGM", "LIGN", "LIHI", "LIHL", "LIIT", "LIPO", "LISL", "LISP", "LTAF", "LTAM", "LTCH", "LTCO", "LTCS", "LTEA", "LTEN", "LTEU", "LTFR", "LTGK", "LTGM", "LTIT", "LTKO", "LTLA", "LTRU", "LTSP", "LTTH", "LTWL", "LTWR", "MAE", "MATH", "MATS", "MBC", "MCWP", "MDE", "MED", "MGT", "MGTA", "MGTF", "MGTP", "MMW", "MSED", "MSP", "MUIR", "MUS", "NANO", "NEU", "NEUG", "OBG", "OPTH", "ORTH", "PATH", "PEDS", "PH", "PHAR", "PHB", "PHIL", "PHLH", "PHYA", "PHYS", "POLI", "PSY", "PSYC", "RAD", "RELI", "REV", "RMAS", "RMED", "SE", "SEV", "SIO", "SIOB", "SIOC", "SIOG", "SOCE", "SOCG", "SOCI", "SOCL", "SOMC", "SOMI", "SPPH", "SPPS", "SURG", "SXTH", "SYN", "TDAC", "TDDE", "TDDM", "TDDR", "TDGE", "TDGR", "TDHD", "TDHT", "TDMV", "TDPF", "TDPR", "TDPW", "TDTR", "TKS", "TMC", "TWS", "UROL", "USP", "VIS", "WARR", "WCWP", "WES"]
courseCodes = set(rawCourseCodes)
reader = PdfReader("webregMain.pdf")
page = reader.pages[0]
rawData = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=1)
newlineCount = rawData.count('\n')
rawRows = rawData.strip().split('\n')

# Only select rows containing course and schuedule information
start_index = 4
end_index = -1
selectRows = rawRows[start_index:end_index]

# for item in selectRows:
#     print(item)

noLeadSpaceRows = [row.strip() for row in selectRows]
cleanedRows = [' '.join(row.split()) for row in noLeadSpaceRows]
courseCodeStartingIndex = []
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
        courseCodeStartingIndex.append(idx)
    # Reset courseCode string to prepare for another check next iteration
    # if we didn't find it then we still have to reset it
    courseCode = ''

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
        
# for row in finalFormattedRows:
#     print(row)

df = pd.DataFrame(finalFormattedRows)

#print(df)

# Next Steps: Create a .ics file based on our dataframe or list of lists, use python ics lib

c = Calendar()
lecture = Event()
discussion = Event()
midtermOne = Event()
midtermTwo = Event()
# for test purposes let's create a MATH 20D calendar

lecture.name = finalFormattedRows[0][0] + " Lecture"

# will have to prompt user for beginning of instruction date
# for now use hard coded start and end days
# it seems UCSD updates class schuedule yearly so just do that
# for this example we have jan 3rd to march 15th 2024, prob put these in variables later
#e.begin = datetime(2023, 7, 20, 7, 0, 0, tzinfo=pytz.timezone("America/Los_Angeles"))
startTime = ''
endTime = ''
sawDash = False
timeString = finalFormattedRows[0][8]
for char in timeString:
    if sawDash == True:
        endTime += char
        continue
    if char == '-':
        sawDash = True
        continue
    startTime += char

def standardToMilitaryTime(timeToConvert):
    if timeToConvert[0] != 0:
        timeToConvert = "0" + timeToConvert
    if timeToConvert[-1] == 'a':
        timeToConvert = timeToConvert[:-1]
        timeToConvert = timeToConvert + "AM"
    if timeToConvert[-1] == 'p':
        timeToConvert = timeToConvert[:-1]
        timeToConvert = timeToConvert + "PM"
    standardTime = dt.strptime(timeToConvert, '%I:%M%p')
    militaryTime = standardTime.strftime('%H:%M')
    return militaryTime

startHour = ''
startMinute = ''
endHour = ''
endMinute = ''
if startTime[-1] == 'p':
    startTime = standardToMilitaryTime(startTime)
    startHour = startTime[:-3]
    startMinute = startTime[-2:]
else:
    startHour = startTime[:-4]
    startMinute = startTime[-2:]
if endTime[-1] == 'p':
    endTime = standardToMilitaryTime(endTime)
    endHour = endTime[:-3]
    endMinute = endTime[-2:]
else:
    endHour = endTime[:-4]
    endMinute = endTime[-2:]

#print("START " + startTime)
#print("END " + endTime)
startMinFirst = int(startMinute[0])
startMinSecond = int(startMinute[1])
endMinFirst = int(endMinute[0])
endMinSecond = int(endMinute[1])
#print("this is end minute: " + endMinute)
#lecture.begin = dt(2023, 7, 20, 9, 0, 0, tzinfo=pytz.timezone("America/Los_Angeles"))

def formatDays(days):
    formattedDays = []
    for char in days:
        if char == 'M':
            formattedDays.append('MO')
        elif char == 'Tu':
            formattedDays.append('TU')
        elif char == 'W':
            formattedDays.append('WE')   
        elif char == 'Th':
            formattedDays.append('TH')
        elif char == 'F':
            formattedDays.append('FR')
    return formattedDays

untilDt = dt(2024, 3, 15, 23, 59)
pacific = pytz.timezone("America/Los_Angeles")
untilPacDt = pacific.localize(untilDt)
untilUtcDt = untilPacDt.astimezone(pytz.utc)
untilString = untilUtcDt.strftime('UNTIL=%Y%m%dT%H%M%SZ')

formattedDays = formatDays(finalFormattedRows[0][7])
#print(formattedDays)
#lecture.begin = dt(2024, 1, 8, int(startHour), int(startMinute), tzinfo=pytz.timezone("America/Los_Angeles"))
dtStart = dt(2024, 1, 8, int(startHour), int(startMinute))
dtStartIcs = dtStart.strftime('%Y%m%dT%H%M%S')
dtEnd = dt(2024, 1, 8, int(endHour), int(endMinute))
dtEndIcs = dtEnd.strftime('%Y%m%dT%H%M%S')

dateToDay = dtStart.weekday()
daysOfTheWeek = ["MO","TU", "WE", "TH", "FR"]
startDay = daysOfTheWeek[dateToDay]
# we need to find a way to do repeat until!
# lecture.end = dt(2024, 1, 8, int(endHour), int(endMinute), tzinfo=pytz.timezone("America/Los_Angeles"))
# created sets DTSTAMP which is required
#print(lecture.end)
lecture.created = dt.now(pytz.utc)

byDayString = ','.join(formattedDays)
rruleString = "FREQ=WEEKLY;" + untilString + ";WKST=" + "SU" + ";BYDAY=" + byDayString
lecture.extra.append(ContentLine(name="RRULE", value=rruleString))



lecture.extra.append(ContentLine("DTSTART", {'TZID': ['America/Los_Angeles']}, dtStartIcs))
lecture.extra.append(ContentLine("DTEND", {'TZID': ['America/Los_Angeles']}, dtEndIcs))


# lecture.begin = '2014-01-01 00:00:00'
c.events.add(lecture)

with open('output.ics', 'w') as outputFile:
        outputFile.writelines(c.serialize_iter())



