#!/usr/bin/env python3
from __future__ import annotations
import os, sys, json, subprocess, re
from pathlib import Path
from datetime import datetime, timezone
try:
    import tomllib
except Exception:
    tomllib = None

REVIEW_JSON_START, REVIEW_JSON_END = "REVIEW_START_JSON","REVIEW_END_JSON"
REVIEW_MD_START,   REVIEW_MD_END   = "REVIEW_START_MD","REVIEW_END_MD"

def run(cmd, input_text=None, check=True):
    return subprocess.run(
        cmd, input=(input_text.encode() if input_text else None),
        capture_output=True, text=False, check=check
    )


def ensure_success(result: subprocess.CompletedProcess, command: str) -> subprocess.CompletedProcess:
    if result.returncode != 0:
        err = d((result.stderr or b""))
        err = err.strip() or f"exit code {result.returncode}"
        raise RuntimeError(f"{command} failed: {err}")
    return result

def d(b: bytes) -> str:
    return b.decode("utf-8", errors="replace")

def git_root() -> Path:
    return Path(d(run(["git","rev-parse","--show-toplevel"]).stdout).strip())

def branch() -> str:
    return d(run(["git","rev-parse","--abbrev-ref","HEAD"]).stdout).strip()

def short_sha() -> str:
    cp = run(["git","rev-parse","--short","HEAD"], check=False)
    out = d(cp.stdout).strip()
    return out if out else "WORKTREE"

def staged() -> bool:
    cp = run(["git","diff","--cached","--name-only"], check=False)
    return bool(d(cp.stdout).strip())


def build_diff(diff_file: Path, base_branch: str):
    if staged():
        names_proc = ensure_success(run(["git","diff","--cached","--name-only"], check=False), "git diff --cached --name-only")
        diff_proc = ensure_success(run(["git","diff","--cached","--unified=3"], check=False), "git diff --cached --unified=3")
        names = d(names_proc.stdout).splitlines()
        diff = d(diff_proc.stdout)
    else:
        run(["git","fetch","-q","--all"], check=False)
        merge_base_cmd = f"git merge-base HEAD {base_branch}"
        mb_proc = ensure_success(run(["git","merge-base","HEAD", base_branch], check=False), merge_base_cmd)
        mb = d(mb_proc.stdout).strip()
        if not mb:
            raise RuntimeError(f"{merge_base_cmd} returned no revision")
        names_cmd = f"git diff {mb}...HEAD --name-only"
        diff_cmd = f"git diff {mb}...HEAD --unified=3"
        names_proc = ensure_success(run(["bash","-lc", names_cmd], check=False), names_cmd)
        diff_proc = ensure_success(run(["bash","-lc", diff_cmd], check=False), diff_cmd)
        names = d(names_proc.stdout).splitlines()
        diff = d(diff_proc.stdout)
    diff_file.write_text(diff, encoding="utf-8")
    return [n for n in names if n.strip()], len(diff.encode("utf-8"))

def load_cfg(p: Path) -> dict:
    if not p.exists() or tomllib is None: return {}
    with p.open("rb") as f: return tomllib.load(f)

def collect_lib(lib: Path) -> dict[str,str]:
    rd = lambda p: p.read_text(encoding="utf-8") if p.exists() else ""
    return {
        "index": rd(lib/"index.md"),
        "agents": rd(lib/"AGENTS.md"),
        "rubric_review": rd(lib/"rubrics"/"reviewer-checklist.md"),
        "rubric_pr": rd(lib/"rubrics"/"pr-checklist.md"),
        "style_py": rd(lib/"style"/"python.md"),
        "style_js": rd(lib/"style"/"js-ts.md"),
        "style_go": rd(lib/"style"/"go.md"),
        "asvs": rd(lib/"security"/"asvs.md"),
        "refactor": rd(lib/"patterns"/"refactoring-catalog.md"),
        "tmpl_exec": rd(lib/"templates"/"review.exec.md"),
    }

def build_prompt(tmpl:str, meta:dict, diff_text:str, lib:dict[str,str]) -> str:
    parts = [
        tmpl,
        "\n\n# META\n", json.dumps(meta, indent=2),
        "\n\n# DIFF PATCH\n```diff\n", diff_text, "\n```\n",
        "\n# LIBRARY INDEX\n", lib["index"],
        "\n# RUBRICS\n", lib["rubric_review"], "\n", lib["rubric_pr"],
        "\n# STYLE\n## Python\n", lib["style_py"], "\n## JS/TS\n", lib["style_js"], "\n## Go\n", lib["style_go"],
        "\n# SECURITY (ASVS)\n", lib["asvs"],
        "\n# REFACTORING PATTERNS\n", lib["refactor"]
    ]
    return "".join(parts)

