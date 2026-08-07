import xml.etree.ElementTree as ET

from app.services.audio import _xml_escape, build_segment_ssml, build_ssml
from app.services.clean_text import Text


def make_text():
    return Text()


def test_inline_inciso_single_reference():
    text = make_text()
    result = text.expand_legal_terms("nos termos do inciso IV do art. 5º")
    assert result == "nos termos do inciso quarto do artigo quinto"


def test_inline_inciso_comma_and_list():
    text = make_text()
    assert text.expand_legal_terms("incisos I, II e III") == "incisos primeiro, segundo e terceiro"


def test_inline_inciso_range():
    text = make_text()
    assert text.expand_legal_terms("conforme incisos II a V") == "conforme incisos segundo a quinto"


def test_inciso_line_start_with_period_delimiter():
    text = make_text()
    assert text.expand_legal_terms("IV. a liberdade") == "quarto. a liberdade"


def test_inciso_line_start_with_dash_delimiter_still_works():
    text = make_text()
    assert text.expand_legal_terms("I - a vida") == "primeiro - a vida"


def test_leading_markdown_dash_bullet_no_longer_blocks_conversion():
    text = make_text()
    assert text.clean("- I - a vida;") == "primeiro - a vida;"


def test_leading_markdown_asterisk_bullet_still_works_no_regression():
    text = make_text()
    assert text.clean("* I - a vida;") == "primeiro - a vida;"


def test_ordinal_hundreds():
    text = make_text()
    assert text.expand_legal_terms("C - centésimo item") == "centésimo - centésimo item"
    assert text._int_to_ordinal_pt(100) == "centésimo"
    assert text._int_to_ordinal_pt(101) == "centésimo primeiro"
    assert text._int_to_ordinal_pt(321) == "trecentésimo vigésimo primeiro"


def test_markdown_headers_are_stripped_not_leaked_into_speech():
    text = make_text()
    assert text.clean("## CAPÍTULO I\n\nConteúdo") == "CAPÍTULO I\n\nConteúdo"


def test_split_by_chapters_preserves_duplicate_chapter_numbers():
    text = make_text()
    doc = "Preamble.\n\nCAPÍTULO I\nContent A\n\nCAPÍTULO II\nContent B\n\nCAPÍTULO I\nContent C"
    chapters = text.split_text_by_chapters(doc)
    titles = [title for title, _ in chapters]
    assert titles.count("CAPÍTULO I") == 2
    contents = [content for _, content in chapters]
    assert "Content A" in contents
    assert "Content C" in contents


def test_split_by_chapters_is_case_insensitive():
    text = make_text()
    doc = "Capítulo IV\nConteúdo do capítulo"
    chapters = text.split_text_by_chapters(doc)
    assert len(chapters) == 1
    assert chapters[0][0] == "CAPÍTULO IV"


def test_split_by_chapters_preserves_preamble():
    text = make_text()
    doc = "Texto de preâmbulo.\n\nCAPÍTULO I\nConteúdo"
    chapters = text.split_text_by_chapters(doc)
    assert chapters[0] == (None, "Texto de preâmbulo.")
    assert chapters[1][0] == "CAPÍTULO I"


def test_split_by_chapters_captures_amendment_suffix():
    text = make_text()
    doc = "CAPÍTULO II-A\nConteúdo emendado"
    chapters = text.split_text_by_chapters(doc)
    assert chapters[0][0] == "CAPÍTULO II-A"
    assert chapters[0][1] == "Conteúdo emendado"


def test_expand_chapter_headings_for_speech_converts_capitulo():
    text = make_text()
    result = text.expand_chapter_headings_for_speech("CAPÍTULO IV\nConteúdo")
    assert result == "CAPÍTULO quarto\nConteúdo"


def test_expand_legal_terms_still_excludes_capitulo_by_default():
    text = make_text()
    # expand_legal_terms (used inside clean(), which feeds split_text_by_chapters)
    # must NOT touch CAPÍTULO, or chapter splitting would break.
    result = text.expand_legal_terms("CAPÍTULO IV")
    assert result == "CAPÍTULO IV"


class _FakeVoiceOnlyText(Text):
    """Minimal subclass exposing just insert_speech_breaks for isolated SSML tests."""


def test_ssml_envelope_is_well_formed_xml():
    ssml = build_segment_ssml("Art. 1º § 1º Isto & aquilo <teste> \"citação\"", cleaner=make_text())
    # Must not raise — a malformed document (bad escaping/tag order) would.
    root = ET.fromstring(ssml)
    assert root.tag.endswith("speak")
    voices = [child for child in root if child.tag.endswith("voice")]
    assert len(voices) == 1


def test_xml_escape_and_break_insertion_order():
    escaped = _xml_escape("Empresas & Cia <teste>")
    assert "&amp;" in escaped and "<" not in escaped
    tagged = make_text().insert_speech_breaks("§ 1º Texto")
    assert tagged.startswith("<break")
    # the break tag itself must not have been escaped
    assert "&lt;break" not in tagged


def test_build_ssml_contains_single_speak_and_voice():
    ssml = build_ssml("texto de teste", voice="pt-BR-ThalitaMultilingualNeural", rate="-8%")
    assert ssml.count("<speak") == 1
    assert ssml.count("<voice") == 1
    assert "<prosody rate='-8%'>" in ssml
