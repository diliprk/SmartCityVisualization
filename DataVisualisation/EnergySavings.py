import pandas as pd
import numpy as np
from datetime import date
import warnings
warnings.simplefilter('ignore') 

# from bokeh.charts import color, marker, Bar, Scatter, Histogram
from bokeh.plotting import figure
from bokeh.layouts import column,layout,widgetbox
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource,CategoricalColorMapper,HoverTool
from bokeh.models.widgets import Slider


# Reading Per Hour Vehicle Counts for the Entire Day
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTCG1elMKQ8RjGwfIhs8_F7uGbx5qvxEidnm0gXhG2-q-zrhPTzno5TyIILLDIWNe-fKLHtsMfrmzb5/pub?gid=1430444734&single=true&output=csv'
df_hourly = pd.read_csv(url,parse_dates = ['TimeStamps'],infer_datetime_format = True,index_col=['TimeStamps'])

# Subset dataframe to just two days
df_night = df_hourly[df_hourly.DayorNight == 'Night']
df_night = df_night[(df_night.index >= '23-2-2018') & (df_night.index < '25-2-2018')]
dates_unique = df_night.index.map(lambda t: t.date()).unique()
dates_unique = [dates_unique[i].strftime('%Y-%m-%d') for i in range(len(dates_unique))]


## Creating Street Light State DataFrame
statelist = []
countlist = []
Timestamps = []
for e in dates_unique:    
    df_night_date = df_night[e].reset_index()
    IQR75 = int(np.percentile(df_night_date.VehicleCountperHour, 75))
    df_night_date['StreetLightState'] = 'FULL'
    dim_index = df_night_date[df_night_date.VehicleCountperHour < IQR75].index
    df_night_date['StreetLightState'].iloc[dim_index] = 'DIM'
    list1 = df_night_date.StreetLightState.tolist()
    statelist.extend(list1)
    list2 = df_night_date.VehicleCountperHour.tolist()
    countlist.extend(list2)
    list3 = df_night_date.TimeStamps.tolist()
    Timestamps.extend(list3)
    

df_night_lightstate = pd.DataFrame({'Timestamps': Timestamps, 'VehicleCountperHour': countlist, 'StreetLightState':statelist})
df_night_lightstate = df_night_lightstate[['Timestamps','VehicleCountperHour','StreetLightState']]
df_night_lightstate = df_night_lightstate.set_index('Timestamps')

# Restructuring data into a new data frame
dimhours = []
fullbrighthours = []
totalnighthours = []
for e in dates_unique:
    list1 = int(df_night[e].DayorNight.count())
    totalnighthours.append(list1)
    list2 = int(df_night_lightstate.StreetLightState[e][df_night_lightstate.StreetLightState == 'DIM'].count())
    dimhours.append(list2)
    list3 = int(df_night_lightstate.StreetLightState[e][df_night_lightstate.StreetLightState == 'FULL'].count())
    fullbrighthours.append(list3)

dates_list = df_night.index.map(lambda t: t.date()).unique()
df_dimhrs = pd.DataFrame({'Date': dates_list, 'NightHours': totalnighthours, 'LightDimHours':dimhours, 'FullBrightHours': fullbrighthours})
df_dimhrs = df_dimhrs[['Date','NightHours','FullBrightHours','LightDimHours']]
df_dimhrs = df_dimhrs.set_index('Date')
dates_unique = [dates_list[i].strftime('%a, %d-%m-%Y') for i in range(len(dates_list))]

# Initialize Values to start the plot
lights = 10
power = 50
dimming_factor = 0.25

## Set Plot Data Source and oter parameters
source1 = ColumnDataSource(data = dict(normal=['Normal'],max_energy = [(14*lights*power*0.001)]))
source2 = ColumnDataSource(data=dict(dates = dates_unique,
                                     energy=[(a*(lights*power*0.001)) + (b*(lights*power*dimming_factor*0.001)) for a, b in zip(df_dimhrs.FullBrightHours.tolist(),df_dimhrs.LightDimHours.tolist())]))
hover = HoverTool(names=['DimDays'],tooltips=[("Energy Consumption", "@energy kWh")])
hover_fullday = HoverTool(names=['FullDay'],tooltips=[("Energy Consumption", "@max_energy kWh")])


## Make Bokeh Interactive Plot
f = figure(plot_width=960,plot_height=540,y_range=['Normal']+dates_unique,toolbar_location=None,tools=[hover], 
               title="Energy Consumption in a Street after Dimming Street Lights",sizing_mode='scale_width')
f.hbar(y='normal',left=0, right = 'max_energy',source=source1, height=0.25,color="#ea2539",alpha = 0.65,legend="FULL",name='FullDay')
f.hbar(y='dates',left=0, right='energy', height=0.25, source=source2,color = "#48ad1d",alpha = 0.65,legend="DIM",name='DimDays')
f.ygrid.grid_line_color = None
f.x_range.start = 0
f.x_range.end = 60 ##Set this to a value to fix the scale of the X-Axis
f.xaxis.axis_label = "kW-Hr"
f.add_tools(hover_fullday)      

def callback(attr, old, new):   
    lights = Lights_Slider.value
    power = PowerSlider.value
    dimming_factor = DimmingSlider.value
    source1.data = dict(normal=['Normal'],max_energy = [(14*lights*power*0.001)])        
    source2.data = dict(dates = dates_unique,
                        energy=[(a*(lights*power*0.001)) + (b*(lights*power*dimming_factor*0.001)) for a, b in zip(df_dimhrs.FullBrightHours.tolist(),df_dimhrs.LightDimHours.tolist())])
    

Lights_Slider = Slider(start=0, end=20, value=10, step=1, title="No. of Street Lights")
PowerSlider = Slider(start=10, end=200, value=50, step=1, title="Power (Watts) of each Light")
DimmingSlider = Slider(start=0.25, end=1, value=0.25, step=.25, title="Dimming Factor")
for w in [Lights_Slider, PowerSlider, DimmingSlider]:
    w.on_change('value', callback)
layout = column(widgetbox(Lights_Slider,PowerSlider,DimmingSlider),f)
curdoc().add_root(layout)
curdoc().title = "EnergySavings"