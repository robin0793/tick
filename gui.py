import tkinter as ui


root = ui.Tk()
root.minsize(width=800, height=480)
root.configure(background='black')
root.overrideredirect(1)

img_overlay = ui.PhotoImage(file="img/overlay.png")
img_weather = ui.PhotoImage(file="img/weather/moon-clouds-thunder-01.png")
img_temp = ui.PhotoImage(file="img/weather/temp.png")
img_cor = ui.PhotoImage(file="img/weather/cor.png")
img_calbg = ui.PhotoImage(file="img/cal/background.png")

color_font = "#cfd8dc"
color_bg1 = "#1c2327"

font = "Roboto"
font_light = "Roboto Lt"



cnvs = ui.Canvas(root, width = 800, height = 480, highlightthickness=0)
cnvs.place(x=0, y=0, relwidth=1, relheight=1)

cnvs.create_rectangle(0, 0, 800, 480, fill=color_bg1)
#cnvs.create_image((0, 0), anchor="nw", image=img_bg)

#Uhrzeit
cnvs.create_text((150, 140), text="23", fill = color_font, font = (font_light, 130), anchor="center")
cnvs.create_text((405, 140), text="36", fill = color_font, font = (font_light, 130), anchor="center")

cnvs.create_image((0, 0), anchor="nw", image=img_overlay)

#Wetter
cnvs.create_image((670, 100), anchor="center", image=img_weather)
cnvs.create_image((580, 210), anchor="center", image=img_temp)
cnvs.create_text ((596, 210), text="28°C", fill = color_font, font = (font, 22), anchor="w")
cnvs.create_image((691, 210), anchor="center", image=img_cor)
cnvs.create_text ((710, 210), text="80%", fill = color_font, font = (font, 22), anchor="w")

#Calendar
cnvs.create_text ((100, 365), text="20", fill = color_font, font = (font_light, 87), anchor="center")
cnvs.create_text ((100, 430), text="NOV", fill = color_font, font = (font, 26), anchor="center")
cnvs.create_rectangle(188, 319, 188+3, 319+130, fill=color_font, width=0)

cnvs.create_image((486, 338), anchor="center", image=img_calbg)
cnvs.create_image((486, 384), anchor="center", image=img_calbg)
cnvs.create_image((486, 430), anchor="center", image=img_calbg)


root.mainloop()
