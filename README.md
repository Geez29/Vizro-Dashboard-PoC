
# vizro-dashboard (PoC)

This PoC contains a minimal Vizro dashboard sample, a sample multi-sheet Excel (`Cloud_Data.xlsx`), and instructions to run locally and deploy to Render (free tier).

## Folder structure
```
vizro-dashboard/
  ├─ app.py
  ├─ requirements.txt
  ├─ Cloud_Data.xlsx
  └─ README.md
```

## Quick local run (recommended)
1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run locally (dev):
   ```bash
   python app.py
   ```
4. Open your browser to `http://127.0.0.1:8050`

If `vizro` isn't installed or available in your environment, the app will print a helpful message. Replace dummy data by editing `Cloud_Data.xlsx` (keep the sheet names: `CSP`, `Services`, `Applications`, `Optimization`).

## Run with gunicorn (what Render will use)
Render expects a WSGI callable. This project exposes `server` for gunicorn to use (see `app.py`).

Start command (local test):
```bash
gunicorn app:server --bind 0.0.0.0:8050
```

On Render, use the start command below (Render injects $PORT automatically):
```
gunicorn app:server --bind 0.0.0.0:$PORT
```

## Deploy to Render (free tier) - step-by-step
1. Push this folder to a GitHub repo (e.g., `vizro-dashboard`).
2. Sign up / login to https://render.com
3. Click **New + > Web Service**.
4. Connect GitHub and choose the repo and branch (main).
5. Settings to use:
   - **Environment**: Python 3 (choose latest available)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server --bind 0.0.0.0:$PORT`
   - **Instance Type**: Free
6. Deploy. Render will build and provide a public URL. Free instances sleep after inactivity (cold start ~30-60s).

## Updating Excel data
- For PoC, you can push a new `Cloud_Data.xlsx` to the repo and Render will auto-deploy.
- For production, consider storing the Excel on OneDrive/SharePoint or moving data to a database.

## Notes & Troubleshooting
- If `gunicorn` fails to find `server`, try `gunicorn app:app` instead in Render start command.
- If performance is slow, reduce Excel size or pre-aggregate data before visualising.
- If you prefer Streamlit for hosting, adapt this code to Streamlit; but Vizro + Render generally offers better performance for non-Streamlit apps.

