#!/usr/bin/env python3
"""
Smart Git Diff & Pre-Push Duplicate Detector
=============================================
Repository Target: https://github.com/Dhruvgupta1015/Matrusetu

Detects file-level and AST function-level duplicates between the local codebase
and the remote GitHub repository. Skips redundant/duplicate code and pushes
only genuinely modified or brand-new code.
"""

import ast
import argparse
import hashlib
import os
import re
import subprocess
import sys
from typing import Dict, List, Optional, Set, Tuple

# Ensure Windows terminal handles UTF-8 correctly
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TARGET_REPO_URL = "https://github.com/Dhruvgupta1015/Matrusetu.git"
DEFAULT_REMOTE_NAME = "upstream"
DEFAULT_BRANCH = "main"

# ANSI Terminal Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def run_git(args: List[str], cwd: Optional[str] = None) -> Tuple[int, str, str]:
    """Execute a git command and return (exit_code, stdout, stderr)."""
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def get_git_root() -> str:
    """Return absolute path to Git repository root."""
    code, out, err = run_git(["rev-parse", "--show-toplevel"])
    if code != 0:
        print(f"{RED}Error: Not inside a Git repository.{RESET}")
        sys.exit(1)
    return os.path.abspath(out)


def ensure_remote(git_root: str, remote_name: str, remote_url: str):
    """Ensure the target remote exists and points to the right URL."""
    code, out, _ = run_git(["remote", "-v"], cwd=git_root)
    remotes = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            remotes[parts[0]] = parts[1]

    if remote_name in remotes:
        if remotes[remote_name] != remote_url and not remotes[remote_name].startswith(remote_url.rstrip(".git")):
            print(f"{YELLOW}Updating remote '{remote_name}' URL to {remote_url}{RESET}")
            run_git(["remote", "set-url", remote_name, remote_url], cwd=git_root)
    else:
        print(f"{CYAN}Adding remote '{remote_name}' -> {remote_url}{RESET}")
        run_git(["remote", "add", remote_name, remote_url], cwd=git_root)


def fetch_remote(git_root: str, remote_name: str, branch: str) -> str:
    """Fetch remote branch without altering working tree. Returns commit SHA."""
    print(f"{CYAN}📡 Fetching latest tree from {remote_name}/{branch}...{RESET}")
    code, _, err = run_git(["fetch", remote_name, branch], cwd=git_root)
    if code != 0:
        print(f"{YELLOW}Warning during fetch: {err}{RESET}")

    # Resolve remote commit SHA
    code, out, _ = run_git(["rev-parse", f"{remote_name}/{branch}"], cwd=git_root)
    if code != 0:
        code, out, _ = run_git(["rev-parse", "FETCH_HEAD"], cwd=git_root)
        if code != 0:
            print(f"{RED}Error: Could not resolve remote branch {remote_name}/{branch}.{RESET}")
            sys.exit(1)
    return out


def get_remote_file_content(git_root: str, remote_ref: str, file_path: str) -> Optional[str]:
    """Retrieve content of a file from remote git tree."""
    # Try direct path and alternative path (handling nested 'matrubhasa/' prefix or lack thereof)
    candidates = [file_path.replace("\\", "/")]
    if candidates[0].startswith("matrubhasa/"):
        candidates.append(candidates[0][len("matrubhasa/"):])
    else:
        candidates.append(f"matrubhasa/{candidates[0]}")

    for cand in candidates:
        code, out, _ = run_git(["show", f"{remote_ref}:{cand}"], cwd=git_root)
        if code == 0:
            return out
    return None


def get_remote_files(git_root: str, remote_ref: str) -> Dict[str, str]:
    """Returns a dict of {remote_path: blob_sha} from the remote tree."""
    code, out, _ = run_git(["ls-tree", "-r", remote_ref], cwd=git_root)
    files = {}
    if code == 0:
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 4:
                blob_sha = parts[2]
                path = parts[3]
                files[path] = blob_sha
    return files


