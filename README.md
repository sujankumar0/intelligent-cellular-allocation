# Intelligent Cellular Channel Allocation Under Variable Traffic

A runnable Streamlit prototype for demonstrating traffic-aware cellular channel allocation.

## Features
- Six-cell cellular interference graph.
- Synthetic low, medium, high, mixed, and sudden-spike traffic scenarios.
- Random Forest traffic prediction.
- A small tabular Q-learning policy to select target channel counts.
- Greedy graph-based channel assignment that prevents direct neighboring cells from sharing a channel.
- Comparison of Fixed Channel Allocation (FCA), Dynamic Channel Allocation (DCA), and the proposed prediction + Q-learning approach.
- Dashboard charts for traffic and performance metrics.

## Requirements
- Python 3.10 or newer (Python 3.12 recommended).
- Internet connection for the first-time Python package installation.

## Run on Ubuntu / Linux

```bash
unzip intelligent-cellular-allocation.zip
cd intelligent-cellular-allocation

python3 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`. Open it in your browser.

## Run on Windows PowerShell

```powershell
py -3 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, use:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## Suggested examiner demonstration
1. Select **Low** traffic and observe channel assignments.
2. Select **High** traffic and compare demand and blocking.
3. Select **Sudden spike** and observe the changed BS1/BS4 demand.
4. Open **Channel allocation** and show assigned channel IDs.
5. Open **Performance comparison** and compare FCA, DCA, and proposed allocation.
6. Change the channel pool in the sidebar and observe the effect.

## Important academic limitations
This is a teaching-scale logical resource-allocation simulation. It uses synthetic traffic and a simplified neighbor-interference rule. It is not a full LTE/5G physical-layer simulator and does not calculate SINR, propagation loss, fading, handover, or real radio scheduling. Performance values are simulator outputs under stated assumptions, not measurements from a live cellular network.

For a stronger research study, run repeated experiments over many random seeds, document the assumptions, add statistical summaries, and consider NS-3 for detailed packet-level wireless simulation.
