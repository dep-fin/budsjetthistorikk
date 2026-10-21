"""Reviewbart Windows Task Scheduler XML. Denne modulen registrerer ingen oppgave."""

import subprocess
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

TASK_NS = "http://schemas.microsoft.com/windows/2004/02/mit/task"


def task_xml(
    config_path: Path, python_path: Path, working_directory: Path, account: str, start_date: date
) -> str:
    if not account.strip() or any(c in account for c in "\r\n"):
        raise ValueError("Eksisterende Windows-driftskonto må oppgis uttrykkelig")
    if not all(p.is_absolute() for p in (config_path, python_path, working_directory)):
        raise ValueError("Windows-oppgaven krever absolutte baner")
    ET.register_namespace("", TASK_NS)
    root = ET.Element("Task", {"xmlns": TASK_NS, "version": "1.4"})

    def node(
        parent: ET.Element, name: str, value: str | None = None, **attributes: str
    ) -> ET.Element:
        result = ET.SubElement(parent, name, attributes)
        result.text = value
        return result

    triggers = node(root, "Triggers")
    trigger = node(triggers, "CalendarTrigger")
    node(trigger, "StartBoundary", f"{start_date.isoformat()}T06:00:00")
    node(trigger, "Enabled", "true")
    node(node(trigger, "ScheduleByDay"), "DaysInterval", "1")
    principals = node(root, "Principals")
    principal = node(principals, "Principal", id="Author")
    node(principal, "UserId", account)
    node(principal, "LogonType", "Password")
    node(principal, "RunLevel", "LeastPrivilege")
    settings = node(root, "Settings")
    for key, value in {
        "MultipleInstancesPolicy": "IgnoreNew",
        "DisallowStartIfOnBatteries": "false",
        "StopIfGoingOnBatteries": "false",
        "StartWhenAvailable": "true",
        "RunOnlyIfNetworkAvailable": "false",
        "Enabled": "true",
        "WakeToRun": "true",
        "ExecutionTimeLimit": "PT0S",
    }.items():
        node(settings, key, value)
    restart = node(settings, "RestartOnFailure")
    node(restart, "Interval", "PT15M")
    node(restart, "Count", "3")
    action = node(node(root, "Actions", Context="Author"), "Exec")
    node(action, "Command", str(python_path))
    node(
        action, "Arguments", subprocess.list2cmdline(["-m", "drift", "--config", str(config_path)])
    )
    node(action, "WorkingDirectory", str(working_directory))
    return ET.tostring(root, encoding="unicode", xml_declaration=True)
