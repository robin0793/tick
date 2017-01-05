import datetime as dt
import time
import os
import tkinter as ui
import pyowm
import cal



path = os.path.dirname(os.path.realpath(__file__))
#os.system("export DISPLAY=:0.0")



class clock():

	def __init__(self):
		time = dt.datetime.now()
		
		self.alarmdb = []
		
		self.year = 1970
		self.month = 1
		self.day = 1
		self.hour = 0
		self.minute = 0
		self.second = 0
		self.weekday = 0
		self.week = 1
	
	def tick(self):

		time = dt.datetime.now()
		if time.minute != self.minute:

			for k in range(0,len(self.alarmdb)):
				if self.alarmdb[k][1] + dt.timedelta(minutes=self.alarmdb[k][2]) == time.replace(second=0, microsecond=0):

					del self.alarmdb[k]
					self.refresh(time)	
					return 2

			self.refresh(time)
			return 1
		return 0
			
	
	def build_db(self):
		time = dt.datetime.now()
		
		#delete old
		for alarm in range(0, len(self.alarmdb)):
			if self.alarmdb[alarm][1] + dt.timedelta(minutes=self.alarmdb[alarm][2])< time: del self.alarmdb[alarm]
	
		#read and add for next 48 hours
		f = open("{}/alarms".format(path), "r")
		alarms = f.readlines()
		for k in range(0,len(alarms)):
			if alarms[k][0] != "#":
				alarm_time = alarms[k].split()
				while len(alarm_time) < 6:
					alarm_time.append("*")
				
				for t_offset in range(0, 48):
					time_n = time + dt.timedelta(hours=t_offset)
					if self.chk(alarm_time[1], time_n.hour) and \
							self.chk(alarm_time[2], time_n.weekday()) and \
							self.chk(alarm_time[3], time_n.isocalendar()[1]) and \
							self.chk(alarm_time[4], time_n.day) and \
							self.chk(alarm_time[5], time_n.month):
						alarm_key=("{:02d}{:02d}{:02d}{:02d}".format(time_n.month, time_n.day, time_n.hour, int(alarm_time[0])))
						alarm_exists = False
						
						if t_offset == 0 and int(alarm_time[0]) <= time_n.minute: alarm_exists = True
						
						for u in range(0,len(self.alarmdb)):
							if self.alarmdb[u][0] == alarm_key:
								alarm_exists = True
								break
						if alarm_exists == False:
							alarm_name = ""
							if len(alarm_time) > 6:
								alarm_name = alarm_time[6]
							self.alarmdb.append([alarm_key, dt.datetime.strptime("{}{}".format(time_n.year, alarm_key), "%Y%m%d%H%M"), 3, alarm_name])
		
		self.alarmdb = sorted(self.alarmdb, key=lambda c: c[1])
		print(self.alarmdb)
			
	def refresh(self, time):
		
		self.year = time.year
		self.month = time.month
		self.day = time.day
		self.hour = time.hour
		self.minute = time.minute
		self.second = time.second
		self.weekday = time.weekday()
		self.week = time.isocalendar()[1]
		
	def chk(self, alarm, now):
		try:
			alarm_spt = alarm.split(",")
			for j in range(0,len(alarm_spt)):
				alarm = alarm_spt[j].replace("*",str(now))
				if "/" in alarm:
					alarm_div = alarm.split("/")
					alarm = float(alarm_div[0]) % float(alarm_div[1])
					return alarm == 0
				if alarm == "-1": 
					odd = now % 2
					return odd == 1
				if int(alarm) == now: return True
			
			return False
			
		except:
			return False
			
	def nextalarm(self):
		time = dt.datetime.now()
		time_end = dt.datetime.now()+dt.timedelta(hours=20)
		f = open("{}/alarms".format(path), "r")
		alarms = f.readlines()
		alarms_nexthours = []
		
		for k in range(0,len(alarms)):
			if alarms[k][0] != "#":
				alarm_time = alarms[k].split()
				while len(alarm_time) < 6:
					alarm_time.append("*")
				if len(alarm_time) < 7:
					alarm_time.append("Alarm")
				if time.minute >= int(alarm_time[0]):
					chk_range = range(1,21)
				else:
					chk_range = range(0,20)
					
				for h in chk_range:
					time_h = time + dt.timedelta(hours=h)
					if self.chk(alarm_time[1], time_h.hour) and \
							self.chk(alarm_time[2], time_h.weekday()) and \
							self.chk(alarm_time[3], time_h.isocalendar()[1]) and \
							self.chk(alarm_time[4], time_h.day) and \
							self.chk(alarm_time[5], time_h.month):
						alarms_nexthours.append(["alarms", "#FFFFFF", dt.datetime(time_h.year, time_h.month, time_h.day, time_h.hour, int(alarm_time[0])).timestamp(), 2, alarm_time[6].replace("_"," ")])
						#alarms_nexthours.append(["Alarm", "#000000", "{}:{}".format(time_h.hour, int(alarm_time[0])), 2, "Nächster Alarm"])
						
		
		return sorted(alarms_nexthours, key=lambda b: b[2])	
	

		
		
