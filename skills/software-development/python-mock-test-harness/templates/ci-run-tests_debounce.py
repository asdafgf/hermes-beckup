#!/usr/bin/env python3
"""
CI/CD Test Koşucusu — Watchdog + debounce şablonu
Bu dosyayı projenizin ci/run_tests.py olarak kullanın.

Özellikler:
  - --watch: tests/ dizinini izler, .py değişikliklerinde otomatik test
  - --no-watch: tek seferlik koş (varsayılan)
  - 1.5s debounce: threading.Timer + Lock, time.sleep() YOK
  - thread-safe: Lock ile çoklu olay güvenliği
"""

import argparse
import os
import subprocess
import sys
import time
from threading import Timer, Lock

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(PROJECT_DIR, "tests")
PYTEST_ARGS = ["-v", "--tb=short"]


def run_tests() -> bool:
    """pytest'i koşar, başarılıysa True döner."""
    print("\n" + "=" * 55)
    print(f"  TEST CALISIYOR: {time.strftime('%H:%M:%S')}")
    print("=" * 55)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", *PYTEST_ARGS, TESTS_DIR],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
    )
    print(result.stdout)
    if result.stderr:
        print("[STDERR]", result.stderr)

    ok = result.returncode == 0
    status = "✓ BASARILI" if ok else "✗ BASARISIZ"
    print(f"{'=' * 55}\n  {status} (cikis: {result.returncode})\n{'=' * 55}\n")
    return ok


class DebouncedWatcher:
    """Watchdog + threading.Timer ile debounce'lu dosya izleyici."""

    def __init__(self, watch_dir: str, debounce_seconds: float = 1.5):
        self.watch_dir = watch_dir
        self.debounce_seconds = debounce_seconds
        self._timer: Timer | None = None
        self._lock = Lock()

    def _debounce_elapsed(self):
        """Debounce süresi doldu — testi koş."""
        with self._lock:
            self._timer = None
        run_tests()

    def on_modified(self, event_path: str):
        """Dosya değişikliği olayını işle — sadece .py dosyaları."""
        if not event_path.endswith(".py"):
            return
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = Timer(self.debounce_seconds, self._debounce_elapsed)
            self._timer.daemon = True
            self._timer.start()

    def run(self):
        """İzleme döngüsünü başlat (Ctrl+C ile durdurulur)."""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class Handler(FileSystemEventHandler):
            def __init__(self, watcher):
                self.watcher = watcher

            def on_modified(self, event):
                if not event.is_directory:
                    self.watcher.on_modified(event.src_path)

            def on_created(self, event):
                if not event.is_directory:
                    self.watcher.on_modified(event.src_path)

        handler = Handler(self)
        observer = Observer()
        observer.schedule(handler, self.watch_dir, recursive=True)

        print(f"\n  [*] Izleniyor: {self.watch_dir}")
        print(f"  [*] Debounce: {self.debounce_seconds}s")
        print(f"  [*] Cikis: Ctrl+C\n")
        observer.start()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n  [i] Durduruluyor...")
            with self._lock:
                if self._timer is not None:
                    self._timer.cancel()
            observer.stop()
        observer.join()
        print("  [OK] Durdu.")


def main():
    parser = argparse.ArgumentParser(description="Test Harness CI/CD")
    parser.add_argument("--watch", action="store_true", help="Dosya değişikliklerini izle")
    parser.add_argument("--debounce", type=float, default=1.5, help="Debounce süresi (saniye)")
    args = parser.parse_args()

    if args.watch:
        DebouncedWatcher(TESTS_DIR, args.debounce).run()
    else:
        sys.exit(0 if run_tests() else 1)


if __name__ == "__main__":
    main()
