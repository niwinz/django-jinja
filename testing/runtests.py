#!/usr/bin/env python
import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    args = sys.argv
    args.insert(1, "test")

    if len(args) == 2:
        args.insert(2, "testapp")

    execute_from_command_line(args)
