import dash  
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the data
tinder = pd.read_csv('Speed_Dating_Data.csv', encoding='ISO-8859-1')

# Replace gender values
tinder['gender'] = tinder['gender'].replace({0: 'female', 1: 'male'})
tinder['match'] = tinder['match'].replace({1: 'yes', 0: 'no'})
tinder['samerace'] = tinder['samerace'].replace({1: 'yes', 0: 'no'})

# Melt the DataFrame for boxplots
tinder_melted = pd.melt(
    tinder,
    id_vars=['gender', 'match', 'samerace', 'like'],
    value_vars=['attr', 'sinc', 'intel', 'fun', 'amb', 'shar']
)
tinder_melted['attributes'] = tinder_melted['variable'].replace({
    'attr': 'Attractive', 'sinc': 'Sincere', 'intel': 'Intelligent',
    'fun': 'Fun', 'amb': 'Ambitious', 'shar': 'Shared Interests'
})

# Data for the interactive activity interest graph
activities = ["tvsports", "exercise", "dining", "museums", "art", "hiking", "gaming",
              "clubbing", "reading", "tv", "theater", "movies", "concerts", "music",
              "shopping", "yoga"]

# Data for the static activity bar plot
data = {
    'activity': ['movies', 'reading', 'gaming', 'dining', 'museums', 'music', 'art', 'theater', 'yoga', 'concerts', 'tvsports', 'clubbing', 'tv', 'exercise', 'hiking', 'shopping'],
    'count': [2021.0, 2000.0, 1983.0, 1924.0, 1801.0, 1789.0, 1750.0, 1618.0, 1549.0, 1531.0, 1522.0, 1402.0, 1381.0, 1358.0, 1212.0, 1198.0],
    'highest_item': [8.0, 9.0, 1.0, 8.0, 7.0, 10.0, 8.0, 7.0, 1.0, 7.0, 1.0, 8.0, 6.0, 8.0, 8.0, 7.0]
}
activity_df = pd.DataFrame(data)
activity_df = activity_df.sort_values(by='highest_item', ascending=True)

# App initialization
app = dash.Dash(__name__)
app.title = "Tinder Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Speed Dating Data Dashboard", style={'textAlign': 'center'}),

    # Dropdown to select a property
    html.Div([
        html.Label("Choose a property to analyze:"),
        dcc.Dropdown(
            id="property-dropdown",
            options=[{'label': col.capitalize(), 'value': col} for col in tinder.columns],
            value="race"
        )
    ], style={'width': '40%', 'margin': 'auto'}),

    # Selected property distribution
    html.Div([
        html.H3("Distribution of Selected Properties"),
        dcc.Graph(id="property-distribution-plot")
    ]),

    html.Hr(),

    # Gender distribution by age
    html.Div([
        html.H3("Gender Distribution by Age"),
        dcc.Graph(id="gender-age-plot")
    ]),

    html.Hr(),

    # Interactive graph for activity interest
    html.Div([
        html.H3("Interest Levels for Selected Activity"),
        dcc.Dropdown(
            id="activity-dropdown",
            options=[{'label': activity.capitalize(), 'value': activity} for activity in activities],
            value="tvsports"
        ),
        dcc.Graph(id="activity-interest-plot")
    ]),

    html.Hr(),

    # Static bar plot for all activities
    html.Div([
        html.H3("Highest Item of Interest by Activity"),
        dcc.Graph(id="activity-barplot")
    ]),

    html.Hr(),

    # Boxplot: Attributes by Same Race
    html.Div([
        html.H3("Boxplot: Attributes by Same Race"),
        dcc.Graph(id="boxplot-samerace")
    ]),

    html.Hr(),

    # Boxplot: Attributes by Match
    html.Div([
        html.H3("Boxplot: Attributes by Match"),
        dcc.Graph(id="boxplot-match")
    ]),

    html.Hr(),

    # Boxplot: Attributes by Like
    html.Div([
        html.H3("Boxplot: Attributes by Like"),
        dcc.Graph(id="boxplot-like")
    ])
])

