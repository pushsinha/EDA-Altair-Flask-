from flask import Flask, jsonify, render_template, request
import altair as alt
import pandas as pd
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('vis1.html')


@app.route('/getJson')
def getjson():
    data1_df = pd.read_csv('./hr.csv')
    alt.data_transformers.enable('default', max_rows=None)
    interval = alt.selection_single(fields = ["start_date_hr"])

    scatter = alt.Chart(data1_df).mark_circle(size=45).encode(
    x=alt.X('start_date_hr:Q', title='Hour'),
    y=alt.Y('start_station_count:Q', title='Average Start Station Count'),
    color= alt.condition(interval, 'start_date_hr:Q', alt.value('lightgray')),
    tooltip = 'name'
    ).properties(
    selection=interval,
    height=250,
    width=400,
    title='Start Station Vs Count Plot'
    )

    percent_slider = alt.binding_range(min=10, max=100, step=10)
    slider_selection = alt.selection_single(bind=percent_slider, fields=['percentile'], name = "percentile")
    scatter1 = scatter.mark_point().encode(
    x='vacancy:Q',
    y=alt.Y('duration_mean:Q', title='Average Duration in Minutes'),
    size=alt.Size('start_station_count:Q', 'Average Start Station Count'),
    shape = 'is_member:N',
    tooltip = [alt.Tooltip(shorthand = 'name:N', title = ("Start Station Name")),alt.Tooltip(shorthand = 'start_station_count:Q', title = ("Average No. of Bikes Taken"))]
    ).properties(
    selection=interval,
    title='Hour and Percentile wise Start Station Analysis',
    height=250,
    width=700
    ).add_selection(
    slider_selection
    ).transform_filter(
    interval
    ).transform_filter(
    slider_selection
    ).interactive()
    data = (scatter & scatter1).to_dict()
    return jsonify(data)
@app.route('/getJson1')
def getjson1():
    # import altair as alt
    data1_df = pd.read_csv('./data/vis1_hr.csv')
    alt.data_transformers.enable('default', max_rows=None)
    interval = alt.selection_single(fields = ["start_date_hr"])

    scatter = alt.Chart(data1_df).mark_point(color = 'red', size=30).encode(
        x=alt.X('start_date_hr:Q', title='Hour'),
        y=alt.Y('start_station_count:Q', title='Average Start Station Count'),
        color= alt.condition(interval,alt.value('steelblue'), alt.value('lightgray')),
        tooltip = 'name'
    ).properties(
        selection=interval,
        width=800,
        title='Start Station Vs Count Plot'
    )


    percent_slider = alt.binding_range(min=10, max=100, step=10)
    slider_selection = alt.selection_single(bind=percent_slider, fields=['percentile'], name = "percentile")
    scatter1 = alt.Chart(data1_df).mark_circle().encode(
    x='vacancy:Q',
    y=alt.Y('duration_mean:Q', title='Average Duration in Minutes'),
    size=alt.Size('start_station_count:Q'),
    color = 'is_member:N',
    tooltip = [alt.Tooltip(shorthand = 'name:N', title = ("Start Station Name")),alt.Tooltip(shorthand = 'start_station_count:Q', title = ("Average No. of Bikes Taken"))]
    ).properties(
    selection=interval,
    title='Hour and Percentile wise Start Station Analysis',
    width=600
    ).transform_filter(
    interval
    ).add_selection(
    slider_selection
    ).transform_filter(
    slider_selection
    ).interactive()
    # scatter & scatter1


    data = (scatter & scatter1).to_dict()
    return jsonify(data)

@app.route('/vis1')
def vis1():
    return render_template('vis1.html')

@app.route('/getJson2')
def getjson2():
    data1_df = pd.read_csv('./data/vis2_hr_weather.csv')
    alt.data_transformers.enable('default', max_rows=None)
    interval = alt.selection_multi(fields = ['weather_desc'])
