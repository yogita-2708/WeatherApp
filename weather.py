from tkinter import *
import tkinter as tk  
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import requests
import pytz
import json

root = tk.Tk()
root.title("Weather App")
root.geometry("900x500")
root.resizable(False, False)

# Function to save data to a file
def save_data(data):
    with open("all_cities_last_fetched_data.json", "w") as file:
        json.dump(data, file)

# Function to load data from a file
def load_data():
    try:
        with open("all_cities_last_fetched_data.json", "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}

# Checking internet connection
def check_internet():
    try:
        requests.get("http://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

# Function to show last fetched data for a specific city
def show_last_fetched_data(city_name):
    all_cities_data = load_data()
    if city_name in all_cities_data:
        last_fetched_data = all_cities_data[city_name]

        name.config(text=f"LAST UPDATED")
        condition = last_fetched_data['weather'][0]['main']
        description = last_fetched_data['weather'][0]['description']
        temp = int(last_fetched_data['main']['temp'] - 273.15)
        pressure = last_fetched_data['main']['pressure']
        humidity = last_fetched_data['main']['humidity']
        wind = last_fetched_data['wind']['speed']

        t.config(text=(temp, "°"))
        c.config(text=(condition, "|", "Feels", "Like", temp, "°C"))
        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)
        messagebox.showinfo("Info", f"Showing last fetched data for {city_name}.")
    else:
        messagebox.showinfo("Info", f"No last fetched data available for {city_name}.")

# Function to get weather data for a specific city
def getWeather():
    try:
        if check_internet():
            city = textfield.get()

            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(city)
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M %p")
            clock.config(text=current_time)
            name.config(text=f"CURRENT WEATHER")

            # Current weather
            api_current = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=cb0ac61ad565ae7eb8367dedbf4fb0cd"
            json_data_current = requests.get(api_current).json()

            # Save last fetched data based on city name
            all_cities_data = load_data()
            all_cities_data[city] = json_data_current
            save_data(all_cities_data)

            condition = json_data_current['weather'][0]['main']
            description = json_data_current['weather'][0]['description']
            temp = int(json_data_current['main']['temp'] - 273.15)
            pressure = json_data_current['main']['pressure']
            humidity = json_data_current['main']['humidity']
            wind = json_data_current['wind']['speed']

            t.config(text=(temp, "°"))
            c.config(text=(condition, "|", "Feels", "Like", temp, "°C"))
            w.config(text=wind)
            h.config(text=humidity)
            d.config(text=description)
            p.config(text=pressure)

            # Forecast
            api_forecast = "https://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=cb0ac61ad565ae7eb8367dedbf4fb0cd"
            json_data_forecast = requests.get(api_forecast).json()
            forecast_data = json_data_forecast['list']

            # Display forecast
            for i in range(5):  # Display forecast for the next 5 days
                date = (local_time + timedelta(days=i)).strftime("%Y-%m-%d")
                temp_min = int(forecast_data[i]['main']['temp_min'] - 273.15)
                temp_max = int(forecast_data[i]['main']['temp_max'] - 273.15)
                description = forecast_data[i]['weather'][0]['description']

                forecast_labels[i].config(text=f"{date}\nMin: {temp_min}°C\nMax: {temp_max}°C\n{description}")

        else:
            messagebox.showwarning("Warning", "Internet not available. Click on Go Offline.")
            # show_last_fetched_data(textfield.get())

    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data!!")

# Designing the interface
# search box
Search_image = PhotoImage(file="search.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=15)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

Search_icon = PhotoImage(file="search_icon.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=28)

# logo
Logo_image = PhotoImage(file="logo.png")
logo = Label(image=Logo_image)
logo.place(x=200, y=90)

# Bottom Box
Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=6, side=BOTTOM)

# time
name = Label(root, font=("Times New Roman", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# label
label1 = Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label1.place(x=125, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label2.place(x=255, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label3.place(x=435, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label4.place(x=655, y=400)

# temperature
t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=500, y=110)

# condition
c = Label(font=("times new roman", 18, 'bold'))
c.place(x=500, y=210)

# wind
w = Label(text="...", font=("times new roman", 15, "bold"), bg="#1ab5ef")
w.place(x=125, y=430)

# humidity
h = Label(text="...", font=("times new roman", 15, "bold"), bg="#1ab5ef")
h.place(x=285, y=430)

# description
d = Label(text="...", font=("Helvetica", 15, "bold"), bg="#1ab5ef")
d.place(x=440, y=430)

# pressure
p = Label(text="...", font=("times new roman", 15, "bold"), bg="#1ab5ef")
p.place(x=700, y=430)

# Labels for forecast
forecast_labels = []
for i in range(5):
    forecast_label = Label(root, text="", font=("Helvetica", 10, "bold"), bg="#404040", padx=10, pady=10, fg="white")
    forecast_label.place(x=30 + i * 180, y=300)
    forecast_labels.append(forecast_label)

# Adding a button for checking internet connectivity and showing last fetched data
check_internet_button = Button(root, text="Go Offline", command=lambda: show_last_fetched_data(textfield.get()))
check_internet_button.place(x=730, y=30)

root.mainloop()
