import threading
from typing import Final

from app.services import pipelines


DEFAULT_INTERVAL_SECONDS: Final = 30

_thread: threading.Thread | None = None
_stop_event = threading.Event()


def start_scheduler(interval_seconds: int = DEFAULT_INTERVAL_SECONDS) -> None:
    global _thread
    pipelines.process_due_schedules()
    if _thread and _thread.is_alive():
        return
    _stop_event.clear()
    _thread = threading.Thread(
        target=_scheduler_loop,
        args=(interval_seconds,),
        name="kriyax-pipeline-scheduler",
        daemon=True,
    )
    _thread.start()


def stop_scheduler() -> None:
    _stop_event.set()
    if _thread and _thread.is_alive():
        _thread.join(timeout=1)


def _scheduler_loop(interval_seconds: int) -> None:
    while not _stop_event.wait(interval_seconds):
        pipelines.process_due_schedules()
