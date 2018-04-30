import pandas as pd
import numpy as np
from datetime import date
import warnings
warnings.simplefilter('ignore')

from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox,row, column
from bokeh.io import curdoc
from bokeh.models import Label,WMTSTileSource,ColumnDataSource,CategoricalColorMapper,HoverTool,Div
from bokeh.models.widgets import Slider,DatePicker,DateSlider,Tabs,Panel


# Reading Per Hour Vehicle Counts for the Entire Day
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTCG1elMKQ8RjGwfIhs8_F7uGbx5qvxEidnm0gXhG2-q-zrhPTzno5TyIILLDIWNe-fKLHtsMfrmzb5/pub?gid=1430444734&single=true&output=csv'
df_hourly = pd.read_csv(url,parse_dates = ['TimeStamps'],infer_datetime_format = True,index_col=['TimeStamps'])
df_hourly['Hour_of_Day'] = df_hourly.index.hour ## Add Hour of Day as Numerical Index
# Initial Declarations
hour_value = 10
date_val = date(2018, 2, 23)
date_val = date_val.strftime('%Y-%m-%d')

## Intro Text
intro_text = Div(text="""
        <h3 style="text-align:center">Vehicle Traffic Analysis for Smart Street Lighting</h3><br>
        <p>This is a data dashboard created using <a href="https://bokeh.pydata.org/en/latest/" target="_blank">Bokeh</a>.<br>
        <ul><li>On the first tab titled <code>MapVizVehicleTraffic</code>  you can see the
        vehicle traffic on a map which changes when dragging the hour slider or
        when selecting a new date from the Date picker.</li>
        <li>On the second tab  titled <code>Traffic & Energy</code> you can see the
        vehicle traffic data distribution as a bar plot with an overlaid line plot.</li>
        <li>We can also see the <em>Street Light State</em> in the night time
        traffic hours indicated as <font style="color:Tomato">RED</font>
        dots for those hours in the night where we run the street lights at Full
        Brightness because of heavy vehicle traffic and <font style="color:MediumSeaGreen">GREEN</font>
        dots for those hours in the night where we can DIM the street lights
        because of low vehicle traffic. Finally we can also see the Energy Savings
        resulting from the dimming the street lights.</li></ul></p>
    """)
para1 = Div(width = 960,text="""<h3>Hourly Vehicle Traffic - Street View</h3><br>
See hourly vehicle count change by dragging the hour slider for date selected.<br>
The right plot shows the total no. of cars that has passed by the street for the entire day.""")

para2 = Div(width = 960,text="""<h3>Traffic Density & Street Light State</h3><br>
Drag the date slider to see the hourly vehicle traffic distribution and Street Light State of the Hour for the selected Date.
""")

para3 = Div(width = 960,text="""<br><h3>Energy Savings by Dimming Street Lights</h3><br>
Comparison of Energy Consumption by Dimming Street Lights (<font style="color:MediumSeaGreen;">Green Bars</font>)
 in a street at certain hours when vehicle traffic is less Vs. running street lights through out the entire night at Full Brightness (<font style="color:Tomato;">Red Bars</font>) .
""")

# Use this link to convert Lat Long to Web Mercarator co-ordinates: https://epsg.io/map
city = x_range,y_range = ((781303,781373),(6316450,6316499))
urlmap = 'http://a.basemaps.cartocdn.com/light_all/{Z}/{X}/{Y}.png'
attribution = "Tiles by Carto, under CC BY 3.0. Data by OSM, under ODbL"

