#!/usr/bin/env python3
"""
CI/CD Test Runner — watchdog + threading.Timer debounce.
Standalone script, test-harness projesinden bağımsız çalışır.
"""

import argparse, os, subprocess, sys, time
from threading import Timer, Lock

def run_tests(tests_dir: str, workdir: str) -> bool:
    """pytest calistir, basariliysa True don."""
    print(f"\n{'='*50}\n  TEST: {time.strftime('%H:%M:%S')}\n{'='*50}")
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--tb=short", tests_dir],
        capture_output=True, text=True, cwd=workdir,
    )
    print(r.stdout)
    if r.stderr: print("[STDERR]", r.stderr)
    ok = r.returncode == 0
    print(f"{'='*50}\n  {'OK' if ok else 'HATA'} (exit: {r.returncode})\n{'='*50}")
    return ok

class DebouncedWatcher:
    def __init__(self, watch_dir: str, tests_dir: str, workdir: str, delay: float = 1.5):
        self.watch_dir, self.tests_dir, self.workdir = watch_dir, tests_dir, workdir
        self.delay, self._timer, self._lock, self._count = delay, None, Lock(), 0

    def _on_change(self, path: str):
        if not path.endswith(".py"): return
        with self._lock:
            self._count += 1
            if self._timer: self._timer.cancel()
            self._timer = Timer(self.delay, lambda: [
                print(f"\n  [{self._count} degisiklik]"), setattr(self, '_count', 0),
                run_tests(self.tests_dir, self.workdir)
            ][0])
            self._timer.daemon = True
            self._timer.start()

    def run(self):
        import watchdog.observers, watchdog.events
        h = type("H", (watchdog.events.FileSystemEventHandler,), {
            "on_modified": lambda s, e: not e.is_directory and self._on_change(e.src_path),
            "on_created": lambda s, e: not e.is_directory and self._on_change(e.src_path),
        })()
        o = watchdog.observers.Observer()
        o.schedule(h, self.watch_dir, recursive=True)
        o.start()
        print(f"  Izleniyor: {self.watch_dir}\n  Debounce: {self.delay}s\n  Ctrl+C cikis")
        try:
            while True: time.sleep(0.1)
        except KeyboardInterrupt:
            with self._lock:
                if self._timer: self._timer.cancel()
            o.stop()
        o.join()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--delay", type=float, default=1.5)
    ap.add_argument("--tests-dir", default="tests")
    ap.add_argument("--workdir", default=os.getcwd())
    args = ap.parse_args()
    if args.watch:
        DebouncedWatcher(args.tests_dir, args.tests_dir, args.workdir, args.delay).run()
    else:
        sys.exit(0 if run_tests(args.tests_dir, args.workdir) else 1)
