from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)

# Importing the graph_objs module which contains plotting objects
import plotly.graph_objs as go
# Trace1 can be viewed like a geom_point() layer with various arguements
trace1 = go.Scatter(x=df.age, y=df.length_of_service, marker=dict(size=5,
                line=dict(width=1),
                color="yellow"
               ), 
                    mode="markers")
					

data1 = go.Data([trace1])
layout1=go.Layout(title="Age vs Length of service", xaxis={'title':'Age'}, yaxis={'title':'Length of Service'})
figure1=go.Figure(data=data1,layout=layout1)
iplot(figure1)


# Histograms

trace2 = go.Histogram(x=df.age)
data2 = go.Data([trace2])
layout2=go.Layout(title="Distribution of Age", xaxis={'title':'AGE'}, yaxis={'title':'Number of employees in data'})
figure2=go.Figure(data=data2,layout=layout2)
iplot(figure2)

# Normalized histogram

trace3 = go.Histogram(x=df.age, histnorm='probability')
data3 = go.Data([trace3])
layout3=go.Layout(title="Distribution of Age", xaxis={'title':'AGE'}, yaxis={'title':'Number of employees in data'})
figure3=go.Figure(data=data3,layout=layout3)
iplot(figure3)

# Overlaid histogram

trace4 = go.Histogram(
    x=terminated.age,
    opacity=1
)
trace5 = go.Histogram(
    x=active.age,
    opacity=0.3
)

data45 = go.Data([trace4, trace5])
layout45 = go.Layout(barmode='overlay')
figure45 = go.Figure(data=data45, layout=layout45)

iplot(figure45, filename='overlaid histogram')

# Stacked Histogram

trace4 = go.Histogram(
    x=terminated.age,
    opacity=0.8
)
trace5 = go.Histogram(
    x=active.age,
    opacity=0.8
)

data45 = go.Data([trace4, trace5])
layout45 = go.Layout(barmode='stack')
figure45 = go.Figure(data=data45, layout=layout45)

iplot(figure45, filename='stacked histogram')

# Bar charts

def create_counts_df(df, categorical_feature):
    new_df = df.groupby([categorical_feature]).count()['store_name'].reset_index()
    new_df.columns = [categorical_feature, 'Total records']
    return new_df

def bar_chart_counts(df, categorical_feature):
    
    df_new = create_counts_df(df, categorical_feature)
    
    data = [go.Bar(
            x=df_new.iloc[:,0],
            y=df_new.iloc[:,1]
    )]

    iplot(data, filename='basic-bar')
    
bar_chart_counts(df, "gender_full")

bar_chart_counts(df, "city_name")

bar_chart_counts(terminated, "city_name")

bar_chart_counts(active, "city_name")

# Grouped Bar Chart

active_gb_gender = create_counts_df(active, "gender_full")
terminated_gb_gender = create_counts_df(terminated, "gender_full")

trace1 = go.Bar(
    x= active_gb_gender.iloc[:,0],
    y= active_gb_gender.iloc[:,1],
    name='Active'
)
trace2 = go.Bar(
    x=terminated_gb_gender.iloc[:,0],
    y=terminated_gb_gender.iloc[:,1],
    name='Terminated'
)

data = [trace1, trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
iplot(fig, filename='grouped-bar')

# Stacked bar chart

data = [trace1, trace2]
layout = go.Layout(
    barmode='stack'
)

fig = go.Figure(data=data, layout=layout)
iplot(fig, filename='stacked-bar')