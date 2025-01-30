# app/services/monitoring.py

from typing import Dict, Any, List
import psutil
import time
from datetime import datetime
import json
import os
from dataclasses import dataclass
from collections import deque

@dataclass
class MetricPoint:
    timestamp: str
    value: float
    metric_type: str
    context: Dict[str, Any]

class MonitoringService:
    def __init__(self):
        self.metrics_path = "logs/metrics"
        os.makedirs(self.metrics_path, exist_ok=True)

        # Keep recent metrics in memory
        self.recent_metrics = deque(maxlen=1000)

        # Performance thresholds
        self.thresholds = {
            'cpu_usage': 80.0,  # percentage
            'memory_usage': 85.0,  # percentage
            'process_time': 300,  # seconds
            'error_rate': 0.1  # 10% threshold
        }

    def start_monitoring(self, context: Dict[str, Any]):
        """
        Start monitoring a process
        """
        start_time = time.time()
        process = psutil.Process()

        return {
            'start_time': start_time,
            'process': process,
            'context': context
        }

    def record_metric(
        self,
        metric_type: str,
        value: float,
        context: Dict[str, Any]
    ):
        """
        Record a single metric
        """
        metric = MetricPoint(
            timestamp=datetime.now().isoformat(),
            value=value,
            metric_type=metric_type,
            context=context
        )

        self.recent_metrics.append(metric)
        self._save_metric(metric)

        # Check thresholds
        self._check_thresholds(metric)

    def end_monitoring(self, monitoring_data: Dict[str, Any]):
        """
        End monitoring and generate summary
        """
        end_time = time.time()
        duration = end_time - monitoring_data['start_time']

        summary = {
            'duration': duration,
            'cpu_usage': monitoring_data['process'].cpu_percent(),
            'memory_usage': monitoring_data['process'].memory_percent(),
            'context': monitoring_data['context']
        }

        self._save_summary(summary)
        return summary

    def _check_thresholds(self, metric: MetricPoint):
        """
        Check if metric exceeds thresholds
        """
        threshold = self.thresholds.get(metric.metric_type)
        if threshold and metric.value > threshold:
            self._handle_threshold_exceeded(metric)

    def _handle_threshold_exceeded(self, metric: MetricPoint):
        """
        Handle cases where metrics exceed thresholds
        """
        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'metric_type': metric.metric_type,
            'value': metric.value,
            'threshold': self.thresholds[metric.metric_type],
            'context': metric.context
        }

        # Save alert
        self._save_alert(alert_data)

    def _save_metric(self, metric: MetricPoint):
        """
        Save metric to file
        """
        filename = f"metrics_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(self.metrics_path, filename)

        with open(filepath, 'a') as f:
            f.write(json.dumps(vars(metric)) + '\n')

    def _save_summary(self, summary: Dict[str, Any]):
        """
        Save monitoring summary
        """
        filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.metrics_path, filename)

        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=4)

    def _save_alert(self, alert_data: Dict[str, Any]):
        """
        Save alert data
        """
        filename = f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.metrics_path, 'alerts', filename)
        os.makedirs(os.path.join(self.metrics_path, 'alerts'), exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(alert_data, f, indent=4)

# Created/Modified files:
# - logs/metrics/metrics_{date}.json
# - logs/metrics/summary_{timestamp}.json
# - logs/metrics/alerts/alert_{timestamp}.json