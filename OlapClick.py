import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('D:/diabetes+130-us+hospitals+for+years+1999-2008/cleaned_diabetic_data_with_Median.csv')

readmitted_mapping = {
    '>30': 'Up',
    '<30': 'Down',
    'NO': 'No'
}
df['readmitted_mapped'] = df['readmitted'].map(readmitted_mapping)

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Medication Combination Effectiveness", style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div([
        html.Label("Select Medication 1:", style={'fontSize': '20px', 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='drug1-dropdown',
            options=[
                {'label': 'Metformin', 'value': 'metformin'},
                {'label': 'Glipizide', 'value': 'glipizide'},
                {'label': 'Glyburide', 'value': 'glyburide'},
                {'label': 'Insulin', 'value': 'insulin'},
                {'label': 'Repaglinide', 'value': 'repaglinide'},
                {'label': 'Nateglinide', 'value': 'nateglinide'},
                {'label': 'Chlorpropamide', 'value': 'chlorpropamide'},
                {'label': 'Glimepiride', 'value': 'glimepiride'},
                {'label': 'Acetohexamide', 'value': 'acetohexamide'},
                {'label': 'Tolbutamide', 'value': 'tolbutamide'}
            ],
            value=None,  
            placeholder="Select the First Medication",
            style={'width': '60%', 'margin': '0 auto'}
        ),
        html.Div(id='drug1-plot', style={'textAlign': 'center', 'marginTop': '20px'})
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    html.Div([
        html.Label("Select Medication 2:", style={'fontSize': '20px', 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='drug2-dropdown',
            options=[],  
            value=None,
            placeholder="Select the Second Medication",
            disabled=True,  
            style={'width': '60%', 'margin': '0 auto'}
        ),
        html.Div(id='drug2-plot', style={'textAlign': 'center', 'marginTop': '20px'})
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    html.Div(style={'textAlign': 'center', 'marginBottom': '40px'}, children=[
        html.Button('Show Details', id='relationship-button', n_clicks=0, 
                    style={
                        'backgroundColor': '#007bff',
                        'color': 'white',
                        'border': 'none',
                        'padding': '10px 20px',
                        'fontSize': '16px',
                        'cursor': 'pointer',
                        'borderRadius': '5px',
                        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
                    })
    ]),

    html.Div(id='relationship-plot', style={'textAlign': 'center', 'marginBottom': '40px'}),
    html.Div(id='analysis-plot', style={'textAlign': 'center', 'marginBottom': '40px'}),
    html.Div(id='summary-statistics', style={'textAlign': 'center', 'marginBottom': '40px'}),
    html.Div(id='correlation-matrix', style={'textAlign': 'center', 'marginBottom': '40px'})
])

@app.callback(
    Output('drug1-plot', 'children'),
    [Input('drug1-dropdown', 'value')]
)
def update_drug1_plot(selected_drug):
    if selected_drug is None:
        return None  

    fig = px.histogram(df, x=selected_drug, color=selected_drug,
                       title=f"Distribution of {selected_drug.capitalize()} Usage",
                       labels={selected_drug: f"{selected_drug.capitalize()} Usage"},
                       template="plotly_dark")
    fig.update_layout(bargap=0.2)

    return dcc.Graph(figure=fig)

@app.callback(
    [Output('drug2-dropdown', 'options'),
     Output('drug2-dropdown', 'disabled'),
     Output('relationship-button', 'disabled')],
    [Input('drug1-dropdown', 'value')]
)
def set_drug2_options(selected_drug1):
    if selected_drug1 is None:
        return [], True, True  
    else:
        options = [
            {'label': 'Metformin', 'value': 'metformin'},
            {'label': 'Glipizide', 'value': 'glipizide'},
            {'label': 'Glyburide', 'value': 'glyburide'},
            {'label': 'Insulin', 'value': 'insulin'},
            {'label': 'Repaglinide', 'value': 'repaglinide'},
            {'label': 'Nateglinide', 'value': 'nateglinide'},
            {'label': 'Chlorpropamide', 'value': 'chlorpropamide'},
            {'label': 'Glimepiride', 'value': 'glimepiride'},
            {'label': 'Acetohexamide', 'value': 'acetohexamide'},
            {'label': 'Tolbutamide', 'value': 'tolbutamide'}
        ]

        options = [opt for opt in options if opt['value'] != selected_drug1]
        return options, False, False  

@app.callback(
    Output('drug2-plot', 'children'),
    [Input('drug2-dropdown', 'value')]
)
def update_drug2_plot(selected_drug):
    if selected_drug is None:
        return None  

    fig = px.histogram(df, x=selected_drug, color=selected_drug,
                       title=f"Distribution of {selected_drug.capitalize()} Usage",
                       labels={selected_drug: f"{selected_drug.capitalize()} Usage"},
                       template="plotly_dark")
    fig.update_layout(bargap=0.2)

    return dcc.Graph(figure=fig)

@app.callback(
    [Output('relationship-plot', 'children'),
     Output('analysis-plot', 'children'),
     Output('summary-statistics', 'children'),
     Output('correlation-matrix', 'children')],
    [Input('relationship-button', 'n_clicks'),
     Input('drug1-dropdown', 'value'),
     Input('drug2-dropdown', 'value')]
)
def handle_relationship_and_analysis(n_clicks, drug1, drug2):
    ctx = dash.callback_context

    if ctx.triggered and ctx.triggered[0]['prop_id'] in ['drug1-dropdown.value', 'drug2-dropdown.value']:
        return None, None, None, None

    if n_clicks > 0 and drug1 and drug2:
        # Generate the violin plot
        fig1 = px.violin(df, x=drug1, y=drug2, 
                          title=f'Violin Plot of {drug2.capitalize()} across {drug1.capitalize()} Levels',
                          labels={drug1: f'{drug1.capitalize()} Usage', drug2: f'{drug2.capitalize()} Usage'},
                          template="plotly_dark")
        fig1.update_traces(box_visible=True, meanline_visible=True)
        relationship_plot = dcc.Graph(figure=fig1)

        # Analysis plot
        df_filtered = df[df[drug1].notna() & df[drug2].notna()]
        df_filtered[drug1] = df_filtered[drug1].astype(str)
        df_filtered[drug2] = df_filtered[drug2].astype(str)
        df_filtered['drug_combination'] = df_filtered[drug1] + ' & ' + df_filtered[drug2]

        def calculate_percentage(group):
            total = group['readmitted_mapped'].count()
            percentages = group['readmitted_mapped'].value_counts(normalize=True) * 100
            return percentages

        combinations = df_filtered['drug_combination'].unique()
        results = []

        for combo in combinations:
            subset = df_filtered[df_filtered['drug_combination'] == combo]
            percentages = calculate_percentage(subset)
            results.append({
                'Combination': combo,
                'Up': percentages.get('Up', 0),
                'Down': percentages.get('Down', 0),
                'No': percentages.get('No', 0)
            })

        results_df = pd.DataFrame(results).set_index('Combination')

        fig2 = go.Figure()

        for status in results_df.columns:
            fig2.add_trace(go.Bar(
                x=results_df.index,
                y=results_df[status],
                name=status
            ))

        fig2.update_layout(barmode='stack',
                           title=f'Percentage of Readmitted Status by Combination of {drug1.capitalize()} and {drug2.capitalize()}',
                           xaxis_title='Medication Combination',
                           yaxis_title='Percentage (%)',
                           template="plotly_dark")

        analysis_plot = dcc.Graph(figure=fig2)

        # Detailed Summary Statistics
        summary_stats = {
            "Statistic": ["Mode", "No", "Up", "Steady", "Down", "Count"],
            drug1.capitalize(): [
                df[drug1].mode()[0] if not df[drug1].mode().empty else None,
                df_filtered[drug1].value_counts().get("No", 0),
                df_filtered[drug1].value_counts().get("Up", 0),
                df_filtered[drug1].value_counts().get("Steady", 0),
                df_filtered[drug1].value_counts().get("Down", 0),
                df_filtered[drug1].count()
            ],
            drug2.capitalize(): [
                df[drug2].mode()[0] if not df[drug2].mode().empty else None,
                df_filtered[drug2].value_counts().get("No", 0),
                df_filtered[drug2].value_counts().get("Up", 0),
                df_filtered[drug2].value_counts().get("Steady", 0),
                df_filtered[drug2].value_counts().get("Down", 0),
                df_filtered[drug2].count()
            ]
        }
        summary_stats_df = pd.DataFrame(summary_stats)

        summary_stats_fig = go.Figure(data=[go.Table(
            header=dict(values=list(summary_stats_df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[summary_stats_df[col] for col in summary_stats_df.columns],
                       fill_color='lavender',
                       align='left'))
        ])
        summary_stats_fig.update_layout(title_text='Detailed Summary Statistics')
        summary_statistics = dcc.Graph(figure=summary_stats_fig)

        le = LabelEncoder()
        df_encoded = df[[drug1, drug2]].apply(le.fit_transform)

        # Correlation Matrix
        corr_matrix = df_encoded.corr()
        corr_matrix_fig = px.imshow(corr_matrix, text_auto=True, aspect='auto', color_continuous_scale='Viridis',
                                    title=f'Correlation Matrix between {drug1.capitalize()} and {drug2.capitalize()}',
                                    labels={'color': 'Correlation'})
        correlation_matrix = dcc.Graph(figure=corr_matrix_fig)

        return relationship_plot, analysis_plot, summary_statistics, correlation_matrix

    return None, None, None, None

if __name__ == '__main__':
    app.run_server(debug=True, port=8054)
