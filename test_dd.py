import time
from contextlib import contextmanager

import ddtrace


class DatadogSpan:
    """Offers a facility to get and create custom trace/span."""

    def __init__(
        self,
        name: str = "logalot.custom_trace",
        resource: str = "logalot",
    ):
        self.name = name
        self.resource = resource
        self.current_span = ddtrace.tracer.current_span()

    @contextmanager
    def span(self):
        """Yield the current span, or return a new custom span."""
        if self.current_span:
            yield self.current_span
        else:
            with ddtrace.tracer.trace(name=self.name, resource=self.resource) as span:
                yield span



def test_crash():
    """Test that causes ConnectionRefusedError and tenacity.RetryError."""
    with DatadogSpan().span() as span:
        time.sleep(5)
        pass
