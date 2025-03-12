from typing import Callable

from privateai_client.components import AnalyzeTextResponse

EntityProcessor = Callable[[dict], str]


def deidentify_text(
    text: list[str],
    response: AnalyzeTextResponse,
    entity_processors: dict[str, EntityProcessor],
    default_processor: EntityProcessor,
) -> list[str]:
    """
    Deidentifies analyzed text by processing entities with multiple processors, adjusting text dynamically.

    Args:
        text: The original list of text messages used as input in the `PAIClient.analyze_text()` call.
        response: The response object returned by `PAIClient.analyze_text()`, containing detected entities.
        entity_processors: A dictionary mapping entity types to processing functions in the format
            `{ENTITY_TYPE: entity_processor_fn}`, where `entity_processor_fn` takes an entity dictionary
            and returns modified text for all occurrences of that entity type.
        default_processor: A fallback function used to process entities not found in `entity_processors`.


    Returns:
        A list of de-identified text messages, with the same length and order as the `text` argument.

    """
    modified_texts = []
    for t, entities in zip(text, response.entities):
        offset = 0
        modified_text = t
        for entity in sorted(entities, key=lambda e: e["location"]["stt_idx"]):
            start_idx = entity["location"]["stt_idx"] + offset
            end_idx = entity["location"]["end_idx"] + offset

            processor = entity_processors.get(entity["best_label"], default_processor)
            modified_entity_text = processor(entity)

            length_diff = len(modified_entity_text) - len(entity["text"])
            offset += length_diff

            modified_text = (
                modified_text[:start_idx]
                + modified_entity_text
                + modified_text[end_idx:]
            )
        modified_texts.append(modified_text)
    return modified_texts
