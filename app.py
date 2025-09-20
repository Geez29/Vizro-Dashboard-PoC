import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# -------- Load Excel Data --------
excel_file = "Cloud_Actual_Optimization.xlsx"

def load_sheet(sheet_name):
    try:
        return pd.read_excel(excel_file, sheet_name=sheet_name)
    except:
        # Dummy data if Excel missing
        if sheet_name == "Services":
            return pd.DataFrame({
                "Service": ["Compute", "Database", "Storage", "Networking", "Analytics"],
                "Cost": [12000, 8500, 6000, 4000, 3000]
            })
        elif sheet_name == "CSP":
            return pd.DataFrame({
                "CSP": ["AWS", "Azure", "GCP"],
                "ServicesSpend": [7000, 5000, 3000],
                "MarketplaceSpend": [2000, 1500, 1000]
            })
        elif sheet_name == "Applications":
            return pd.DataFrame({
                "Application": ["App1", "App2", "App3", "App4"],
                "Cost": [7000, 5000, 6000, 4000]
            })
        return pd.DataFrame()

# -------- Initialize Dash App --------
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # for Render

# McKinsey-style color palette
colors = {
    "background": "#ffffff",
    "text": "#003366",
    "primary": "#005eb8",
    "light_blue": "#cce6ff"
}

# -------- Layout --------
app.layout = html.Div([
    html.H1("Cloud Cost Dashboard", style={"font-family": "Aptos, Calibri", "color": colors["text"]}),
    dcc.Tabs(id="tabs", value="tab-csp", children=[
        dcc.Tab(label="CSP", value="tab-csp"),
        dcc.Tab(label="Services", value="tab-services"),
        dcc.Tab(label="Applications", value="tab-apps"),
    ]),
    html.Div(id="tab-content")
])

# -------- Callback to Update Tabs --------
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "tab-csp":
        df = load_sheet("CSP")

        # Vertical Bar Chart for all CSP
        bar_fig = px.bar(
            df, x="CSP", y=["ServicesSpend", "MarketplaceSpend"],
            title="CSP Total Cost",
            labels={"value": "Cost ($)", "CSP": "Cloud Provider"},
            color_discrete_sequence=[colors["primary"], colors["light_blue"]]
        )

        # Waterfall chart - Services Spend
        waterfall_services = go.Figure(go.Waterfall(
            name="Services Spend",
            orientation="v",
            x=df["CSP"],
            y=df["ServicesSpend"],
            text=[f"${v}" for v in df["ServicesSpend"]],
            textposition="outside",
            decreasing={"marker":{"color": colors["light_blue"]}},
            increasing={"marker":{"color": colors["primary"]}},
            totals={"marker":{"color": colors["primary"]}}
        ))
        waterfall_services.update_layout(title="CSP Services Spend", font={"family": "Aptos, Calibri"})

        # Waterfall chart - Marketplace Spend
        waterfall_market = go.Figure(go.Waterfall(
            name="Marketplace Spend",
            orientation="v",
            x=df["CSP"],
            y=df["MarketplaceSpend"],
            text=[f"${v}" for v in df["MarketplaceSpend"]],
            textposition="outside",
            decreasing={"marker":{"color": colors["light_blue"]}},
            increasing={"marker":{"color": colors["primary"]}},
            totals={"marker":{"color": colors["primary"]}}
        ))
        waterfall_market.update_layout(title="CSP Marketplace Spend", font={"family": "Aptos, Calibri"})

        return html.Div([
            html.Div([
                dcc.Graph(figure=bar_fig)
            ], style={"width": "100%"}),
            html.Div([
                html.Div(dcc.Graph(figure=waterfall_services), style={"width": "49%", "display": "inline-block"}),
                html.Div(dcc.Graph(figure=waterfall_market), style={"width": "49%", "display": "inline-block", "float": "right"})
            ])
        ])
    
    elif tab == "tab-services":
        df = load_sheet("Services")
        # Simplified Heatmap with text annotation
        heat_fig = go.Figure(data=go.Heatmap(
            z=df["Cost"],
            x=df["Service"],
            y=["Cost"]*len(df),
            colorscale=[[0, colors["light_blue"]], [1, colors["primary"]]],
            showscale=True
        ))
        # Add annotations for value display
        for i, val in enumerate(df["Cost"]):
            heat_fig.add_annotation(
                x=df["Service"][i],
                y="Cost",
                text=f"${val}",
                showarrow=False,
                font={"color": "black", "family": "Aptos, Calibri"}
            )
        heat_fig.update_layout(title="Service Cost Heatmap", font={"family": "Aptos, Calibri"})

        return html.Div([
            dcc.Graph(figure=heat_fig)
        ])

    elif tab == "tab-apps":
        df = load_sheet("Applications")
        fig_bar = px.bar(
            df, x="Application", y="Cost",
            title="Cost by Application",
            color_discrete_sequence=[colors["primary"]],
            labels={"Cost": "Cost ($)"}
        )
        fig_bar.update_layout(font={"family": "Aptos, Calibri"})
        return dcc.Graph(figure=fig_bar)
    
    return html.Div("No data available")

# -------- Run App --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)