def wgs84_to_web_mercator(df, lon="lon", lat="lat"):
    """Converts decimal longitude/latitude to Web Mercator format"""
    k = 6378137
    df["x"] = df[lon] * (k * np.pi/180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
    return df

df_city = pd.DataFrame(dict(name=["Waldhausweg, Saarbruecken"], lat=[49.2447058], lon=[7.0188925]))
wgs84_to_web_mercator(df_city)

## Make Bokeh Interactive Plot of Map Viz Data
p1 = figure(plot_width=425, plot_height=425,tools="",toolbar_location="above", x_range=x_range,y_range=y_range,sizing_mode='scale_width',
                title = "Hourly Vehicle Count at {}".format(df_city.name.iloc[0]))
p1.axis.visible = False
p1.add_tile(WMTSTileSource(url=urlmap, attribution=attribution))
p1.circle(x=df_city['x'], y=df_city['y'], fill_color='white',line_color="red",line_width=4,size=42)
ant1 = Label(x=207, y=247, x_units='screen', y_units='screen',render_mode='css',background_fill_color='white',
         text='{}'.format(int(df_hourly.VehicleCountperHour.loc[date_val][df_hourly.Hour_of_Day == hour_value])),
        background_fill_alpha=0.0,text_color = 'black',text_font = 'arial',text_font_size = '12pt')
p1.add_layout(ant1)
p2 = figure(plot_width=425,plot_height=425,tools='save',toolbar_location="above",x_range=x_range,y_range=y_range,sizing_mode='scale_width',
            title = "Daily Total Vehicle Count for {}".format(df_city.name.iloc[0]))
p2.axis.visible = False
p2.add_tile(WMTSTileSource(url=urlmap, attribution=attribution))
p2.circle(x=df_city['x'], y=df_city['y'], fill_color='white',line_color="red",line_width=4,size=42)
ant2 = Label(x=200, y=247, x_units='screen',y_units='screen',background_fill_color='white',text_color = 'black',   text='{}'.format(df_hourly.loc[date_val].VehicleCountperHour.sum()),render_mode='css',background_fill_alpha=0.0,text_font = 'arial',text_font_size = '12pt')
p2.add_layout(ant2)

def update_mapplot(attr, old, new):
    datepick_value = date_picker.value.strftime('%Y-%m-%d')
    hour_value = hour_slider.value
    ant1.text = '{}'.format(int(df_hourly.VehicleCountperHour.loc[datepick_value][df_hourly.Hour_of_Day == hour_value]))
    ant2.text = '{}'.format(df_hourly.loc[datepick_value].VehicleCountperHour.sum())

date_picker = DatePicker(min_date=date(2018,2,23), max_date=date(2018,2,24), value=date(2018,2,23), title="Select Date:")
date_picker.on_change('value', update_mapplot)
hour_slider = Slider(title="Hour of Day", start=0, end=23,value=10, step=1)
hour_slider.on_change('value', update_mapplot)
# layout = column(widgetbox(date_picker,hour_slider),row(p1,p2))
Panel1 = Panel(child = column(para1,widgetbox(date_picker,hour_slider),row(p1,p2)), title = "MapVizVehicleTraffic")

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


## Set Plot Data Source and other parameters
source1 = ColumnDataSource(data=dict(x=df_hourly.loc[date_val].index,
                                     y=df_hourly.loc[date_val].VehicleCountperHour,
                                     label1 = df_hourly.loc[date_val].DayorNight.tolist()))
source2 = ColumnDataSource(data=dict(a = df_night_lightstate.loc[date_val].index,
                                     b = df_night_lightstate.loc[date_val].VehicleCountperHour,
                                     label2 = df_night_lightstate.loc[date_val].StreetLightState.tolist()))
hover = HoverTool(names=['Traffic'],tooltips=[("Timestamp", "@x{%F %T}"),("CountValue", "@y")],formatters={"x": "datetime"})
hover.point_policy= "snap_to_data"
color_mapper1 = CategoricalColorMapper(factors=['Day', 'Night'], palette=['#ffe47c','#3692b6'])
color_mapper2 = CategoricalColorMapper(factors=['FULL', 'DIM'], palette=['#ea2539','#48ad1d'])

source3 = ColumnDataSource(data = dict(normal=['Normal'],max_energy = [(14*lights*power*0.001)]))
source4 = ColumnDataSource(data=dict(dates = dates_unique,
                                     energy=[(a*(lights*power*0.001)) + (b*(lights*power*dimming_factor*0.001)) for a, b in zip(df_dimhrs.FullBrightHours.tolist(),df_dimhrs.LightDimHours.tolist())]))
hover_dimdays = HoverTool(names=['DimDays'],tooltips=[("Energy Consumption", "@energy kWh")])
hover_fullday = HoverTool(names=['FullDay'],tooltips=[("Energy Consumption", "@max_energy kWh")])


## Custom function to Set the bar for each hour at a decent width
## https://stackoverflow.com/questions/40185561/auto-set-vbar-line-width-based-on-x-range-in-bokeh
def get_width(df):
    '''Pass DataFrame as input attribute to the function'''
    mindate = min(df.index)
    maxdate = max(df.index)
    return 0.75 * (maxdate-mindate).total_seconds()*1000 / len(df.index)

## Make Bokeh Interactive Plot of Traffic Distribution
p3 = figure(title = "Hourly Vehicle Count",width = 960,height=540,sizing_mode='scale_width',x_axis_type='datetime',y_range=(0, (df_hourly.VehicleCountperHour.max()+1)))
p3.line('x','y',color="Red",alpha = 0.55, source = source1)
p3.vbar('x', top='y',width=get_width(df_hourly),alpha = 0.75,source=source1,color={'field': 'label1', 'transform': color_mapper1},legend='label1',name='Traffic')
p3.add_tools(hover)
p3.circle('a','b',size=15,alpha = 0.5,source=source2,color={'field': 'label2', 'transform': color_mapper2},legend='label2')
annotation1 = Label(x=20, y=460, x_units='screen', y_units='screen',text='Busiest Hour of the Day: {} cars @ {}'.format(df_hourly.loc[date_val].VehicleCountperHour.max(),df_hourly.loc['23-2-2018'].VehicleCountperHour.idxmax()), render_mode='css',background_fill_color='white', background_fill_alpha=0.45,text_font = 'arial',text_font_size = '9pt', text_color='#828282')
annotation2 = Label(x=20, y=440, x_units='screen', y_units='screen',text='Average Hourly Vehicle Traffic: ~ {} per hour'.format(round(df_hourly.loc[date_val].VehicleCountperHour.mean())), render_mode='css',background_fill_color='white', background_fill_alpha=0.55,text_font = 'arial',text_font_size = '9pt', text_color='#828282')
annotation3 = Label(x=20, y=-40, x_units='screen', y_units='screen',text='Total Car movement in the day:{}'.format(df_hourly.loc[date_val].VehicleCountperHour.sum()),render_mode='css',background_fill_color='white',background_fill_alpha=0.55,text_font = 'times',text_font_size = '10pt',text_font_style='bold')
p3.add_layout(annotation1)
p3.add_layout(annotation2)
p3.add_layout(annotation3)

## Make Bokeh Interactive Plot of Energy Savings
f = figure(width = 960,height=540,sizing_mode='scale_width',y_range=['Normal']+dates_unique,toolbar_location=None,tools=[hover_dimdays],
               title="Energy Consumption in a Street after Dimming Street Lights")
f.hbar(y='normal',left=0, right = 'max_energy',source=source3, height=0.25,color="#ea2539",alpha = 0.65,legend="FULL",name='FullDay')
f.hbar(y='dates',left=0, right='energy', height=0.25, source=source4,color = "#48ad1d",alpha = 0.65,legend="DIM",name='DimDays')
f.ygrid.grid_line_color = None
f.x_range.start = 0
f.x_range.end = 60 ##Set this to a value to fix the scale of the X-Axis
f.xaxis.axis_label = "kW-Hr"
f.add_tools(hover_fullday)

def update_trafficdist(attr, old, new):
    date_value = new.strftime('%Y-%m-%d')
    new_data1 = dict(x=df_hourly.loc[date_value].index,
                     y=df_hourly.loc[date_value].VehicleCountperHour,
                     label1 = df_hourly.loc[date_value].DayorNight.tolist())
    source1.data = new_data1
    new_data2 = dict(a = df_night_lightstate.loc[date_value].index,
                     b = df_night_lightstate.loc[date_value].VehicleCountperHour,
                     label2 = df_night_lightstate.loc[date_value].StreetLightState.tolist())
    source2.data = new_data2
    annotation1.text = 'Busiest Hour of the Day: {} cars @ {}'.format(df_hourly.loc[date_value].VehicleCountperHour.max(),df_hourly.loc[date_value].VehicleCountperHour.idxmax())
    annotation2.text = 'Average Hourly Vehicle Traffic: ~ {} per hour'.format(round(df_hourly.loc[date_value].VehicleCountperHour.mean()))
    annotation3.text = 'Total Car movement in the day: {}'.format((df_hourly.loc[date_value].VehicleCountperHour.sum()))

date_slider = DateSlider(start=date(2018,2,23), end=date(2018,2,24), value=date(2018,2,23), step=1, title="Date")
date_slider.on_change('value', update_trafficdist)

def callback(attr, old, new):
    lights = Lights_Slider.value
    power = PowerSlider.value
    dimming_factor = DimmingSlider.value
    source3.data = dict(normal=['Normal'],max_energy = [(14*lights*power*0.001)])
    source4.data = dict(dates = dates_unique,
                        energy=[(a*(lights*power*0.001)) + (b*(lights*power*dimming_factor*0.001)) for a, b in zip(df_dimhrs.FullBrightHours.tolist(),df_dimhrs.LightDimHours.tolist())])


Lights_Slider = Slider(start=0, end=20, value=10, step=1, title="No. of Street Lights")
PowerSlider = Slider(start=10, end=200, value=50, step=1, title="Power (Watts) of each Light")
DimmingSlider = Slider(start=0.25, end=1, value=0.25, step=.25, title="Dimming Factor")
for w in [Lights_Slider, PowerSlider, DimmingSlider]:
    w.on_change('value', callback)

Panel2 = Panel(child = column(para2,column(date_slider,p3),para3,column(widgetbox(Lights_Slider,PowerSlider,DimmingSlider),f)), title = "Traffic&Energy",sizing_mode='scale_width')

# show the results
layout = column(intro_text,Tabs(tabs = [Panel1,Panel2]),sizing_mode='scale_width')
curdoc().add_root(layout)
curdoc().title = "Vehicle Traffic Analysis for Smart Street Lighting"