clk = clock()
clk.build_db()

root = ui.Tk()
root.minsize(width=800, height=480)
root.configure(background='black')
root.overrideredirect(1)

img_overlay = ui.PhotoImage(file="img/overlay.png")
img_weather = ui.PhotoImage(file="img/weather/02n.png")
img_temp = ui.PhotoImage(file="img/weather/temp.png")
img_cor = ui.PhotoImage(file="img/weather/cor.png")
img_calbg = ui.PhotoImage(file="img/cal/background.png")
img_cal_other = ui.PhotoImage(file="{}/img/cal/other.png".format(path))
img_cal_dyn = {}

color_font = "#FAFAFA"
color_bg1 = "#1C2327"
color_bg2 = "#36464D"

font = "Roboto"
font_light = "Roboto Light"



cnvs = ui.Canvas(root, width = 800, height = 480, highlightthickness=0)
cnvs.place(x=0, y=0, relwidth=1, relheight=1)

cnvs.create_rectangle(0, 0, 800, 480, fill=color_bg1)
#cnvs.create_image((0, 0), anchor="nw", image=img_bg)

#Uhrzeit
gui_hour = cnvs.create_text((150, 140), text="23", fill = color_font, font = (font, 130), anchor="center")
gui_min = cnvs.create_text((405, 140), text="0", fill = color_font, font = (font_light, 130), anchor="center")

#Termine
gui_cal_time=[0,0,0]
gui_cal_text=[0,0,0]
gui_cal_line=[0,0,0]
gui_cal_icon=[0,0,0]
#cnvs.create_image((486, 338), anchor="center", image=img_calbg)
gui_cal_time[0] = cnvs.create_text ((252, 337), text="", fill = color_font, font = (font, 22), anchor="w")
gui_cal_text[0] = cnvs.create_text ((335, 337), text="", fill = color_font, font = (font, 22), anchor="w")
gui_cal_line[0] = cnvs.create_rectangle(100, 354, 770, 358, fill=color_font, width=0)
gui_cal_icon[0] = cnvs.create_image((233, 339), anchor="center", image=img_cal_other)
#cnvs.create_image((486, 384), anchor="center", image=img_calbg)
gui_cal_time[1] = cnvs.create_text ((252, 383), text="", fill = color_font, font = (font, 22), anchor="w")
gui_cal_text[1] = cnvs.create_text ((335, 383), text="", fill = color_font, font = (font, 22), anchor="w")
gui_cal_line[1] = cnvs.create_rectangle(100, 400, 770, 404, fill=color_font, width=0)
gui_cal_icon[1] = cnvs.create_image((233, 385), anchor="center", image=img_cal_other)
#cnvs.create_image((486, 430), anchor="center", image=img_calbg)
gui_cal_time[2] = cnvs.create_text ((252, 429), text="", fill = color_font, font = (font, 22), anchor="w")
gui_cal_text[2] = cnvs.create_text ((335, 429), text="", fill = color_font, font = (font, 22), anchor="w")
gui_cal_line[2] = cnvs.create_rectangle(100, 446, 770, 450, fill=color_font, width=0)
gui_cal_icon[2] = cnvs.create_image((233, 431), anchor="center", image=img_cal_other)
cnvs.create_image((0, 0), anchor="nw", image=img_overlay)

