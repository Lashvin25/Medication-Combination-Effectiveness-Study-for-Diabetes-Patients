import matplotlib
matplotlib.use('Agg')  
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import random

df = pd.read_csv('D:/diabetes+130-us+hospitals+for+years+1999-2008/cleaned_diabetic_data_with_Median.csv')

readmitted_mapping = {
    '>30': 'Up',
    '<30': 'Down',
    'NO': 'No'
}
df['readmitted_mapped'] = df['readmitted'].map(readmitted_mapping)

app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("Medication Combination Effectiveness ", style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div([
        html.Label("Select Drug 1:", style={'fontSize': '20px', 'fontWeight': 'bold'}),
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
                # {'label': 'Readmitted', 'value': 'readmitted'},
                # {'label': 'DiabetesMed', 'value': 'diabetesMed'}
            ],
            value=None,  
            placeholder="Select the first drug",
            style={'width': '60%', 'margin': '0 auto'}
        ),
        html.Div(id='drug1-plot', style={'textAlign': 'center', 'marginTop': '20px'})
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    html.Div([
        html.Label("Select Drug 2:", style={'fontSize': '20px', 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='drug2-dropdown',
            options=[],  
            value=None,
            placeholder="Select the second drug",
            disabled=True,  
            style={'width': '60%', 'margin': '0 auto'}
        ),
        html.Div(id='drug2-plot', style={'textAlign': 'center', 'marginTop': '20px'})
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    html.Div(style={'textAlign': 'center', 'marginBottom': '40px'}, children=[
        html.Button('Show Relationship', id='relationship-button', n_clicks=0, 
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
    html.Div(id='analysis-plot', style={'textAlign': 'center'})  
])

def plot_with_gradient(col, color1, color2):
    plt.figure(figsize=(10, 6))

    bars = sns.countplot(x=col, data=df, color=color1, edgecolor='black')
    
    for bar in bars.patches:
        bar.set_facecolor(color1)
        bar.set_edgecolor('black')
        bar.set_linewidth(1.5)
        bar.set_hatch('//')
        
        height = bar.get_height()
        bars.annotate(f'{int(height)}',
                      xy=(bar.get_x() + bar.get_width() / 2, height),
                      xytext=(0, 3), 
                      textcoords="offset points",
                      ha='center', va='bottom', fontsize=12, color='black')

    plt.title(f'Distribution of {col.capitalize()} Usage', fontsize=16)
    plt.xlabel(f'{col.capitalize()} Usage', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_bytes = buf.getvalue()
    buf.close()
    
    encoded_image = base64.b64encode(img_bytes).decode('utf-8')
    return 'data:image/png;base64,{}'.format(encoded_image)

@app.callback(
    Output('drug1-plot', 'children'),
    [Input('drug1-dropdown', 'value')]
)
def update_drug1_plot(selected_drug):
    if selected_drug is None:
        return None  
    colors = {
        'metformin': ('skyblue', 'dodgerblue'),
        'glipizide': ('salmon', 'firebrick'),
        'glyburide': ('lightgreen', 'forestgreen'),
        'insulin': ('orange', 'darkorange'),
        'repaglinide': ('purple', 'indigo'),
        'nateglinide': ('red', 'darkred'),
        'chlorpropamide': ('cyan', 'darkcyan'),
        'glimepiride': ('magenta', 'darkmagenta'),
        'acetohexamide': ('lime', 'green'),
        'tolbutamide': ('brown', 'saddlebrown')
        # 'readmitted': ('blue', 'navy'),
        # 'diabetesMed': ('pink', 'deeppink')
    }
    color1, color2 = colors[selected_drug]
    return html.Div(html.Img(src=plot_with_gradient(selected_drug, color1, color2)), style={'textAlign': 'center'})

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
            # {'label': 'Readmitted', 'value': 'readmitted'},
            # {'label': 'DiabetesMed', 'value': 'diabetesMed'}
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
    colors = {
        'metformin': ('skyblue', 'dodgerblue'),
        'glipizide': ('salmon', 'firebrick'),
        'glyburide': ('lightgreen', 'forestgreen'),
        'insulin': ('orange', 'darkorange'),
        'repaglinide': ('purple', 'indigo'),
        'nateglinide': ('red', 'darkred'),
        'chlorpropamide': ('cyan', 'darkcyan'),
        'glimepiride': ('magenta', 'darkmagenta'),
        'acetohexamide': ('lime', 'green'),
        'tolbutamide': ('brown', 'saddlebrown')
    }
    color1, color2 = colors[selected_drug]
    return html.Div(html.Img(src=plot_with_gradient(selected_drug, color1, color2)), style={'textAlign': 'center'})

@app.callback(
    [Output('relationship-plot', 'children'),
     Output('analysis-plot', 'children')],
    [Input('relationship-button', 'n_clicks'),
     Input('drug1-dropdown', 'value'),
     Input('drug2-dropdown', 'value')]
)
def handle_relationship_and_analysis(n_clicks, drug1, drug2):
    ctx = dash.callback_context

    if ctx.triggered and ctx.triggered[0]['prop_id'] in ['drug1-dropdown.value', 'drug2-dropdown.value']:
        return None, None

    if n_clicks > 0 and drug1 and drug2:
        def random_color():
            return '#%06x' % random.randint(0, 0xFFFFFF)

        plt.figure(figsize=(10, 6))
        sns.lineplot(x=drug1, y=drug2, data=df, marker='o', color=random_color())
        plt.title(f'Relationship between {drug1.capitalize()} and {drug2.capitalize()}', fontsize=16)
        plt.xlabel(f'{drug1.capitalize()} Usage', fontsize=14)
        plt.ylabel(f'{drug2.capitalize()} Usage', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        img_bytes = buf.getvalue()
        buf.close()
        
        relationship_plot = html.Div(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(img_bytes).decode('utf-8'))), style={'textAlign': 'center'})

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

        plt.figure(figsize=(14, 8))

        results_df_melted = results_df.reset_index().melt(id_vars='Combination', var_name='Status', value_name='Percentage')

        colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(results_df_melted['Status'].nunique())]

        sns.barplot(data=results_df_melted, x='Combination', y='Percentage', hue='Status', palette=colors, edgecolor='black')

        plt.xticks(rotation=90)
        plt.xlabel('Medication Combination', fontsize=14)
        plt.ylabel('Percentage (%)', fontsize=14)
        plt.title(f'Percentage of Readmitted Status by Combination of {drug1.capitalize()} and {drug2.capitalize()}', fontsize=16)
        plt.legend(title='Readmitted Status')
        plt.grid(True, linestyle='--', alpha=0.7)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        img_bytes = buf.getvalue()
        buf.close()
        
        analysis_plot = html.Div(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(img_bytes).decode('utf-8'))), style={'textAlign': 'center'})
        
        return relationship_plot, analysis_plot

    return None, None

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
