import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


DEFAULT_SOURCE = "git+https://github.com/wang930813-blip/wx-rpa.git#subdirectory=src"


def log(message):
    print(message, flush=True)


def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise RuntimeError(
            "command failed: {}\nstdout:\n{}\nstderr:\n{}".format(
                " ".join(map(str, cmd)), result.stdout, result.stderr
            )
        )
    return result


def venv_python(workspace):
    if os.name == "nt":
        return workspace / ".venv" / "Scripts" / "python.exe"
    return workspace / ".venv" / "bin" / "python"


def package_available():
    return importlib.util.find_spec("pyweixin") is not None or importlib.util.find_spec("pywechat") is not None


def ensure_bootstrap(args):
    workspace = Path(args.workspace or os.getcwd()).resolve()
    python_path = venv_python(workspace)

    if not python_path.exists():
        uv = shutil.which("uv")
        if not uv:
            raise RuntimeError("uv is required to create the local Python environment.")
        log("Creating virtual environment: {}".format(workspace / ".venv"))
        run([uv, "venv", "--python", args.python, str(workspace / ".venv")], cwd=workspace)

    current = Path(sys.executable).resolve()
    target = python_path.resolve()
    if current != target:
        cmd = [str(target), str(Path(__file__).resolve())] + sys.argv[1:] + ["--bootstrapped"]
        os.execv(str(target), cmd)

    if args.force_install or not package_available():
        uv = shutil.which("uv")
        if not uv:
            raise RuntimeError("uv is required to install pywechat127 dependencies.")
        log("Installing pywechat127 from {}".format(args.source))
        run([uv, "pip", "install", args.source], cwd=workspace)


def get_wechat_processes():
    import psutil

    processes = []
    for proc in psutil.process_iter(["name", "exe"]):
        try:
            name = proc.info.get("name") or ""
            exe = proc.info.get("exe") or ""
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        if name.lower() in {"weixin.exe", "wechat.exe"}:
            processes.append({"name": name, "exe": exe})
    return processes


def file_version(path):
    if not path or os.name != "nt":
        return ""
    ps = (
        "(Get-Item -LiteralPath '{}').VersionInfo.ProductVersion".format(
            str(path).replace("'", "''")
        )
    )
    result = run(["powershell", "-NoProfile", "-Command", ps], check=False)
    return (result.stdout or "").strip()


def choose_backend():
    processes = get_wechat_processes()
    if not processes:
        raise RuntimeError("No running WeChat/Weixin process found. Open and log in to PC WeChat first.")

    preferred = None
    for proc in processes:
        if proc["name"].lower() == "weixin.exe":
            preferred = proc
            break
    if preferred is None:
        preferred = processes[0]

    version = file_version(preferred.get("exe", ""))
    major = None
    if version:
        try:
            major = int(version.split(".")[0])
        except ValueError:
            major = None

    if preferred["name"].lower() == "weixin.exe" or (major is not None and major >= 4):
        return "pyweixin", preferred, version
    return "pywechat", preferred, version


def send_message(backend, recipient, messages):
    if backend == "pyweixin":
        from pyweixin import Messages
    else:
        from pywechat import Messages

    Messages.send_messages_to_friend(
        friend=recipient,
        messages=messages,
        close_weixin=False,
    )


def visible_wechat_text():
    from pywinauto import Desktop

    desktop = Desktop(backend="uia")
    windows = [w for w in desktop.windows(class_name="mmui::MainWindow") if w.window_text() == "微信"]
    if not windows:
        windows = desktop.windows(title_re=".*微信.*")
    if not windows:
        return ""
    main = windows[0]
    return "\n".join(d.window_text() for d in main.descendants() if d.window_text())


def verify_visible_text(recipient, messages, timeout):
    deadline = time.time() + timeout
    last_text = ""
    while time.time() < deadline:
        last_text = visible_wechat_text()
        if recipient in last_text and all(message in last_text for message in messages):
            return True, last_text
        time.sleep(0.5)
    return False, last_text


def parse_args():
    parser = argparse.ArgumentParser(description="Send and verify Windows PC WeChat messages.")
    parser.add_argument("--to", dest="recipient", help="WeChat contact, group, or 文件传输助手 name.")
    parser.add_argument("--message", action="append", dest="messages", help="Message text. Repeat to send multiple messages.")
    parser.add_argument("--workspace", default=os.getcwd(), help="Workspace where .venv should be created or reused.")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="pip install source for pywechat127.")
    parser.add_argument("--python", default="3.12", help="Python version for uv venv.")
    parser.add_argument("--force-install", action="store_true", help="Reinstall pywechat127 from --source.")
    parser.add_argument("--skip-verify", action="store_true", help="Skip visible WeChat UI text verification.")
    parser.add_argument("--ensure-only", action="store_true", help="Only ensure environment and report selected backend.")
    parser.add_argument("--verify-timeout", type=float, default=8.0, help="Seconds to wait for UI verification.")
    parser.add_argument("--bootstrapped", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args()


def main():
    args = parse_args()
    ensure_bootstrap(args)

    backend, process, version = choose_backend()
    summary = {
        "backend": backend,
        "process": process,
        "version": version,
        "source": args.source,
    }

    if args.ensure_only:
        print(json.dumps({"ok": True, **summary}, ensure_ascii=False))
        return 0

    if not args.recipient or not args.messages:
        raise SystemExit("--to and at least one --message are required unless --ensure-only is used.")

    send_message(backend, args.recipient, args.messages)

    verified = None
    if not args.skip_verify:
        verified, _ = verify_visible_text(args.recipient, args.messages, args.verify_timeout)
        if not verified:
            print(json.dumps({"ok": False, "verified": False, **summary}, ensure_ascii=False))
            return 2

    print(json.dumps({"ok": True, "verified": verified, "to": args.recipient, "messages": args.messages, **summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
