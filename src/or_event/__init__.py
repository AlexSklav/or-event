'''
Wait on multiple :class:`threading.Event` instances.

Based on code from: https://stackoverflow.com/questions/12317940/python-threading-can-i-sleep-on-two-threading-events-simultaneously/12320352#12320352
'''
import threading
from typing import List

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


__all__ = ['OrEvent']


def or_set(event: threading.Event) -> None:
    event._set()
    event.changed()


def or_clear(event: threading.Event) -> None:
    event._clear()
    event.changed()


def orify(event: threading.Event, changed_callback: callable) -> None:
    """
    Override `set` and `clear` methods on event to call specified callback
    function after performing default behavior.

    Parameters
    ----------
    event : threading.Event
        The event to override methods for.
    changed_callback : callable
        The callback function to call after performing default behavior.
    """
    event.changed = changed_callback
    if not hasattr(event, '_set'):
        # `set`/`clear` methods have not been overridden on the event yet.
        # Override methods to call `changed_callback` after performing default
        # action.
        event._set = event.set
        event._clear = event.clear
        event.set = lambda: or_set(event)
        event.clear = lambda: or_clear(event)


def OrEvent(*events: List[threading.Event]) -> threading.Event:
    """
    Create an event that is set when **at least one** of the specified events
    is set.

    Parameters
    ----------
    *events : List[threading.Event]
        Variable-length argument list of events.

    Returns
    -------
    threading.Event
        Event that is set when **at least one** of the events in `events` is set.
    """
    or_event = threading.Event()

    def changed() -> None:
        """
        Set `or_event` if any of the specified events have been set.
        """
        bools = [event_i.is_set() for event_i in events]
        if any(bools):
            or_event.set()
        else:
            or_event.clear()

    for event_i in events:
        # Override `set` and `clear` methods on event to update the state of
        # `or_event` after performing default behavior.
        orify(event_i, changed)

    # Set the initial state of `or_event`.
    changed()
    return or_event
