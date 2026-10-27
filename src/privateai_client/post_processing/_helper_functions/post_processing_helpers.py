import json

from requests import Response

from privateai_client.components import TextResponse


def _strip_marker_brackets(text: str) -> str:
    """
    Match the DEID convention of storing marker text without its enclosing brackets.

    Args:
        text: DEID redaction markers.

    Return:
        Markers with brackets removed.
    """
    if len(text) >= 2 and text.startswith("[") and text.endswith("]"):
        return text[1:-1]
    return text


def _populate_entity_locations(
    processed_text: str, entities: list[dict], clear_existing: bool = True
) -> None:
    """
    Add back OCR text location markers to PDF file entities.

    Args:
        processed_text: The redacte text processed in a given text block.
        entities: The entity list returned by the TextResponse with redacted text info.
        clear_existing: delete the existing location information before inserting new location info.
    """
    located_entities = []
    search_from = 0

    for entity in entities:
        placeholder = entity.get("processed_text")
        original_text = entity.get("text")
        if not isinstance(placeholder, str) or not isinstance(original_text, str):
            raise ValueError(
                "Each entity must have string 'processed_text' and 'text' values"
            )

        marker = f"[{placeholder.strip('[]')}]"
        processed_start = processed_text.find(marker, search_from)
        if processed_start == -1:
            raise ValueError(f"Redaction marker {marker!r} was not found")

        processed_end = processed_start + len(marker)
        located_entities.append(
            (processed_start, processed_end, marker, original_text, entity)
        )
        search_from = processed_end

    original_offset = 0
    for (
        processed_start,
        processed_end,
        marker,
        original_text,
        entity,
    ) in located_entities:
        original_start = processed_start + original_offset
        location = entity.get("location")
        if location is None:
            location = {}
            entity["location"] = location
        elif not isinstance(location, dict):
            raise ValueError("Entity 'location' must be an object")
        elif clear_existing:
            location.clear()

        location.setdefault("stt_idx", original_start)
        location.setdefault("end_idx", original_start + len(original_text))
        location.setdefault("stt_idx_processed", processed_start)
        location.setdefault("end_idx_processed", processed_end)
        original_offset += len(original_text) - len(marker)


def _enhance_pdf_redact_response(response: TextResponse) -> TextResponse:
    """
    Enhance PDF text responses with OCR text locations to enable downstream post-processing
    and re-identificatiom.

    Args:
        reponse: a redacted text repsonse

    Returns:
        a redacted text response.
    """
    json_response = response.body
    redact_list = json_response if isinstance(json_response, list) else [json_response]
    if not redact_list or any(
        not isinstance(redact_blk, dict)
        or "processed_text" not in redact_blk
        or "entities" not in redact_blk
        for redact_blk in redact_list
    ):
        raise ValueError(
            "Response must contain a response object or list with "
            "'processed_text' and 'entities'"
        )

    for redact_blk in redact_list:
        blk_processed_text = redact_blk["processed_text"]
        blk_entities = redact_blk["entities"]

        # validate ResponseText structure
        if not isinstance(blk_processed_text, str) or isinstance(blk_entities, str):
            raise ValueError(
                "{json_file} response rows must have string 'processed_text' "
                "and list 'entities' values"
            )

        if "characters_processed" not in redact_blk:
            redact_blk.setdefault("characters_processed", None)
        # repopulate entity locations into PDF entities
        _populate_entity_locations(blk_processed_text, blk_entities, False)
    # make a new response
    response = Response()
    response.status_code = 200
    response._content = json.dumps(redact_list).encode("utf-8")
    response.headers["Content-Type"] = "application/json"
    return TextResponse(response)
