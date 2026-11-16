"""Snapshot one public source with a timeout, timing and a transport audit."""

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from time import perf_counter
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS = ROOT / "data" / "source_snapshots"
DEADLINE = datetime.fromisoformat("2026-11-16T04:30:00+00:00")


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript", "svg"}:
            self.hidden += 1
        if not self.hidden and tag in {"p", "li", "div", "h1", "h2", "h3", "h4", "br", "tr", "time"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "svg"}:
            self.hidden = max(0, self.hidden - 1)
        if not self.hidden and tag in {"p", "li", "div", "h1", "h2", "h3", "h4", "tr", "time"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

    def text(self):
        lines = [re.sub(r"\s+", " ", line).strip() for line in "".join(self.parts).splitlines()]
        return "\n".join(line for line in lines if line) + "\n"


def check_source(slug, url):
    remaining = (DEADLINE - datetime.now(timezone.utc)).total_seconds()
    if remaining <= 0:
        raise TimeoutError("The real Monday 10:00 AM IST submission deadline has been reached.")
    if not re.fullmatch(r"[a-z0-9_]+", slug) or not url.startswith("https://"):
        raise ValueError("Use a simple source slug and a public HTTPS URL.")
    audit_path = SNAPSHOTS / f"{slug}.json"
    if audit_path.is_file():
        audit = json.loads(audit_path.read_text())
        if audit["source_url"] != url:
            raise ValueError("Existing source slug has a different URL; do not overwrite it.")
        print(f"{slug}: snapshot cache hit; HTTP {audit.get('http_status')}; no network request; elapsed seconds: 0.000")
        return
    audit = {"source_id": slug, "source_url": url, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
             "http_status": None, "error": None, "semantic_review": "pending"}
    raw_root = Path("/tmp/opencode/agent-network-source-html")
    raw_root.mkdir(parents=True, exist_ok=True)
    raw_path = raw_root / f"{slug}.html"
    started = perf_counter()
    html = None
    try:
        result = subprocess.run(
            ["curl", "--silent", "--show-error", "--location", "--retry", "0",
             "--connect-timeout", "5", "--max-time", str(min(15.0, remaining)),
             "--max-filesize", "3000000", "--user-agent", "Mozilla/5.0",
             "--output", str(raw_path), "--write-out", "%{http_code}\n%{url_effective}", url],
            capture_output=True, text=True, timeout=min(18.0, remaining),
        )
        fields = result.stdout.splitlines()
        audit.update(http_status=int(fields[0]) if fields and fields[0].isdigit() else None,
                     final_url=fields[1] if len(fields) > 1 else url)
        if result.returncode:
            audit["error"] = f"curl_exit_{result.returncode}"
        elif audit["http_status"] == 200:
            html = raw_path.read_text(encoding="utf-8", errors="replace")
        else:
            audit["error"] = "non_200_status"
    except Exception as error:
        audit["error"] = type(error).__name__
    finally:
        audit["elapsed_s"] = perf_counter() - started
        print(f"{slug}: HTTP {audit['http_status']}; error {audit['error']}; elapsed seconds: {audit['elapsed_s']:.3f}", flush=True)
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    if html is not None:
        parser = VisibleText()
        parser.feed(html)
        text = parser.text()
        snapshot = SNAPSHOTS / f"{slug}.txt"
        snapshot.write_text(text, encoding="utf-8")
        audit.update(snapshot_path=str(snapshot.relative_to(ROOT)),
                     snapshot_sha256=hashlib.sha256(text.encode()).hexdigest())
        print("Visible source text saved; HTTP success alone does not verify a claim.")
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("slug")
    arguments.add_argument("url")
    values = arguments.parse_args()
    check_source(values.slug, values.url)
