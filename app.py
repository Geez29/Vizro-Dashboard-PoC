
import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

def load_sheet(sheet_name):
    if sheet_name=="Services":
        return pd.DataFrame({"Service":["Compute","Database","Storage"],"Cost":[12000,8500,6000]})
    elif sheet_name=="CSP":
        return pd.DataFrame({"CSP":["AWS","Azure","GCP"],"ServicesSpend":[7000,5000,3000],"MarketplaceSpend":[2000,1500,1000]})
    elif sheet_name=="Applications":
        return pd.DataFrame({"Application":["App1","App2","App3"],"Cost":[7000,5000,6000]})
    return pd.DataFrame()

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
colors = {"primary":"#005eb8","light_blue":"#cce6ff","text":"#003366"}

app.layout = html.Div([
    html.H1("Cloud Cost Dashboard", style={"font-family":"Aptos, Calibri","color":colors["text"]}),
    dcc.Tabs(id="tabs", value="tab-csp", children=[
        dcc.Tab(label="CSP", value="tab-csp"),
        dcc.Tab(label="Services", value="tab-services"),
        dcc.Tab(label="Applications", value="tab-apps"),
    ]),
    html.Div(id="tab-content")
])

@app.callback(Output("tab-content","children"), Input("tabs","value"))
def render_tab(tab):
    if tab=="tab-csp":
        df = load_sheet("CSP")
        bar_fig = px.bar(df, x="CSP", y=["ServicesSpend","MarketplaceSpend"], color_discrete_sequence=[colors["primary"],colors["light_blue"]], title="CSP Total Cost")
        wf_s = go.Figure(go.Waterfall(x=df["CSP"], y=df["ServicesSpend"], text=[f"${v}" for v in df["ServicesSpend"]], textposition="outside", decreasing={"marker":{"color":colors["light_blue"]}}, increasing={"marker":{"color":colors["primary"]}}, totals={"marker":{"color":colors["primary"]}}))
        wf_s.update_layout(title="Services Spend", font={"family":"Aptos, Calibri"})
        wf_m = go.Figure(go.Waterfall(x=df["CSP"], y=df["MarketplaceSpend"], text=[f"${v}" for v in df["MarketplaceSpend"]], textposition="outside", decreasing={"marker":{"color":colors["light_blue"]}}, increasing={"marker":{"color":colors["primary"]}}, totals={"marker":{"color":colors["primary"]}}))
        wf_m.update_layout(title="Marketplace Spend", font={"family":"Aptos, Calibri"})
        return html.Div([html.Div(dcc.Graph(figure=bar_fig)), html.Div([html.Div(dcc.Graph(figure=wf_s), style={"width":"49%","display":"inline-block"}), html.Div(dcc.Graph(figure=wf_m), style={"width":"49%","display":"inline-block","float":"right"})])])
    elif tab=="tab-services":
        df = load_sheet("Services")
        heat_fig = go.Figure(go.Heatmap(z=df["Cost"], x=df["Service"], y=["Cost"]*len(df), colorscale=[[0,colors["light_blue"]],[1,colors["primary"]]], showscale=True))
        for i,v in enumerate(df["Cost"]):
            heat_fig.add_annotation(x=df["Service"][i], y="Cost", text=f"${v}", showarrow=False, font={"family":"Aptos, Calibri"})
        heat_fig.update_layout(title="Service Cost Heatmap", font={"family":"Aptos, Calibri"})
        return html.Div([dcc.Graph(figure=heat_fig)])
    elif tab=="tab-apps":
        df = load_sheet("Applications")
        fig = px.bar(df, x="Application", y="Cost", color_discrete_sequence=[colors["primary"]], title="Cost by Application")
        fig.update_layout(font={"family":"Aptos, Calibri"})
        return dcc.Graph(figure=fig)
    return html.Div("No data available")

if __name__=="__main__":
    port = int(os.environ.get("PORT",8050))
    app.run(debug=False, host="0.0.0.0", port=port)