def extract_between(text:str, start:str, end:str) -> str|None:
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), text, re.DOTALL)
    return m.group(1).strip() if m else None

def main():
    repo = git_root(); os.chdir(repo)
    lib_dir = repo/".codex-review"; out_dir = repo/"var"/"reviews"; in_dir = repo/"var"/"_codex_input"
    out_dir.mkdir(parents=True, exist_ok=True); in_dir.mkdir(parents=True, exist_ok=True)

    cfg        = load_cfg(lib_dir/"config.toml")
    codex_cfg  = cfg.get("codex",{})
    gate_cfg   = cfg.get("gating",{})
    review_cfg = cfg.get("review",{})

    base_branch = review_cfg.get("base_branch","origin/main")
    if len(sys.argv)>1 and not sys.argv[1].startswith("-"):
        base_branch = sys.argv[1]

    br = branch(); sha = short_sha(); ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    diff_file = in_dir/"diff.patch"
    changed, diff_bytes = build_diff(diff_file, base_branch)
    diff_text = diff_file.read_text(encoding="utf-8")

    meta = {
        "branch": br, "short_sha": sha, "timestamp_utc": ts,
        "base_branch": base_branch, "changed_files": changed, "diff_bytes": diff_bytes,
        "include_categories": review_cfg.get("include_categories",[])
    }
    (in_dir/"meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    lib = collect_lib(lib_dir)
    prompt = build_prompt(lib["tmpl_exec"], meta, diff_text, lib)
    (in_dir/"prompt.txt").write_text(prompt, encoding="utf-8")

    # Build codex exec command
    help_txt = d(run(["codex","--help"], check=False).stdout or b"")
    cmd = ["codex","exec"]
    if "--model" in help_txt and codex_cfg.get("model"): cmd += ["--model", str(codex_cfg["model"])]
    if "--reasoning" in help_txt and codex_cfg.get("reasoning"): cmd += ["--reasoning", str(codex_cfg["reasoning"])]
    if "--approval-mode" in help_txt and codex_cfg.get("approval_mode"): cmd += ["--approval-mode", str(codex_cfg["approval_mode"])]
    if "--max-output-tokens" in help_txt and codex_cfg.get("max_output_tokens"): cmd += ["--max-output-tokens", str(codex_cfg["max_output_tokens"])]

    cp = run(cmd, input_text=prompt, check=False)
    stdout = d(cp.stdout); (in_dir/"raw.txt").write_text(stdout, encoding="utf-8")

    report_md   = out_dir/f"{br}_{sha}_{ts}.md"
    report_json = out_dir/f"{br}_{sha}_{ts}.json"

    js = extract_between(stdout, REVIEW_JSON_START, REVIEW_JSON_END)
    md = extract_between(stdout, REVIEW_MD_START, REVIEW_MD_END)

    if js: report_json.write_text(js, encoding="utf-8")
    if md: report_md.write_text(md, encoding="utf-8")
    if not md: report_md.write_text(stdout, encoding="utf-8")

    # Gating
    threshold = int(gate_cfg.get("fail_on_priority_max", 1))
    triggered = False
    if report_json.exists():
        try:
            obj = json.loads(report_json.read_text(encoding="utf-8"))
            pri = [f.get("priority", None) for f in obj.get("findings",[])]
            pri = [p for p in pri if isinstance(p,int)]
            if pri and min(pri) <= threshold:
                triggered = True
        except Exception:
            pass
    if not triggered:
        # Fallback: severity tokens in MD
        sev_tokens = [s.upper() for s in gate_cfg.get("fail_on_severity", ["HIGH"])]
        md_txt = report_md.read_text(encoding="utf-8")
        if any(f"[{tok}]" in md_txt for tok in sev_tokens):
            triggered = True

    print(f"Report: {report_md}")
    if report_json.exists(): print(f"JSON:   {report_json}")
    if triggered:
        print(f"Failing due to priority/severity policy.")
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
    except subprocess.CalledProcessError as exc:
        print(exc.stderr.decode("utf-8", errors="replace"), file=sys.stderr)
        sys.exit(exc.returncode)