# interval1 = alt.selection_multi(fields = ['hr:N'])

    scatter = alt.Chart(data1_df).mark_circle(size=45).encode(
    y=alt.Y('count:Q', title='Count'),
    x=alt.X('temp_bin:N', title='Temperature Bucket (Farenheit)'),
    color= alt.condition(interval, alt.Color('weather_desc:N', scale=alt.Scale(scheme='category20')), alt.value('lightgray')),
    tooltip = [alt.Tooltip(shorthand = 'hr:N', title = ("Average Count")), alt.Tooltip(shorthand = 'weather_desc:N', title = ("Weather"))]
    ).properties(
    selection=interval,
    width=400,
    title='Weather and Time popularity Info Plot'
    )
    hour_slider = alt.binding_range(min=1, max=24, step=1)
    slider_selection = alt.selection_single(bind=hour_slider, fields=['hr'], name = "Hour")

    # percent_slider = alt.binding_range(min=10, max=100, step=5)
    # slider_selection = alt.selection_single(bind=percent_slider, fields=['percentile'], name = "percentile")
    scatter2 = alt.Chart(data1_df).mark_point().encode(
    x=alt.X('wind_bin:N', title='Wind Speed Bucket (Km/h)'),
    size=alt.Size('count:Q', title='Average Count'),
    y=alt.Y('duration_mean:Q', title='Average Duration in Minutes'),
    shape = 'is_member:N',
    tooltip = [alt.Tooltip(shorthand = 'duration_mean:Q', title = ("Average Duration")), alt.Tooltip(shorthand = 'temp_bin:N', title = ("Temperature Bucket (Farenheit)")), alt.Tooltip(shorthand = 'weather_desc', title = ("Weather")), alt.Tooltip(shorthand = 'count:Q', title = ("Average Count"))]
    ).properties(
    selection=interval,
    title='Counts Based on Temperature Hour and Wind Speed',
    width=200,
    height=500
    ) .transform_filter(
    interval
    ).add_selection(
    slider_selection
    ).transform_filter(
    slider_selection
    ).interactive()
    data = (scatter | scatter2).to_dict()
    return jsonify(data)



@app.route('/getJson3')
def getjson3():
    data1_df = pd.read_csv('./data/vis3_routes.csv')
    alt.data_transformers.enable('default', max_rows=None)
    interval = alt.selection_interval(encodings = ['x', 'y'])

    scatter = alt.Chart(data1_df).mark_point(size=10).encode(
    x=alt.X('weather_desc:N', title='Weather Description'),
    y=alt.Size('count:Q', title='Route Count'),
    color= alt.condition(interval, alt.Color('weather_desc:N', scale=alt.Scale(scheme='category20')), alt.value('lightgray')),
    tooltip = [alt.Tooltip(shorthand = 'start_station_name:N', title = ("Start Station Name"))],
    size = 'duration_mean:Q',
    shape = 'is_member:N'
    ).properties(
    selection=interval,
    width=400,
    height=600,
    title='Routes Plot'
    )

# percent_slider = alt.binding_range(min=10, max=100, step=5)
# slider_selection = alt.selection_single(bind=percent_slider, fields=['percentile'], name = "percentile")
    scatter1 = alt.Chart(data1_df).mark_bar().encode(
    y=alt.Y('end_station_name:N', title='End Station Name'),
    #     size=alt.Y('duration_mean:Q', title='Average Duration in Minutes'),
    x=alt.X('duration_mean:Q', title='Average Duration in Minutes'),
    tooltip = [alt.Tooltip(shorthand = 'start_station_name:N', title = ("Start Station Name")), alt.Tooltip(shorthand = 'end_station_name:N', title = ("End Station Name"))]
    #     color = alt.X('start_station_name:N', title='End Station Name')
    ).properties(
    selection=interval,
    title='End Station and Their Average Duration in Minutes',
    width=500,
    height=300
    ).transform_filter(
    interval
    )
    data = (scatter | scatter1).to_dict()
    return jsonify(data)
