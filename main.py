import json
import logging
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.my_config import Config
from app.services import reddit_service
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {
        "debug_mode": Config.DEBUG,
        "results_json": None
    })


@app.post("/", response_class=HTMLResponse)
async def analyze(request: Request, json_data: str = Form(...)):
    try:
        data = json.loads(json_data)
        items = data.get("items", [])
        limit = data.get("limit", 25)

        final_output = {}
        for item in items:
            sub_raw = item.get("subreddit", "")
            kws = item.get("keywords", [])

            filtered = reddit_service.fetch_and_filter(sub_raw, kws, limit)

            clean = sub_raw.replace("r/", "").strip("/")
            final_output[f"/r/{clean}"] = filtered

        res_json = json.dumps(final_output, indent=2, ensure_ascii=False)
        logging.info(f"Analysis complete:\n{res_json}")

        return templates.TemplateResponse(request, "index.html", {
            "debug_mode": Config.DEBUG,
            "results_json": res_json,
            "results_dict": final_output,
            "request": request
        })

    except Exception as e:
        logging.error(f"Error: {e}")
        return templates.TemplateResponse(request, "index.html", {
            "debug_mode": Config.DEBUG,
            "results_json": json.dumps({"error": str(e)}),
            "results_dict": {},
            "request": request
        })