#Wetter
cnvs.create_image((670, 100), anchor="center", image=img_weather)
cnvs.create_image((580, 210), anchor="center", image=img_temp)
gui_temp = cnvs.create_text ((596, 210), text="28°C", fill = color_font, font = (font, 22), anchor="w")
gui_wicon = cnvs.create_image((691, 210), anchor="center", image=img_cor)
gui_cor = cnvs.create_text ((710, 210), text="80%", fill = color_font, font = (font, 22), anchor="w")

#Calendar
gui_day = cnvs.create_text ((100, 365), text="20", fill = color_font, font = (font_light, 84), anchor="center")
gui_month = cnvs.create_text ((100, 430), text="NULL", fill = color_font, font = (font, 26), anchor="center")
cnvs.create_rectangle(188, 319, 188+3, 319+130, fill=color_font, width=0)
gui_cal_overlay = cnvs.create_rectangle(200, 460, 770, 460-100, fill=color_bg2, width=0)



#Open Weather Map
owm = pyowm.OWM("be3ff91c8c9a98d8bf457edcab0d2bc2")
loc_id = 2940397 #Callenberg

#Kalender
month_shortname = {1 : "JAN", 2 : "FEB", 3 : "MÄRZ", 4 : "APR", 5 : "MAI", 6 : "JUNI", 7 : "JULI", 8 : "AUG", 9 : "SEP", 10 : "OKT", 11 : "NOV", 12 : "DEZ"}
kal = cal.googlecal()

counter = 10

while 1:
	status = clk.tick()
	if status > 0:
		cnvs.itemconfig(gui_min, text = str(clk.minute).zfill(2))
		cnvs.itemconfig(gui_hour, text = str(clk.hour).zfill(2))
		cnvs.itemconfig(gui_day, text = str(clk.day).zfill(2))
		cnvs.itemconfig(gui_month, text = month_shortname[clk.month])
		
		counter += 1
	
	if counter >= 10: #Alle 10 Min...
		obs = owm.weather_at_id(loc_id)
		w = obs.get_weather()
		cnvs.itemconfig(gui_temp, text = "{}°C".format(round(w.get_temperature("celsius")["temp"]))) 
		#cnvs.itemconfig(gui_wicon, image = ui.PhotoImage(file="img/{}.png".format(w.get_weather_icon_name())))
		
		nextalarms = clk.nextalarm()
		
		termine = kal.nextevents()
		
		events = nextalarms + termine

		g = 0
		try: 
			events.remove([])
		except:
			pass
			
		events = sorted(events, key=lambda c: c[2])
		len_real = len(events)
		if len_real < 2: height_overlay = 100
		if len_real == 2: height_overlay = 50
		if len_real > 2: height_overlay = 0
		
		while len(events) < 4:
			events.append(["info", "#1c2327", 0, 0, "Keine weiteren Termine"])
		img_cal_dyn = {}				
		for d in range(0,3):
			if events[d][3] == 0:
				cnvs.coords(gui_cal_text[d],(252, 337+46*d))
				cnvs.itemconfig(gui_cal_text[d], text = "{}".format(events[d][4]))
				cnvs.itemconfig(gui_cal_time[d], text = "")
				
			else:
				cnvs.coords(gui_cal_text[d],(335, 337+46*d))
				cnvs.itemconfig(gui_cal_time[d], text = "{}".format(dt.datetime.fromtimestamp(events[d][2]).strftime('%H:%M')))
				
			cnvs.itemconfig(gui_cal_text[d], text = "{}".format(events[d][4]))
			cnvs.itemconfig(gui_cal_line[d], fill = events[d][1])
			
			if os.path.isfile("{}/img/cal/{}.png".format(path, events[d][0].lower())):
				img_cal_dyn[events[d][0].lower() + str(d)] = ui.PhotoImage(file="{}/img/cal/{}.png".format(path, events[d][0].lower()))
			else:
				img_cal_dyn[events[d][0].lower() + str(d)] = img_cal_other
			cnvs.itemconfig(gui_cal_icon[d], image=img_cal_dyn[events[d][0].lower() + str(d)])
				
		
		cnvs.coords(gui_cal_overlay, 200, 460, 770, 460-height_overlay)
	
		#cnvs.itemconfig(gui_cal3_time, text = "{}".format(dt.datetime.fromtimestamp(events[2][2]).strftime('%H:%M')), fill = events[2][1])
		
		counter = 0
		
	
	root.update_idletasks()
	root.update()
	time.sleep(0.5)
	