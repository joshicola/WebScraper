from datetime import datetime,timedelta

fl=open('Monday.html','r')
lines=fl.readlines()
fl.close()
line=lines[420]
daysOfWeek=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
fieldsOfInterest=['Time','Title','Instructor','Studio']
DaysSchedule={}
for day in daysOfWeek:
	DaysSchedule[day]=[]
	start=line.find('<div id="GXP'+day)
	end=line.find('<br style="clear: both;"></div></div>',start)
	startEntry=line.find("GXPEntry",start,end)
	while startEntry>0:
		GXPEntry={}
		for field in fieldsOfInterest:
			startItem=line.find('<div class="GXP'+field+'">',startEntry)
			endItem=line.find('</div>',startItem)
			Item=line[startItem+17+len(field):endItem]
			st=Item.find('<span')
			if st>0:
				Item=Item[:st-1]
			GXPEntry[field]=Item.replace('&nbsp;','')
		startEntry=line.find("GXPEntry",endItem,end)
		DaysSchedule[day].append(GXPEntry)
		
startDate=datetime.date(datetime(2018,04,01))
endDate=datetime.date(datetime(2018,05,01))

header='Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private,Recurring\n'
Studios=['Training Studio',
 'Multipurpose Studio',
 'Mind Body Studio']

for studio in Studios:
	fl=open(studio+'.csv','w')
	fl.write(header)

	CurrDate=startDate
	DD=timedelta(days=1)
	i=0
	while CurrDate<endDate:
		for GXPEntry in DaysSchedule[daysOfWeek[i%7]]:
			if GXPEntry['Studio']==studio:
				line=GXPEntry['Studio']+': '+GXPEntry['Title']+','
				line+=CurrDate.strftime('%m/%d/%Y')+','
				Time=GXPEntry['Time']
				Time=Time.replace('am',':00 AM').replace('pm',':00 PM')
				line+=Time[:Time.find('-')]+','
				line+=CurrDate.strftime('%m/%d/%Y')+','
				line+=Time[Time.find('-')+1:]+','
				line+='False,'
				line+=GXPEntry['Title']+':'+GXPEntry['Instructor']+':'+GXPEntry['Studio']+','
				line+=GXPEntry['Studio']+','
				line+='False,'
				line+='Y\n'
				fl.write(line)
	
		CurrDate+=DD
		i+=1
	

