from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Callable

from app.models import DocumentResult, SegmentResult
from app.services.audio import build_segment_ssml, generate_tts
from app.services.clean_text import Text
from app.services.file_converter import FileConverter


class DocumentProcessingPipeline:
    def __init__(self, output_dir: str = "storage/jobs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.converter = FileConverter()
        self.cleaner = Text()

    def _slugify(self, value: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
        return slug or "segment"

    def _build_segments(self, cleaned_text: str) -> list[tuple[str | None, str]]:
        chapters = self.cleaner.split_text_by_chapters(cleaned_text)
        if chapters:
            return chapters
        speakable_text = self.cleaner.expand_chapter_headings_for_speech(cleaned_text)
        return [(None, chunk) for chunk in self.cleaner.chunk_text(speakable_text)]

    def process(
        self,
        job_id: str,
        pdf_path: str,
        file_name: str,
        on_text_ready: Callable[[str, str, int], None] | None = None,
        on_segment_ready: Callable[[SegmentResult], None] | None = None,
    ) -> DocumentResult:
        markdown = self.converter.pdf_to_markdown(pdf_path)
        cleaned_text = self.cleaner.clean(markdown)
        segments = self._build_segments(cleaned_text)

        if on_text_ready:
            on_text_ready(markdown, cleaned_text, len(segments))

        job_dir = self.output_dir / job_id
        audio_dir = job_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)

        use_ssml = os.getenv("AZURE_SPEECH_USE_SSML", "false").lower() == "true"

        results: list[SegmentResult] = []
        for index, (title, segment_text) in enumerate(segments, start=1):
            label = self._slugify(title or f"segment-{index}")
            audio_file = audio_dir / f"{index:02d}-{label}.mp3"
            if use_ssml:
                ssml_doc = build_segment_ssml(segment_text, cleaner=self.cleaner)
                generate_tts(ssml_doc, output_path=str(audio_file), use_ssml=True)
            else:
                generate_tts(segment_text, output_path=str(audio_file), use_ssml=False)
            segment = SegmentResult(
                title=title,
                text=segment_text,
                audio_file=audio_file.name,
                download_url=f"/api/jobs/{job_id}/audio/{audio_file.name}",
            )
            results.append(segment)
            if on_segment_ready:
                on_segment_ready(segment)

        return DocumentResult(markdown=markdown, cleaned_text=cleaned_text, segments=results)
