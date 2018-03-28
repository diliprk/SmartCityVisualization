import pandas as pd
import numpy as np
from datetime import date
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox,row, column
from bokeh.io import curdoc
from bokeh.models import Label,WMTSTileSource
from bokeh.models.widgets import Slider,DatePicker


# Reading Per Hour Vehicle Counts for the Entire Day
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTCG1elMKQ8RjGwfIhs8_F7uGbx5qvxEidnm0gXhG2-q-zrhPTzno5TyIILLDIWNe-fKLHtsMfrmzb5/pub?gid=1430444734&single=true&output=csv'
df_hourly = pd.read_csv(url,parse_dates = ['TimeStamps'],infer_datetime_format = True,index_col=['TimeStamps'])
df_hourly['Hour_of_Day'] = df_hourly.index.hour ## Add Hour of Day as Numerical Index
# Initial Declarations
hour_value = 10
date_value = date(2018, 2, 23)
date_value = date_value.strftime('%Y-%m-%d')

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

## Make Bokeh Interactive Plot
p1 = figure(plot_width=425, plot_height=425,tools="",toolbar_location="above", x_range=x_range,y_range=y_range,
                title = "Hourly Vehicle Count at {}".format(df_city.name.iloc[0]),sizing_mode='scale_width')
p1.axis.visible = False
p1.add_tile(WMTSTileSource(url=urlmap, attribution=attribution))
p1.circle(x=df_city['x'], y=df_city['y'], fill_color='white',line_color="red",line_width=4,size=42)
annotation1 = Label(x=207, y=247, x_units='screen', y_units='screen',render_mode='css',background_fill_color='white',
         text='{}'.format(int(df_hourly.VehicleCountperHour.loc[date_value][df_hourly.Hour_of_Day == hour_value])),
        background_fill_alpha=0.0,text_color = 'black',text_font = 'arial',text_font_size = '12pt')
p1.add_layout(annotation1)
p2 = figure(plot_width=425, plot_height=425,tools='save',toolbar_location="above", x_range=x_range,y_range=y_range,
            title = "Daily Total Vehicle Count for {}".format(df_city.name.iloc[0]),sizing_mode='scale_width')
p2.axis.visible = False
p2.add_tile(WMTSTileSource(url=urlmap, attribution=attribution))
p2.circle(x=df_city['x'], y=df_city['y'], fill_color='white',line_color="red",line_width=4,size=42)
annotation2 = Label(x=200, y=247, x_units='screen',y_units='screen',background_fill_color='white',text_color = 'black',   text='{}'.format(df_hourly.loc[date_value].VehicleCountperHour.sum()),render_mode='css',background_fill_alpha=0.0,text_font = 'arial',text_font_size = '12pt')
p2.add_layout(annotation2)

def update(attr, old, new):    
    date_value = date_picker.value.strftime('%Y-%m-%d')
    hour_value = hour_slider.value
    annotation1.text = '{}'.format(int(df_hourly.VehicleCountperHour.loc[date_value][df_hourly.Hour_of_Day == hour_value]))
    annotation2.text = '{}'.format(df_hourly.loc[date_value].VehicleCountperHour.sum())             
    
date_picker = DatePicker(min_date=date(2018,2,23), max_date=date(2018,2,24), value=date(2018,2,23), title="Select Date:")
date_picker.on_change('value', update)    
hour_slider = Slider(title="Hour of Day", start=0, end=23,value=10, step=1)
hour_slider.on_change('value', update)
layout = column(widgetbox(date_picker,hour_slider),row(p1,p2)) 
curdoc().add_root(layout)
curdoc().title = "MapVizVehicleTraffic"