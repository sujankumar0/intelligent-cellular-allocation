

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx

from simulation.network import create_network
from simulation.traffic_generator import current_loads, generate_traffic
from models.traffic_prediction import predict_demands
from simulation.channel_allocator import allocate_fca, allocate_dca, allocate_proposed
from simulation.metrics import calculate_metrics
from simulation.interference import count_interference_violations

st.set_page_config(page_title="Intelligent Cellular Channel Allocation", page_icon="📡", layout="wide")

st.title("📡 Intelligent Cellular Channel Allocation")
st.caption("Simulation of traffic-aware channel assignment with prediction and interference constraints")

with st.sidebar:
    st.header("Simulation controls")
    traffic_mode = st.selectbox("Traffic scenario", ["Mixed", "Low", "Medium", "High", "Sudden spike"])
    seed = st.number_input("Random seed", min_value=1, max_value=9999, value=42, step=1)
    total_channels = st.slider("Total channel pool", 12, 36, 24, 2)
    users_per_channel = st.slider("Users supported per channel (display metric)", 5, 25, 13)
    st.info("This is a software simulation using synthetic traffic. It does not connect to a real cellular network.")

loads = current_loads(traffic_mode, int(seed))
predicted = predict_demands(loads, int(seed))
graph = create_network()

fca = allocate_fca(graph, loads, total_channels)
dca = allocate_dca(graph, loads, total_channels)
proposed, requested = allocate_proposed(graph, predicted, loads, total_channels)

def metrics_for(assignments):
    m = calculate_metrics(graph, loads, assignments, users_per_channel)
    m["interference_violations"] = count_interference_violations(graph, assignments)
    return m

results = {
    "Fixed Channel Allocation": metrics_for(fca),
    "Dynamic Channel Allocation": metrics_for(dca),
    "Proposed AI-based Allocation": metrics_for(proposed),
}

st.subheader("Network overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Base stations", "6")
c2.metric("Channel pool", total_channels)
c3.metric("Total active users", sum(loads.values()))
c4.metric("Traffic scenario", traffic_mode)

tab1, tab2, tab3, tab4 = st.tabs(["Network topology", "Channel allocation", "Performance comparison", "How it works"])

with tab1:
    left, right = st.columns([1.2, 1])
    with left:
        pos = nx.spring_layout(graph, seed=9)
        edge_x, edge_y = [], []
        for a, b in graph.edges:
            x0, y0 = pos[a]; x1, y1 = pos[b]
            edge_x += [x0, x1, None]; edge_y += [y0, y1, None]
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=2, color="#8aa0b8"), hoverinfo="none"))
        node_x = [pos[n][0] for n in graph.nodes]
        node_y = [pos[n][1] for n in graph.nodes]
        node_text = [f"{n}<br>Users: {loads[n]}<br>Predicted: {predicted[n]:.0f}" for n in graph.nodes]
        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode="markers+text", text=list(graph.nodes),
                                 textposition="bottom center", hovertext=node_text, hoverinfo="text",
                                 marker=dict(size=38, color=[loads[n] for n in graph.nodes],
                                             colorscale="YlOrRd", showscale=True,
                                             colorbar=dict(title="Users"), line=dict(width=2, color="white"))))
        fig.update_layout(title="Cell adjacency / interference graph", height=440, margin=dict(l=10,r=10,t=50,b=10),
                          xaxis=dict(visible=False), yaxis=dict(visible=False), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        load_df = pd.DataFrame({"Base station": list(loads.keys()), "Actual users": list(loads.values()),
                                "Predicted users": [round(predicted[k], 1) for k in loads]})
        st.dataframe(load_df, hide_index=True, use_container_width=True)
        fig2 = px.bar(load_df, x="Base station", y=["Actual users", "Predicted users"], barmode="group",
                      title="Actual vs predicted traffic")
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    selected = st.selectbox("Allocation algorithm", list(results.keys()), index=2)
    mapping = {
        "Fixed Channel Allocation": fca,
        "Dynamic Channel Allocation": dca,
        "Proposed AI-based Allocation": proposed
    }[selected]
    allocation_df = pd.DataFrame([
        {"Base station": cell, "Active users": loads[cell],
         "Predicted users": round(predicted[cell], 1),
         "Requested channels": requested.get(cell, 4 if selected == "Fixed Channel Allocation" else 0),
         "Assigned channels": len(mapping[cell]),
         "Channel IDs": ", ".join(map(str, mapping[cell])) or "None"}
        for cell in graph.nodes
    ])
    st.dataframe(allocation_df, hide_index=True, use_container_width=True)
    st.caption("Neighboring base stations are connected in the topology graph and are prevented from sharing the same channel.")

with tab3:
    metric = st.selectbox("Metric to compare", [
        "channel_utilization_pct", "throughput_units", "blocking_probability_pct",
        "fairness_index", "allocated_channels", "interference_violations"
    ], format_func=lambda x: {
        "channel_utilization_pct":"Channel utilization (%)",
        "throughput_units":"Throughput (normalized units)",
        "blocking_probability_pct":"Blocking probability (%)",
        "fairness_index":"Jain fairness index",
        "allocated_channels":"Allocated channels",
        "interference_violations":"Interference violations"
    }[x])
    compare_df = pd.DataFrame([{"Algorithm": name, metric: values[metric]} for name, values in results.items()])
    fig3 = px.bar(compare_df, x="Algorithm", y=metric, color="Algorithm", title="Algorithm comparison")
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(pd.DataFrame(results).T, use_container_width=True)
    st.warning("Results are generated by this simulator's simplified assumptions. Use repeated seeds and scenarios for research-grade comparisons.")

with tab4:
    st.markdown("""
    **1. Traffic generation:** creates synthetic active-user demand for six cells.

    **2. Random Forest prediction:** estimates near-future demand from generated historical-style features.

    **3. Q-Learning policy:** selects a target channel count using a small tabular policy trained in a simulated reward environment.

    **4. Graph-based channel assignment:** assigns channel IDs while preventing direct neighbors from sharing a channel.

    **5. Evaluation:** compares fixed, demand-based dynamic, and proposed prediction-plus-Q-learning allocation using utilization, throughput, blocking, fairness, and interference metrics.

    **Important scope note:** this prototype models logical channel allocation and neighbor interference. It does not model RF propagation, SINR, fading, handover, or standards-compliant LTE/5G physical layers.
    """)

st.divider()
st.caption("Project prototype • Synthetic data • Six-cell interference graph • For academic demonstration")
