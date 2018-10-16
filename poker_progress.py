import os
import sys
import time
import csv
from datetime import datetime

def getDateTimeObject(dateTimeString):
	"""Receives a string in the form 'yyyy-mm-dd hh:mm' and returns
	a datetime object
	"""
	dateAndTimeData = dateTimeString.split()

	yearMonthDay = dateAndTimeData[0].split('-')
	yearMonthDay = list(int(item) for item in yearMonthDay)

	hourMinute = dateAndTimeData[1].split(':')
	hourMinute = list(int(item) for item in hourMinute)
	
	return datetime(*yearMonthDay, *hourMinute)

def getDayOfTheWeek(dateTimeString):
	"""Receives a string in the form 'yyyy-mm-dd hh:mm' and returns
	the day of the week in the form Mon, Tue, Wed, Thu, Fri, Sat or Sun
	"""
	daysOfWeek = {
				0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 
				4: "Fri", 5: "Sat", 6: "Sun"}

	dateAndTimeData = dateTimeString.split()

	yearMonthDay = dateAndTimeData[0].split('-')
	yearMonthDay = list(int(item) for item in yearMonthDay)

	date = datetime(*yearMonthDay)
	day = date.weekday()
	
	return daysOfWeek[day]


if __name__ == '__main__':
	try:
		fileName = sys.argv[1]
	except IndexError:
		print("Please enter a csv filename...")
		sys.exit()

	# Create the name of the output file
	filenameBase = os.path.splitext(fileName)[0]
	currentDate = datetime.now().strftime("%m%d%Y")
	currentTime = time.strftime("%I%M%S")
	outputFileName = filenameBase + '_processed_at_' + currentDate + '_' + currentTime + '.csv'

	try:
		with open(fileName) as inputcsvFile, open(outputFileName, 'w') as outputcsvFile:

			pokerReader = csv.reader(inputcsvFile)
			pokerWriter = csv.writer(outputcsvFile)

			for row in pokerReader:
				
				# insert columns named 'result', 'time_played' and 'hourly_rate' 
				if pokerReader.line_num == 2:
					row.insert(2, 'result')
					row.insert(4, 'start_day')
					row.insert(6, 'end_day')
					row.insert(7, 'time_played')
					row.insert(8, 'hourly_rate')
					pokerWriter.writerow(row)

				if pokerReader.line_num > 2:					
					# calculate the difference between buy in and cash out
					# and insert into the result column
					result = float(row[1]) - float(row[0])
					row.insert(2, str(result))
					
					# Calculate the start day and add to the start_day column
					start_day = getDayOfTheWeek(row[3])
					row.insert(4, start_day)

					# Calculate the end day and add to the end_day column
					end_day = getDayOfTheWeek(row[5])
					row.insert(6, end_day)

					# calculate the time played
					start = getDateTimeObject(row[3])
					end = getDateTimeObject(row[5])
					timeDiff = end - start
					hoursPlayed = timeDiff.seconds / 3600
					hoursPlayedString = format(hoursPlayed, '.2f')
					# and insert into the time played column
					row.insert(7, hoursPlayedString)

					# calculate the hourly rate 
					# and insert into the hourly rate column
					hourlyRate = result / hoursPlayed
					hourlyRateString = format(hourlyRate, '.2f')
					row.insert(8, hourlyRateString)


					# Write to file
					pokerWriter.writerow(row)

		print("Processed File saved to filename:", outputFileName)

					# if pokerReader.line_num > 2 and pokerReader.line_num <5:
					# 	print("start:", start)
					# 	print("end:", end)
					# 	timeDiff = end - start
					# 	print("Difference: ", timeDiff)
					# 	print("Row #" + str(pokerReader.line_num) + ": ", row)
					# 	print(dir(timeDiff))
					# 	print("timeDiff.days:", timeDiff.days)
					# 	print("timeDiff.seconds:", timeDiff.seconds)
					# 	print("timeDiff hour:", timeDiff.seconds / 3600)
					# 	hoursPlayed = timeDiff.seconds / 3600
					# 	hourlyRate = result / hoursPlayed
					# 	hourlyRate = format(hourlyRate, '.2f')
					# 	print("Hourly rate:", hourlyRate)
					# print("start day:", getDayOfTheWeek(row[3]))


	except FileNotFoundError:
		print("Cannot open file \'" + fileName + "\'.")
		print("Please check the filename and file location and try again.")
		# raise