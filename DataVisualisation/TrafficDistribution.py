import pandas as pd
import numpy as np
from datetime import date
import warnings
warnings.simplefilter('ignore') 

# from bokeh.charts import color, marker, Bar, Scatter, Histogram
from bokeh.plotting import figure
from bokeh.layouts import column,layout,widgetbox
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource,CategoricalColorMapper,HoverTool,Label
from bokeh.models.widgets import Slider,DateSlider


# Reading Per Hour Vehicle Counts for the Entire Day
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTCG1elMKQ8RjGwfIhs8_F7uGbx5qvxEidnm0gXhG2-q-zrhPTzno5TyIILLDIWNe-fKLHtsMfrmzb5/pub?gid=1430444734&single=true&output=csv'
df_hourly = pd.read_csv(url,parse_dates = ['TimeStamps'],infer_datetime_format = True,index_col=['TimeStamps'])
df_night = df_hourly[df_hourly.DayorNight == 'Night']
df_night = df_night[(df_night.index >= '22-2-2018') & (df_night.index < '25-2-2018')]
dates_unique = df_night.index.map(lambda t: t.date()).unique()
dates_unique = [dates_unique[i].strftime('%Y-%m-%d') for i in range(len(dates_unique))]

## Custom function to Set the bar for each hour at a decent width
## https://stackoverflow.com/questions/40185561/auto-set-vbar-line-width-based-on-x-range-in-bokeh
def get_width(df):
    '''Pass DataFrame as input attribute to the function'''
    mindate = min(df.index)
    maxdate = max(df.index)
    return 0.75 * (maxdate-mindate).total_seconds()*1000 / len(df.index)

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

## Set Plot Data Source and oter parameters
source1 = ColumnDataSource(data=dict(x=df_hourly.loc[('23-2-2018')].index, 
                                     y=df_hourly.loc['23-2-2018'].VehicleCountperHour,
                                     label1 = df_hourly.loc['23-2-2018'].DayorNight.tolist()))
source2 = ColumnDataSource(data=dict(a = df_night_lightstate.loc['23-2-2018'].index,
                                     b = df_night_lightstate.loc['23-2-2018'].VehicleCountperHour,
                                     label2 = df_night_lightstate.loc['23-2-2018'].StreetLightState.tolist()))
hover = HoverTool(names=['Traffic'],tooltips=[("Timestamp", "@x{%F %T}"),("CountValue", "@y")],formatters={"x": "datetime"})
hover.point_policy= "snap_to_data"
color_mapper1 = CategoricalColorMapper(factors=['Day', 'Night'], palette=['#ffe47c','#3692b6'])
color_mapper2 = CategoricalColorMapper(factors=['FULL', 'DIM'], palette=['#ea2539','#48ad1d'])


## Make Bokeh Interactive Plot
p = figure(title = "Hourly Vehicle Count",width = 960,height=540,sizing_mode='scale_width',
              x_axis_type='datetime',y_range=(0, (df_hourly.VehicleCountperHour.max()+1)))
p.line('x','y',color="Red",alpha = 0.55, source = source1)
p.vbar('x', top='y',width=get_width(df_hourly),alpha = 0.75,source=source1,color={'field': 'label1', 'transform': color_mapper1},legend='label1',name='Traffic')
p.add_tools(hover)
p.circle('a','b',size=15,alpha = 0.5,source=source2,color={'field': 'label2', 'transform': color_mapper2},legend='label2')
annotation1 = Label(x=20, y=460, x_units='screen', y_units='screen',text='Busiest Hour of the Day: {} cars @ {}'.format(df_hourly.loc['23-2-2018'].VehicleCountperHour.max(),df_hourly.loc['23-2-2018'].VehicleCountperHour.idxmax()), render_mode='css',background_fill_color='white', background_fill_alpha=0.45,text_font = 'arial',text_font_size = '9pt', text_color='#828282')
annotation2 = Label(x=20, y=440, x_units='screen', y_units='screen',text='Average Hourly Vehicle Traffic: ~ {} per hour'.format(round(df_hourly.loc['23-2-2018'].VehicleCountperHour.mean())), render_mode='css',background_fill_color='white', background_fill_alpha=0.55,text_font = 'arial',text_font_size = '9pt', text_color='#828282')
annotation3 = Label(x=20, y=-40, x_units='screen', y_units='screen',text='Total Car movement in the day:{}'.format(df_hourly.loc['23-2-2018'].VehicleCountperHour.sum()),render_mode='css',background_fill_color='white',background_fill_alpha=0.55,text_font = 'times',text_font_size = '10pt',text_font_style='bold')   
p.add_layout(annotation1)
p.add_layout(annotation2)
p.add_layout(annotation3)

def update(attr, old, new):    
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

slider = DateSlider(start=date(2018,2,22), end=date(2018,2,24), value=date(2018,2,23), step=1, title="Date")
slider.on_change('value', update)
layout = column(slider,p)
curdoc().add_root(layout)
curdoc().title = "HourlyVehicleTraffic"