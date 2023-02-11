from tkinter import *
from tkinter import ttk
from configparser import ConfigParser
import requests
from tkinter import messagebox
import PIL.ImageTk as ptk

class Application:
    def __init__(self,root):
        self.url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
        self.config_file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_file)
        self.api_key = self.config['api_key']['key']

        self.root=root
        self.root.title('Weather Live')
        self.root.minsize(1280,632)

        self.background=ptk.PhotoImage(file='pictures/home.jpg')
        self.background_label=ttk.Label(image=self.background)
        self.background_label.image=self.background
        self.background_label.place(x=0,y=0)
        
        self.city_var = StringVar() 

        self.welcome = ttk.Label(root,text='Welcome to Weather Live',font='helvetica 25',foreground='green')
        self.welcome.pack()

        self.search_label = ttk.Label(root,text='Please enter a city to search',font='helvetica 10',foreground='blue')
        self.search_label.pack()
        
        self.city_entry = ttk.Entry(root,textvariable=self.city_var)
        self.city_entry.pack(pady=5)

        self.searchimg = ptk.PhotoImage(file='buttons/searchbutton.png')
        self.searchimg_label = ttk.Label(root,image=self.searchimg)
        self.searchbtn = Button(root,image=self.searchimg,command=self.search,borderwidth=0)
        self.searchbtn.pack()

    def get_weather(self,city):
        self.result = requests.get(self.url.format(city,self.api_key))
        if self.result:
            self.json = self.result.json()
            self.city = self.json['name']
            self.country = self.json['sys']['country']
            self.temp_kelvin = self.json['main']['temp']
            self.temp_celsius = self.temp_kelvin - 273.15
            self.temp_fahrenheit = (self.temp_kelvin-273.15)*9/5+32
            self.icon = self.json['weather'][0]['icon']
            self.weather = self.json['weather'][0]['main']
            self.feelslikecelsius = self.json['main']['feels_like']-273.15
            self.humidity = self.json['main']['humidity']
            self.pressure = self.json['main']['pressure']
            self.visibility = self.json['visibility']
            self.windspeed = self.json['wind']['speed']
            self.final = (self.city,self.country,self.temp_celsius,self.temp_fahrenheit,self.icon,self.weather,self.feelslikecelsius,self.humidity,self.pressure,self.visibility,self.windspeed)
            return self.final
        else:
            return None

    def retourner(self):
        root.deiconify()
        self.new.destroy()

    def search(self):
        self.city = self.city_var.get()
        self.weather = self.get_weather(self.city)

        if self.weather:
            if self.weather[4] == '01d':
                self.new=Toplevel()
                self.new.minsize(1280,632)
                self.new.protocol('WM_DELETE_WINDOW',self.retourner)
                self.background_clearday=ptk.PhotoImage(file='pictures/clearday.png')
                self.background_label_clearday=ttk.Label(self.new,image=self.background_clearday)
                self.background_label_clearday.place(x=0,y=0)
                self.location_label = ttk.Label(self.new,text='',font='bold 20',background='cyan')
                self.location_label.pack(pady=10)
                self.temp_labelcelsius = ttk.Label(self.new,text='',font='helvetica 50',background='cyan')
                self.temp_labelcelsius.pack(pady= 20)
                self.feelslike = ttk.Label(self.new,text='',font='helvetica 20',background='cyan')
                self.feelslike.pack()
                self.weather_label = ttk.Label(self.new,text='',font='helvetica 20',background='cyan')
                self.weather_label.pack(pady = 20)
                self.humiditylabel = ttk.Label(self.new,text='',font='helvetica 20',background='cyan')
                self.humiditylabel.pack()
                self.pressurelabel = ttk.Label(self.new,text='',font='helvetica 20',background='cyan')
                self.pressurelabel.pack(pady = 20)
                self.visibilitylabel = ttk.Label(self.new,text='',font='helvetica 20',background='cyan')
                self.visibilitylabel.pack()
                self.windspeedlabel = ttk.Label(self.new,text='',font='helvetica 20',background='cyan')
                self.windspeedlabel.pack(pady=20)
                self.backimg = ptk.PhotoImage(file='buttons/backbutton.jpg')
                self.backimg_label = ttk.Label(self.new,image=self.backimg)
                self.backbtn = Button(self.new,image=self.backimg,command=self.retourner,borderwidth=0)
                self.backbtn.pack()
                self.location_label['text'] = '{}, {}'.format(self.weather[0],self.weather[1]) 
                self.temp_labelcelsius['text'] = '{:.2f}°C'.format(self.weather[2])
                self.feelslike['text'] = 'feels like '+'{:.2f}°C'.format(self.weather[6])
                self.weather_label['text'] = self.weather[5]
                self.humiditylabel['text'] = 'humidity: '+str(self.weather[7])+'%'
                self.pressurelabel['text'] = 'pressure: '+ str(self.weather[8])+' mBar'
                self.visibilitylabel['text']='visibility: '+str(self.weather[9]/1000)+' km'
                self.windspeedlabel['text'] = 'wind speed: '+str(self.weather[10])+' m/s'
                root.withdraw()
            elif self.weather[4] == '01n':
                self.new=Toplevel()
                self.new.minsize(1280,632)
                self.new.protocol('WM_DELETE_WINDOW',self.retourner)
                self.background_clearnight=ptk.PhotoImage(file='pictures/clearnight.png')
                self.background_label_clearnight=ttk.Label(self.new,image=self.background_clearnight)
                self.background_label_clearnight.place(x=0,y=0)
                self.location_label = ttk.Label(self.new,text='',font='bold 20',background='blue',foreground='white')
                self.location_label.pack(pady=10)
                self.temp_labelcelsius = ttk.Label(self.new,text='',font='helvetica 50',background='blue',foreground='white')
                self.temp_labelcelsius.pack(pady= 20)
                self.feelslike = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.feelslike.pack()
                self.weather_label = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.weather_label.pack(pady = 20)
                self.humiditylabel = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.humiditylabel.pack()
                self.pressurelabel = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.pressurelabel.pack(pady = 20)
                self.visibilitylabel = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.visibilitylabel.pack()
                self.windspeedlabel = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.windspeedlabel.pack(pady=20)
                self.backimg = ptk.PhotoImage(file='buttons/backbutton.jpg')
                self.backimg_label = ttk.Label(self.new,image=self.backimg)
                self.backbtn = Button(self.new,image=self.backimg,command=self.retourner,borderwidth=0)
                self.backbtn.pack()
                self.location_label['text'] = '{}, {}'.format(self.weather[0],self.weather[1]) 
                self.temp_labelcelsius['text'] = '{:.2f}°C'.format(self.weather[2])
                self.feelslike['text'] = 'feels like '+'{:.2f}°C'.format(self.weather[6])
                self.weather_label['text'] = self.weather[5]
                self.humiditylabel['text'] = 'humidity: '+str(self.weather[7])+'%'
                self.pressurelabel['text'] = 'pressure: '+ str(self.weather[8])+' mBar'
                self.visibilitylabel['text']='visibility: '+str(self.weather[9]/1000)+' km'
                self.windspeedlabel['text'] = 'wind speed: '+str(self.weather[10])+' m/s'
                root.withdraw()
            elif self.weather[4] == '02d' or self.weather[4]== '03d' or self.weather[4]=='04d':
                self.new=Toplevel()
                self.new.minsize(1280,632)
                self.new.protocol('WM_DELETE_WINDOW',self.retourner)
                self.background_cloudyday=ptk.PhotoImage(file='pictures/cloudyday.jpg')
                self.background_label_cloudyday=ttk.Label(self.new,image=self.background_cloudyday)
                self.background_label_cloudyday.place(x=0,y=0)
                self.location_label = ttk.Label(self.new,text='',font='bold 20',background='grey',foreground='white')
                self.location_label.pack(pady=10)
                self.temp_labelcelsius = ttk.Label(self.new,text='',font='helvetica 50',background='grey',foreground='white')
                self.temp_labelcelsius.pack(pady= 20)
                self.feelslike = ttk.Label(self.new,text='',font='helvetica 20',background='grey',foreground='white')
                self.feelslike.pack()
                self.weather_label = ttk.Label(self.new,text='',font='helvetica 20',background='grey',foreground='white')
                self.weather_label.pack(pady = 20)
                self.humiditylabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey',foreground='white')
                self.humiditylabel.pack()
                self.pressurelabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey',foreground='white')
                self.pressurelabel.pack(pady = 20)
                self.visibilitylabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey',foreground='white')
                self.visibilitylabel.pack()
                self.windspeedlabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey',foreground='white')
                self.windspeedlabel.pack(pady=20)
                self.backimg = ptk.PhotoImage(file='buttons/backbutton.jpg')
                self.backimg_label = ttk.Label(self.new,image=self.backimg)
                self.backbtn = Button(self.new,image=self.backimg,command=self.retourner,borderwidth=0)
                self.backbtn.pack()
                self.location_label['text'] = '{}, {}'.format(self.weather[0],self.weather[1]) 
                self.temp_labelcelsius['text'] = '{:.2f}°C'.format(self.weather[2])
                self.feelslike['text'] = 'feels like '+'{:.2f}°C'.format(self.weather[6])
                self.weather_label['text'] = self.weather[5]
                self.humiditylabel['text'] = 'humidity: '+str(self.weather[7])+'%'
                self.pressurelabel['text'] = 'pressure: '+ str(self.weather[8])+' mBar'
                self.visibilitylabel['text']='visibility: '+str(self.weather[9]/1000)+' km'
                self.windspeedlabel['text'] = 'wind speed: '+str(self.weather[10])+' m/s'
                root.withdraw()
            elif self.weather[4] == '02n' or self.weather[4]== '03n' or self.weather[4]=='04n':
                self.new=Toplevel()
                self.new.minsize(1280,632)
                self.new.protocol('WM_DELETE_WINDOW',self.retourner)
                self.background_cloudynight=ptk.PhotoImage(file='pictures/cloudynight.jpg')
                self.background_label_cloudynight=ttk.Label(self.new,image=self.background_cloudynight)
                self.background_label_cloudynight.place(x=0,y=0)
                self.location_label = ttk.Label(self.new,text='',font='bold 20',background='grey')
                self.location_label.pack(pady=10)
                self.temp_labelcelsius = ttk.Label(self.new,text='',font='helvetica 50',background='grey')
                self.temp_labelcelsius.pack(pady= 20)
                self.feelslike = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.feelslike.pack()
                self.weather_label = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.weather_label.pack(pady = 20)
                self.humiditylabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.humiditylabel.pack()
                self.pressurelabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.pressurelabel.pack(pady = 20)
                self.visibilitylabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.visibilitylabel.pack()
                self.windspeedlabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.windspeedlabel.pack(pady=20)
                self.backimg = ptk.PhotoImage(file='buttons/backbutton.jpg')
                self.backimg_label = ttk.Label(self.new,image=self.backimg)
                self.backbtn = Button(self.new,image=self.backimg,command=self.retourner,borderwidth=0)
                self.backbtn.pack()
                self.location_label['text'] = '{}, {}'.format(self.weather[0],self.weather[1]) 
                self.temp_labelcelsius['text'] = '{:.2f}°C'.format(self.weather[2])
                self.feelslike['text'] = 'feels like '+'{:.2f}°C'.format(self.weather[6])
                self.weather_label['text'] = self.weather[5]
                self.humiditylabel['text'] = 'humidity: '+str(self.weather[7])+'%'
                self.pressurelabel['text'] = 'pressure: '+ str(self.weather[8])+' mBar'
                self.visibilitylabel['text']='visibility: '+str(self.weather[9]/1000)+' km'
                self.windspeedlabel['text'] = 'wind speed: '+str(self.weather[10])+' m/s'
                root.withdraw()
            elif self.weather[4] == '09d' or self.weather[4]== '10d' or self.weather[4]=='11d':
                self.new=Toplevel()
                self.new.minsize(1280,632)
                self.new.protocol('WM_DELETE_WINDOW',self.retourner)
                self.background_rainyday=ptk.PhotoImage(file='pictures/rainyday.jpg')
                self.background_label_rainyday=ttk.Label(self.new,image=self.background_rainyday)
                self.background_label_rainyday.place(x=0,y=0)
                self.location_label = ttk.Label(self.new,text='',font='bold 20',background='dark green',foreground='black')
                self.location_label.pack(pady=10)
                self.temp_labelcelsius = ttk.Label(self.new,text='',font='helvetica 50',background='dark green',foreground='black')
                self.temp_labelcelsius.pack(pady= 20)
                self.feelslike = ttk.Label(self.new,text='',font='helvetica 20',background='dark green',foreground='black')
                self.feelslike.pack()
                self.weather_label = ttk.Label(self.new,text='',font='helvetica 20',background='dark green',foreground='black')
                self.weather_label.pack(pady = 20)
                self.humiditylabel = ttk.Label(self.new,text='',font='helvetica 20',background='dark green',foreground='black')
                self.humiditylabel.pack()
                self.pressurelabel = ttk.Label(self.new,text='',font='helvetica 20',background='dark green',foreground='black')
                self.pressurelabel.pack(pady = 20)
                self.visibilitylabel = ttk.Label(self.new,text='',font='helvetica 20',background='dark green',foreground='black')
                self.visibilitylabel.pack()
                self.windspeedlabel = ttk.Label(self.new,text='',font='helvetica 20',background='dark green',foreground='black')
                self.windspeedlabel.pack(pady=20)
                self.backimg = ptk.PhotoImage(file='buttons/backbutton.jpg')
                self.backimg_label = ttk.Label(self.new,image=self.backimg)
                self.backbtn = Button(self.new,image=self.backimg,command=self.retourner,borderwidth=0)
                self.backbtn.pack()
                self.location_label['text'] = '{}, {}'.format(self.weather[0],self.weather[1]) 
                self.temp_labelcelsius['text'] = '{:.2f}°C'.format(self.weather[2])
                self.feelslike['text'] = 'feels like '+'{:.2f}°C'.format(self.weather[6])
                self.weather_label['text'] = self.weather[5]
                self.humiditylabel['text'] = 'humidity: '+str(self.weather[7])+'%'
                self.pressurelabel['text'] = 'pressure: '+ str(self.weather[8])+' mBar'
                self.visibilitylabel['text']='visibility: '+str(self.weather[9]/1000)+' km'
                self.windspeedlabel['text'] = 'wind speed: '+str(self.weather[10])+' m/s'
                root.withdraw()
            elif self.weather[4] == '09n' or self.weather[4]== '10n' or self.weather[4]=='11n':
                self.new=Toplevel()
                self.new.minsize(1280,632)
                self.new.protocol('WM_DELETE_WINDOW',self.retourner)
                self.background_rainynight=ptk.PhotoImage(file='pictures/rainynight.jpg')
                self.background_label_rainynight=ttk.Label(self.new,image=self.background_rainynight)
                self.background_label_rainynight.place(x=0,y=0)
                self.location_label = ttk.Label(self.new,text='',font='bold 20',background='light blue')
                self.location_label.pack(pady=10)
                self.temp_labelcelsius = ttk.Label(self.new,text='',font='helvetica 50',background='light blue')
                self.temp_labelcelsius.pack(pady= 20)
                self.feelslike = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.feelslike.pack()
                self.weather_label = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.weather_label.pack(pady = 20)
                self.humiditylabel = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.humiditylabel.pack()
                self.pressurelabel = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.pressurelabel.pack(pady = 20)
                self.visibilitylabel = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.visibilitylabel.pack()
                self.windspeedlabel = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.windspeedlabel.pack(pady=20)
                self.backimg = ptk.PhotoImage(file='buttons/backbutton.jpg')
                self.backimg_label = ttk.Label(self.new,image=self.backimg)
                self.backbtn = Button(self.new,image=self.backimg,command=self.retourner,borderwidth=0)
                self.backbtn.pack()
                self.location_label['text'] = '{}, {}'.format(self.weather[0],self.weather[1]) 
                self.temp_labelcelsius['text'] = '{:.2f}°C'.format(self.weather[2])
                self.feelslike['text'] = 'feels like '+'{:.2f}°C'.format(self.weather[6])
                self.weather_label['text'] = self.weather[5]
                self.humiditylabel['text'] = 'humidity: '+str(self.weather[7])+'%'
                self.pressurelabel['text'] = 'pressure: '+ str(self.weather[8])+' mBar'
                self.visibilitylabel['text']='visibility: '+str(self.weather[9]/1000)+' km'
                self.windspeedlabel['text'] = 'wind speed: '+str(self.weather[10])+' m/s'
                root.withdraw()
            elif self.weather[4] == '13d':
                self.new=Toplevel()
                self.new.minsize(1280,632)
                self.new.protocol('WM_DELETE_WINDOW',self.retourner)
                self.background_snowyday=ptk.PhotoImage(file='pictures/snowyday.jpg')
                self.background_label_snowyday=ttk.Label(self.new,image=self.background_snowyday)
                self.background_label_snowyday.place(x=0,y=0)
                self.location_label = ttk.Label(self.new,text='',font='bold 20',background='light blue')
                self.location_label.pack(pady=10)
                self.temp_labelcelsius = ttk.Label(self.new,text='',font='helvetica 50',background='light blue')
                self.temp_labelcelsius.pack(pady= 20)
                self.feelslike = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.feelslike.pack()
                self.weather_label = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.weather_label.pack(pady = 20)
                self.humiditylabel = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.humiditylabel.pack()
                self.pressurelabel = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.pressurelabel.pack(pady = 20)
                self.visibilitylabel = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.visibilitylabel.pack()
                self.windspeedlabel = ttk.Label(self.new,text='',font='helvetica 20',background='light blue')
                self.windspeedlabel.pack(pady=20)
                self.backimg = ptk.PhotoImage(file='buttons/backbutton.jpg')
                self.backimg_label = ttk.Label(self.new,image=self.backimg)
                self.backbtn = Button(self.new,image=self.backimg,command=self.retourner,borderwidth=0)
                self.backbtn.pack()
                self.location_label['text'] = '{}, {}'.format(self.weather[0],self.weather[1]) 
                self.temp_labelcelsius['text'] = '{:.2f}°C'.format(self.weather[2])
                self.feelslike['text'] = 'feels like '+'{:.2f}°C'.format(self.weather[6])
                self.weather_label['text'] = self.weather[5]
                self.humiditylabel['text'] = 'humidity: '+str(self.weather[7])+'%'
                self.pressurelabel['text'] = 'pressure: '+ str(self.weather[8])+' mBar'
                self.visibilitylabel['text']='visibility: '+str(self.weather[9]/1000)+' km'
                self.windspeedlabel['text'] = 'wind speed: '+str(self.weather[10])+' m/s'
                root.withdraw()
            elif self.weather[4] == '13n':
                self.new=Toplevel()
                self.new.minsize(1280,632)
                self.new.protocol('WM_DELETE_WINDOW',self.retourner)
                self.background_snowynight=ptk.PhotoImage(file='pictures/snowynight.jpg')
                self.background_label_snowynight=ttk.Label(self.new,image=self.background_snowynight)
                self.background_label_snowynight.place(x=0,y=0)
                self.location_label = ttk.Label(self.new,text='',font='bold 20',background='blue',foreground='white')
                self.location_label.pack(pady=10)
                self.temp_labelcelsius = ttk.Label(self.new,text='',font='helvetica 50',background='blue',foreground='white')
                self.temp_labelcelsius.pack(pady= 20)
                self.feelslike = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.feelslike.pack()
                self.weather_label = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.weather_label.pack(pady = 20)
                self.humiditylabel = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.humiditylabel.pack()
                self.pressurelabel = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.pressurelabel.pack(pady = 20)
                self.visibilitylabel = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.visibilitylabel.pack()
                self.windspeedlabel = ttk.Label(self.new,text='',font='helvetica 20',background='blue',foreground='white')
                self.windspeedlabel.pack(pady=20)
                self.backimg = ptk.PhotoImage(file='buttons/backbutton.jpg')
                self.backimg_label = ttk.Label(self.new,image=self.backimg)
                self.backbtn = Button(self.new,image=self.backimg,command=self.retourner,borderwidth=0)
                self.backbtn.pack()
                self.location_label['text'] = '{}, {}'.format(self.weather[0],self.weather[1]) 
                self.temp_labelcelsius['text'] = '{:.2f}°C'.format(self.weather[2])
                self.feelslike['text'] = 'feels like '+'{:.2f}°C'.format(self.weather[6])
                self.weather_label['text'] = self.weather[5]
                self.humiditylabel['text'] = 'humidity: '+str(self.weather[7])+'%'
                self.pressurelabel['text'] = 'pressure: '+ str(self.weather[8])+' mBar'
                self.visibilitylabel['text']='visibility: '+str(self.weather[9]/1000)+' km'
                self.windspeedlabel['text'] = 'wind speed: '+str(self.weather[10])+' m/s'
                root.withdraw()
            elif self.weather[4] == '50d':
                self.new=Toplevel()
                self.new.minsize(1280,632)
                self.new.protocol('WM_DELETE_WINDOW',self.retourner)
                self.background_foggyday=ptk.PhotoImage(file='pictures/foggyday.jpg')
                self.background_label_foggyday=ttk.Label(self.new,image=self.background_foggyday)
                self.background_label_foggyday.place(x=0,y=0)
                self.location_label = ttk.Label(self.new,text='',font='bold 20',background='grey')
                self.location_label.pack(pady=10)
                self.temp_labelcelsius = ttk.Label(self.new,text='',font='helvetica 50',background='grey')
                self.temp_labelcelsius.pack(pady= 20)
                self.feelslike = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.feelslike.pack()
                self.weather_label = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.weather_label.pack(pady = 20)
                self.humiditylabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.humiditylabel.pack()
                self.pressurelabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.pressurelabel.pack(pady = 20)
                self.visibilitylabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.visibilitylabel.pack()
                self.windspeedlabel = ttk.Label(self.new,text='',font='helvetica 20',background='grey')
                self.windspeedlabel.pack(pady=20)
                self.backimg = ptk.PhotoImage(file='buttons/backbutton.jpg')
                self.backimg_label = ttk.Label(self.new,image=self.backimg)
                self.backbtn = Button(self.new,image=self.backimg,command=self.retourner,borderwidth=0)
                self.backbtn.pack()
                self.location_label['text'] = '{}, {}'.format(self.weather[0],self.weather[1]) 
                self.temp_labelcelsius['text'] = '{:.2f}°C'.format(self.weather[2])
                self.feelslike['text'] = 'feels like '+'{:.2f}°C'.format(self.weather[6])
                self.weather_label['text'] = self.weather[5]
                self.humiditylabel['text'] = 'humidity: '+str(self.weather[7])+'%'
                self.pressurelabel['text'] = 'pressure: '+ str(self.weather[8])+' mBar'
                self.visibilitylabel['text']='visibility: '+str(self.weather[9]/1000)+' km'
                self.windspeedlabel['text'] = 'wind speed: '+str(self.weather[10])+' m/s'
                root.withdraw()
            elif self.weather[4] == '50n':
                self.new=Toplevel()
                self.new.minsize(1280,632)
                self.new.protocol('WM_DELETE_WINDOW',self.retourner)
                self.background_foggynight=ptk.PhotoImage(file='pictures/foggynight.jpg')
                self.background_label_foggynight=ttk.Label(self.new,image=self.background_foggynight)
                self.background_label_foggynight.place(x=0,y=0)
                self.location_label = ttk.Label(self.new,text='',font='bold 20',background='yellow')
                self.location_label.pack(pady=10)
                self.temp_labelcelsius = ttk.Label(self.new,text='',font='helvetica 50',background='yellow')
                self.temp_labelcelsius.pack(pady= 20)
                self.feelslike = ttk.Label(self.new,text='',font='helvetica 20',background='yellow')
                self.feelslike.pack()
                self.weather_label = ttk.Label(self.new,text='',font='helvetica 20',background='yellow')
                self.weather_label.pack(pady = 20)
                self.humiditylabel = ttk.Label(self.new,text='',font='helvetica 20',background='yellow')
                self.humiditylabel.pack()
                self.pressurelabel = ttk.Label(self.new,text='',font='helvetica 20',background='yellow')
                self.pressurelabel.pack(pady = 20)
                self.visibilitylabel = ttk.Label(self.new,text='',font='helvetica 20',background='yellow')
                self.visibilitylabel.pack()
                self.windspeedlabel = ttk.Label(self.new,text='',font='helvetica 20',background='yellow')
                self.windspeedlabel.pack(pady=20)
                self.backimg = ptk.PhotoImage(file='buttons/backbutton.jpg')
                self.backimg_label = ttk.Label(self.new,image=self.backimg)
                self.backbtn = Button(self.new,image=self.backimg,command=self.retourner,borderwidth=0)
                self.backbtn.pack()
                self.location_label['text'] = '{}, {}'.format(self.weather[0],self.weather[1]) 
                self.temp_labelcelsius['text'] = '{:.2f}°C'.format(self.weather[2])
                self.feelslike['text'] = 'feels like '+'{:.2f}°C'.format(self.weather[6])
                self.weather_label['text'] = self.weather[5]
                self.humiditylabel['text'] = 'humidity: '+str(self.weather[7])+'%'
                self.pressurelabel['text'] = 'pressure: '+ str(self.weather[8])+' mBar'
                self.visibilitylabel['text']='visibility: '+str(self.weather[9]/1000)+' km'
                self.windspeedlabel['text'] = 'wind speed: '+str(self.weather[10])+' m/s'
                root.withdraw()
        elif self.city == '':
            messagebox.showerror('Error','No city selected')
        else:
            messagebox.showerror('Error','Cannot find city {}'.format(self.city))

root=Tk()
Application(root)
root.mainloop()