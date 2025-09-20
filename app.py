import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# -------- Load Excel Data --------
excel_file = "Cloud_Actual_Optimization.xlsx"

def load_sheet(sheet_name):
    try:
        return pd.read_excel(excel_file, sheet_name=sheet_name)
    except:
        # Dummy data if Excel missing
        if sheet_name == "Services":
            return pd.DataFrame({
                "Service": ["Compute", "Database", "Storage", "Networking"],
                "Cost": [12000, 8500, 6000, 4000]
            })
        elif sheet_name == "CSP":
            return pd.DataFrame({
                "CSP": ["AWS", "Azure", "GCP"],
                "Cost": [15000, 10000, 5000]
            })
        elif sheet_name == "Applications":
            return pd.DataFrame({
                "Application": ["App1", "App2", "App3"],
                "Cost": [7000, 5000, 6000]
            })
        return pd.DataFrame()

# -------- Initialize App --------
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # for Render deployment

# -------- App Layout --------
app.layout = html.Div([
    html.H1("Cloud Cost Dashboard"),
    dcc.Tabs(id="tabs", value="tab-services", children=[
        dcc.Tab(label="Services", value="tab-services"),
        dcc.Tab(label="CSP", value="tab-csp"),
        dcc.Tab(label="Applications", value="tab-apps"),
    ]),
    html.Div(id="tab-content")
])

# -------- Callbacks to Update Tabs --------
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "tab-services":
        df = load_sheet("Services")
        fig_bar = px.bar(df, x="Service", y="Cost", title="Cost by Service")
        fig_pie = px.pie(df, names="Service", values="Cost", title="Service Cost Distribution")
        return html.Div([
            dcc.Graph(figure=fig_bar),
            dcc.Graph(figure=fig_pie)
        ])
    elif tab == "tab-csp":
        df = load_sheet("CSP")
        fig = px.bar(df, x="CSP", y="Cost", title="Cost by CSP")
        return dcc.Graph(figure=fig)
    elif tab == "tab-apps":
        df = load_sheet("Applications")
        fig = px.bar(df, x="Application", y="Cost", title="Cost by Application")
        return dcc.Graph(figure=fig)
    return html.Div("No data")

# -------- Run App --------
if __name__ == "__main__":
    app.run(debug=True)   # ✅ updated for Dash 3.x