def normalize_content(content: str) -> str:
    """Normalize line endings and trailing whitespace."""
    lines = [line.rstrip() for line in content.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip()


def compute_hash(content: str) -> str:
    """SHA-256 of normalized content."""
    return hashlib.sha256(normalize_content(content).encode("utf-8")).hexdigest()


class ASTNormalizer(ast.NodeTransformer):
    """Normalizes Python AST for invariant comparison (ignores line numbers, docstrings, formatting)."""
    def visit_Expr(self, node):
        # Ignore standalone docstrings in functions/classes
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return None
        return self.generic_visit(node)


def extract_python_blocks(code_str: str) -> Dict[str, Tuple[str, str]]:
    """
    Parse Python code and extract {symbol_name: (ast_dump_hash, raw_source_snippet)}.
    Captures top-level and class functions/methods.
    """
    blocks = {}
    try:
        tree = ast.parse(code_str)
    except SyntaxError:
        return blocks

    normalizer = ASTNormalizer()

    def process_node(node, prefix=""):
        name = getattr(node, "name", None)
        if not name:
            return

        full_name = f"{prefix}{name}"
        normalized_tree = normalizer.visit(ast.fix_missing_locations(node))
        dump_repr = ast.dump(normalized_tree, annotate_fields=False, include_attributes=False)
        block_hash = hashlib.sha256(dump_repr.encode("utf-8")).hexdigest()

        try:
            source_segment = ast.get_source_segment(code_str, node) or ""
        except Exception:
            source_segment = ""

        blocks[full_name] = (block_hash, source_segment)

        # Traverse nested methods inside classes
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    process_node(child, prefix=f"{full_name}.")

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            process_node(node)

    return blocks


def get_local_tracked_and_untracked(git_root: str) -> List[str]:
    """Get all local files (tracked modified, staged, and untracked), ignoring .git and venv."""
    files = []
    # Status check
    code, out, _ = run_git(["status", "--porcelain", "-uall"], cwd=git_root)
    if code == 0:
        for line in out.splitlines():
            if not line.strip():
                continue
            status = line[:2]
            filepath = line[3:].strip()
            # Clean quotes if any
            if filepath.startswith('"') and filepath.endswith('"'):
                filepath = filepath[1:-1]
            
            # Skip ignored directories like venv, .env, __pycache__, .git
            parts = filepath.replace("\\", "/").split("/")
            if any(p in ["venv", ".git", "__pycache__", ".venv", "node_modules", ".env"] for p in parts):
                continue
            if filepath.endswith((".pyc", ".DS_Store")):
                continue
            files.append(filepath.replace("\\", "/"))
    return files


def analyze_diff(git_root: str, remote_ref: str) -> Dict:
    """Analyze local files vs remote tree for duplicates and genuine modifications."""
    remote_tree_files = get_remote_files(git_root, remote_ref)
    local_files = get_local_tracked_and_untracked(git_root)

    results = {
        "identical_files_skipped": [],
        "genuine_modified_files": [],
        "brand_new_files": [],
        "python_ast_analysis": {},
    }

    # Also compute hashes of all remote files for cross-file duplicate detection
    remote_hashes = {}
    for r_path in remote_tree_files:
        content = get_remote_file_content(git_root, remote_ref, r_path)
        if content is not None:
            remote_hashes[compute_hash(content)] = r_path

    for rel_path in local_files:
        full_path = os.path.join(git_root, rel_path)
        if not os.path.isfile(full_path):
            continue

        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                local_content = f.read()
        except Exception:
            continue

        local_hash = compute_hash(local_content)

        # 1. Check if identical to an existing remote file
        remote_content = get_remote_file_content(git_root, remote_ref, rel_path)

        if remote_content is not None:
            remote_hash = compute_hash(remote_content)
            if local_hash == remote_hash:
                results["identical_files_skipped"].append({
                    "path": rel_path,
                    "reason": "Exact byte-for-byte / normalized duplicate of remote file"
                })
                continue
            else:
                # File is modified. Let's inspect functions if it's Python
                if rel_path.endswith(".py"):
                    local_blocks = extract_python_blocks(local_content)
                    remote_blocks = extract_python_blocks(remote_content)

                    duplicate_functions = []
                    new_functions = []
                    modified_functions = []

                    for name, (b_hash, _) in local_blocks.items():
                        if name in remote_blocks:
                            if b_hash == remote_blocks[name][0]:
                                duplicate_functions.append(name)
                            else:
                                modified_functions.append(name)
                        else:
                            new_functions.append(name)

                    results["python_ast_analysis"][rel_path] = {
                        "duplicate_functions": duplicate_functions,
                        "new_functions": new_functions,
                        "modified_functions": modified_functions,
                    }

                results["genuine_modified_files"].append(rel_path)
        else:
            # File doesn't exist under this relative path on remote.
            # Check if it's a duplicate of a remote file located elsewhere (cross-file duplicate)
            if local_hash in remote_hashes:
                matched_remote = remote_hashes[local_hash]
                results["identical_files_skipped"].append({
                    "path": rel_path,
                    "reason": f"Content duplicate of existing remote file '{matched_remote}'"
                })
            else:
                results["brand_new_files"].append(rel_path)

    return results


def print_report(results: Dict):
    """Print an attractive summary report of the duplicate detection audit."""
    print("\n" + "=" * 70)
    print(f"{BOLD}{CYAN}🔍 PRE-PUSH INTELLIGENT DUPLICATE AUDIT REPORT{RESET}")
    print("=" * 70)

    # 1. Skipped Duplicate Files
    skipped = results["identical_files_skipped"]
    print(f"\n{BOLD}⏩ 1. DUPLICATE FILES SKIPPED ({len(skipped)} files identical to GitHub):{RESET}")
    if skipped:
        for item in skipped:
            print(f"  {DIM}• {item['path']} {RESET}{YELLOW}[SKIP - {item['reason']}]{RESET}")
    else:
        print(f"  {DIM}(None - no redundant identical files found){RESET}")

    # 2. Genuinely Modified Files
    modified = results["genuine_modified_files"]
    print(f"\n{BOLD}✏️  2. GENUINELY MODIFIED FILES TO PUSH ({len(modified)} files):{RESET}")
    if modified:
        for f in modified:
            print(f"  • {GREEN}{f}{RESET}")
            # If Python AST details exist
            if f in results["python_ast_analysis"]:
                ast_data = results["python_ast_analysis"][f]
                dup_fn = ast_data["duplicate_functions"]
                new_fn = ast_data["new_functions"]
                mod_fn = ast_data["modified_functions"]

                if dup_fn:
                    print(f"    {DIM}└─ Skipped Duplicate Functions ({len(dup_fn)}): {', '.join(dup_fn[:4])}{'...' if len(dup_fn) > 4 else ''}{RESET}")
                if new_fn:
                    print(f"    └─ {GREEN}★ Brand-New Functions ({len(new_fn)}): {', '.join(new_fn)}{RESET}")
                if mod_fn:
                    print(f"    └─ {CYAN}⚡ Modified Functions ({len(mod_fn)}): {', '.join(mod_fn)}{RESET}")
    else:
        print(f"  {DIM}(None){RESET}")

    # 3. Brand-New Files
    brand_new = results["brand_new_files"]
    print(f"\n{BOLD}🆕 3. BRAND-NEW FILES TO PUSH ({len(brand_new)} files):{RESET}")
    if brand_new:
        for f in brand_new:
            print(f"  • {GREEN}{f}{RESET} {GREEN}[NEW]{RESET}")
    else:
        print(f"  {DIM}(None){RESET}")

    print("\n" + "-" * 70)
    total_genuine = len(modified) + len(brand_new)
    print(f"{BOLD}SUMMARY: {len(skipped)} duplicates skipped | {total_genuine} genuine files ready to push.{RESET}")
    print("-" * 70 + "\n")


def stage_genuine_changes(git_root: str, results: Dict):
    """Stage only genuinely modified and brand-new files; unstage duplicates."""
    to_stage = results["genuine_modified_files"] + results["brand_new_files"]
    skipped = [item["path"] for item in results["identical_files_skipped"]]

    # Unstage skipped files if they were staged
    for path in skipped:
        run_git(["reset", "HEAD", path], cwd=git_root)

    # Stage genuine files
    if to_stage:
        print(f"{CYAN}Staging {len(to_stage)} genuine files...{RESET}")
        for path in to_stage:
            code, _, err = run_git(["add", path], cwd=git_root)
            if code == 0:
                print(f"  {GREEN}✔ Staged:{RESET} {path}")
            else:
                print(f"  {RED}✖ Failed to stage {path}: {err}{RESET}")


def install_git_hook(git_root: str):
    """Installs this script as a Git pre-push hook."""
    hooks_dir = os.path.join(git_root, ".git", "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    hook_path = os.path.join(hooks_dir, "pre-push")

    script_path = os.path.abspath(__file__)
    hook_script = f"""#!/bin/sh
# Matrubhasa AI Pre-Push Duplicate Guard Hook
python3 "{script_path}" --dry-run
if [ $? -ne 0 ]; then
    echo "Pre-push check failed. Push aborted."
    exit 1
fi
"""
    with open(hook_path, "w", encoding="utf-8") as f:
        f.write(hook_script)

    # Make executable on Unix/Git Bash
    try:
        os.chmod(hook_path, 0o755)
    except Exception:
        pass

    print(f"{GREEN}✔ Successfully installed pre-push hook at: {hook_path}{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Smart Git & Python Pre-Push Duplicate Checker for Matrusetu"
    )
    parser.add_argument("--remote", default=DEFAULT_REMOTE_NAME, help="Target remote name (default: upstream)")
    parser.add_argument("--remote-url", default=TARGET_REPO_URL, help=f"Remote URL (default: {TARGET_REPO_URL})")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="Target remote branch (default: main)")
    parser.add_argument("--stage", action="store_true", help="Stage only genuine changes (excluding duplicates)")
    parser.add_argument("--commit", type=str, help="Commit message to commit staged genuine changes")
    parser.add_argument("--push", action="store_true", help="Push genuine changes to target remote")
    parser.add_argument("--install-hook", action="store_true", help="Install this script as Git pre-push hook")
    parser.add_argument("--dry-run", action="store_true", help="Run audit only without modifying git index")

    args = parser.parse_args()

    git_root = get_git_root()

    if args.install_hook:
        install_git_hook(git_root)
        return

    # Ensure remote exists
    ensure_remote(git_root, args.remote, args.remote_url)

    # Fetch remote ref
    remote_sha = fetch_remote(git_root, args.remote, args.branch)

    # Analyze duplicates vs genuine changes
    print(f"{CYAN}🔬 Analyzing local codebase against remote {args.remote}/{args.branch} ({remote_sha[:7]})...{RESET}")
    results = analyze_diff(git_root, f"{args.remote}/{args.branch}")

    # Print Visual Report
    print_report(results)

    total_genuine = len(results["genuine_modified_files"]) + len(results["brand_new_files"])

    if total_genuine == 0:
        print(f"{GREEN}All files/blocks are identical to GitHub or no new changes detected. Nothing to push!{RESET}")
        return

    if args.stage or args.commit or args.push:
        stage_genuine_changes(git_root, results)

    if args.commit:
        print(f"\n{CYAN}Creating commit with message: '{args.commit}'...{RESET}")
        code, out, err = run_git(["commit", "-m", args.commit], cwd=git_root)
        if code == 0:
            print(f"{GREEN}✔ Committed successfully: {out.splitlines()[0]}{RESET}")
        else:
            print(f"{RED}Commit error: {err}{RESET}")

    if args.push:
        current_branch_code, current_branch, _ = run_git(["branch", "--show-current"], cwd=git_root)
        src_branch = current_branch if current_branch_code == 0 and current_branch else "HEAD"
        print(f"\n{CYAN}🚀 Pushing genuine code to {args.remote} {args.branch}...{RESET}")
        code, out, err = run_git(["push", args.remote, f"{src_branch}:{args.branch}"], cwd=git_root)
        if code == 0:
            print(f"{GREEN}✔ Push successful! Codebase synchronized.{RESET}")
        else:
            print(f"{YELLOW}Note during push:{RESET}\n{err or out}")


if __name__ == "__main__":
    main()
