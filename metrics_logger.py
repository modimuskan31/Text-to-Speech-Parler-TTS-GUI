import logging
import time
import psutil
import tracemalloc

class PerformanceTracker:
    def __init__(self, label="Default Task"):
        self.label = label
        self.process = psutil.Process()
        self.start_time = None
        self.end_time = None
        self.cpu_start = None
        self.cpu_end = None
        self.memory_usage = None

    def start(self):
        self.start_time = time.time()
        self.cpu_start = self.process.cpu_times()
        tracemalloc.start()

    def stop(self):
        self.end_time = time.time()
        self.cpu_end = self.process.cpu_times()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed = self.end_time - self.start_time
        cpu_percent = self._calculate_cpu_percent()

        self.memory_usage = peak / (1024 * 1024)  # Convert to MB

        return {
            "label": self.label,
            "duration": elapsed,
            "cpu": cpu_percent,
            "memory": self.memory_usage
        }

    def _calculate_cpu_percent(self):
        # Calculate CPU usage over the time duration
        user_diff = self.cpu_end.user - self.cpu_start.user
        system_diff = self.cpu_end.system - self.cpu_start.system
        total_time = user_diff + system_diff
        elapsed = self.end_time - self.start_time
        if elapsed == 0:
            return 0.0
        return (total_time / elapsed) * 100

    def log_metrics(self):
        metrics = self.stop()
        logging.info(f"[{metrics['label']}] Time: {metrics['duration']:.2f}s | "
                     f"CPU: {metrics['cpu']:.2f}% | Peak Mem: {metrics['memory']:.2f} MB")
