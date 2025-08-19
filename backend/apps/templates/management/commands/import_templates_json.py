from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.templates.models import GutierrezTemplate, RossiTemplate


class Command(BaseCommand):
    help = "Import text templates from JSON dump. Supports Rossi and Gutierrez separation."

    def add_arguments(self, parser):
        parser.add_argument("json_path", type=str, help="Path to JSON file exported from old DB")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and show counts without writing to the database",
        )

    def handle(self, *args, **options):
        json_path = Path(options["json_path"]).expanduser()
        if not json_path.exists():
            raise CommandError(f"File not found: {json_path}")

        with json_path.open("r", encoding="utf-8") as f:
            try:
                payload = json.load(f)
            except json.JSONDecodeError as e:
                raise CommandError(f"Invalid JSON: {e}")

        # Accept either array or object with key 'blog_texttemplate'
        if isinstance(payload, dict) and "blog_texttemplate" in payload:
            rows: Iterable[Dict[str, Any]] = payload["blog_texttemplate"]
        elif isinstance(payload, list):
            rows = payload
        else:
            raise CommandError("Unsupported JSON format. Expected array or object with 'blog_texttemplate'.")

        rossi_count = 0
        gut_count = 0

        if options["dry_run"]:
            for row in rows:
                ttype = str(row.get("template_type") or "gutierrez").lower()
                if ttype == "rossi":
                    rossi_count += 1
                else:
                    gut_count += 1
            self.stdout.write(self.style.SUCCESS(f"Would import: Rossi={rossi_count}, Gutierrez={gut_count}"))
            return

        with transaction.atomic():
            for row in rows:
                title = (row.get("title") or "").strip()
                category = (row.get("category") or "Без категории").strip()
                content = row.get("content") or ""
                created_by_id = row.get("created_by_id")
                template_type = str(row.get("template_type") or "gutierrez").lower()

                if template_type == "rossi":
                    RossiTemplate.objects.update_or_create(
                        title=title,
                        category=category,
                        defaults={"content": content},
                    )
                    rossi_count += 1
                else:
                    GutierrezTemplate.objects.update_or_create(
                        title=title,
                        category=category,
                        defaults={"content": content, "created_by_id": created_by_id},
                    )
                    gut_count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported: Rossi={rossi_count}, Gutierrez={gut_count}"))


