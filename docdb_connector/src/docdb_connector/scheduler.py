import logging
import threading
import time

import schedule

log = logging.getLogger(__name__)


def run_threaded(job_func):
    """Runs a given job in a thread."""
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


#  See: https://schedule.readthedocs.io/en/stable/ for documentation on job syntax
class Scheduler(object):
    """Simple scheduler class that holds all scheduled functions."""

    registered_tasks = []

    def add(self, job, *args, **kwargs):
        """Adds a task to the scheduler."""

        def decorator(func):
            if not kwargs.get("name"):
                name = func.__name__
            else:
                name = kwargs.pop("name")

            self.registered_tasks.append(
                {"name": name, "func": func, "job": job.do(run_threaded, func)}
            )

        return decorator

    def remove(self, task):
        """Removes a task from the scheduler."""
        schedule.cancel_job(task["job"])

    def start(self):
        """Runs all scheduled tasks."""
        while True:
            schedule.run_pending()
            time.sleep(1)


scheduler = Scheduler()
