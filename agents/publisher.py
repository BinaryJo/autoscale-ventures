import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "infra" / "site"
POSTS = SITE / "posts"
SITEMAP = SITE / "sitemap.xml"
OPENAPI = ROOT / "infra" / "openapi"

def deploy_assets(_artifacts):
    POSTS.mkdir(parents=True, exist_ok=True)
    urls = []
    for html in sorted(POSTS.glob("*.html")):
        path = str(html).split("/infra/site")[-1]
        urls.append(path)
    body = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"]
    for u in urls:
        body += ["  <url>", f"    <loc>{u}</loc>", f"    <lastmod>{datetime.utcnow().date()}</lastmod>", "  </url>"]
    body += ["</urlset>"]
    SITEMAP.parent.mkdir(parents=True, exist_ok=True)
    SITEMAP.write_text("\n".join(body), encoding="utf-8")

    OPENAPI.mkdir(parents=True, exist_ok=True)
    def write_openapi(name, path, summary, params):
        spec = {"openapi":"3.0.2","info":{"title":f"{name} API","version":"1.0.0"},
                "paths":{path:{"get":{"summary":summary,"parameters":params,"responses":{"200":{"description":"OK"}}}}}}
        (OPENAPI / f"{name}.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")
    write_openapi("slugify","/api/convert/slugify","Convert text into a URL-friendly slug",
                  [{"name":"text","in":"query","required":False,"schema":{"type":"string"}}])
    write_openapi("csv2json","/api/convert/csv2json","Convert CSV to JSON",
                  [{"name":"csv","in":"query","required":False,"schema":{"type":"string"}}])
    write_openapi("tzslots","/api/slots","Generate time slots from a start time",
                  [{"name":"tz","in":"query","required":False,"schema":{"type":"string"}},
                   {"name":"start","in":"query","required":True,"schema":{"type":"string"}},
                   {"name":"blocks","in":"query","required":False,"schema":{"type":"integer"}},
                   {"name":"block_minutes","in":"query","required":False,"schema":{"type":"integer"}}])
    write_openapi("schedule","/api/schedule","Generate recurring schedule dates",
                  [{"name":"period","in":"query","required":True,"schema":{"type":"string"}},
                   {"name":"start","in":"query","required":True,"schema":{"type":"string"}},
                   {"name":"count","in":"query","required":False,"schema":{"type":"integer"}}])
    print("[publisher] site sitemap and OpenAPI stubs updated")
