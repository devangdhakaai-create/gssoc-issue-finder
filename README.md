# GSSoC Issue Finder

Find unclaimed GSSoC issues matching your skillset.

## Run Backend
```bash
cd backend
pip install fastapi uvicorn httpx
export GITHUB_TOKEN=your_token_here
uvicorn main:app --reload
```

## Run Frontend
```bash
cd frontend
npm create vite@latest . -- --template react
# Press 'y' to ignore existing files
npm install
npm run dev
```

## Usage
1. Click **Refresh Data** — fetches repos + issues
2. Enter skills (e.g. `python,react`)
3. Click **Find Issues** — filtered results dikhenge

## Add More Repos
Edit `backend/scraper.py` → `GSSOC_REPOS` list mein add karo.