# Callbacks
@app.callback(
    Output("property-distribution-plot", "figure"),
    Input("property-dropdown", "value")
)
def update_property_distribution(property_name):
    if property_name not in tinder.columns:
        return px.bar(title=f"No data available for {property_name}")

    fig = px.histogram(
        tinder,
        x=property_name,
        title=f"Distribution of {property_name.capitalize()}",
        labels={property_name: property_name.capitalize()},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    return fig


@app.callback(
    Output("gender-age-plot", "figure"),
    Input("property-dropdown", "value")
)
def update_gender_age_plot(_):
    fig = px.histogram(
        tinder,
        x="age",
        color="gender",
        title="Gender Distribution by Age",
        barmode="overlay",
        labels={"age": "Age", "count": "Count"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    return fig


@app.callback(
    Output("boxplot-samerace", "figure"),
    Input("property-dropdown", "value")
)
def update_boxplot_samerace(_):
    fig = px.box(
        tinder_melted,
        x="attributes",
        y="value",
        color="samerace",
        title="Attributes by Same Race",
        labels={"value": "Score", "attributes": "Attributes"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    return fig


@app.callback(
    Output("boxplot-match", "figure"),
    Input("property-dropdown", "value")
)
def update_boxplot_match(_):
    fig = px.box(
        tinder_melted,
        x="attributes",
        y="value",
        color="match",
        title="Attributes by Match",
        labels={"value": "Score", "attributes": "Attributes"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    return fig


@app.callback(
    Output("boxplot-like", "figure"),
    Input("property-dropdown", "value"))

def update_boxplot_like(_):
    median_scores = (
        tinder_melted[tinder_melted['like'].notnull()]
        .groupby('attributes')['value']
        .median()
        .sort_values())

    # Reorder the attributes based on the median score
    ordered_attributes = median_scores.index

    fig = px.box(
        tinder_melted,
        x="attributes",
        y="value",
        color="like",
        title="Attributes by Like (Ordered by Median Score)",
        labels={"value": "Score", "attributes": "Attributes"},
        category_orders={"attributes": ordered_attributes}, 
        color_discrete_sequence=px.colors.qualitative.Set2)
    return fig
    
    fig = px.box(
        tinder_melted,
        x="attributes",
        y="value",
        color="like",
        title="Attributes by Like",
        labels={"value": "Score", "attributes": "Attributes"},
        color_discrete_sequence=px.colors.qualitative.Set2
        #color_continuous_scale='darkmint'
    )
    return fig


@app.callback(
    Output("activity-interest-plot", "figure"),
    Input("activity-dropdown", "value")
)
def update_activity_plot(selected_activity):
    sorted_values = tinder[selected_activity].value_counts().sort_values(ascending=False)
    activity_df = pd.DataFrame({
        'Interest Level': sorted_values.index,
        'Count': sorted_values.values
    }).sort_values(by='Interest Level')

    fig = px.bar(
        activity_df,
        x='Interest Level',
        y='Count',
        title=f"Interest Levels for {selected_activity.capitalize()}",
        labels={'Interest Level': 'Interest Level', 'Count': 'Count'},
        color='Interest Level',
        color_continuous_scale='darkmint'
    )
    return fig


@app.callback(
    Output("activity-barplot", "figure"),
    Input("property-dropdown", "value")
)
def update_activity_barplot(_):
    fig = px.bar(
        activity_df,
        x='activity',
        y='highest_item',
        title='Highest Item of Interest by Activity',
        labels={'activity': 'Activity', 'highest_item': 'Highest Interest Level'},
        color='highest_item',
        color_continuous_scale='darkmint'
    )
    fig.update_layout(xaxis_tickangle=45)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)#app.run_server(debug=False, use_reloader=False) ## app.run_server(debug=True)