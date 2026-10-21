import json
import logging
from typing import Callable

import requests

from privateai_client.components import (
    AnalyzeTextResponse,
    FilesBase64Response,
    FilesUriResponse,
    TextResponse,
)

EntityProcessor = Callable[[dict], str]


def deidentify_text(
    text: list[str],
    response: AnalyzeTextResponse,
    entity_processors: dict[str, EntityProcessor],
    default_processor: EntityProcessor,
    convert_response: bool = False,
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
        convert_response: inidcates whether you want to modify the existing AnalyzeResponse into a TextResponse.


    Returns:
        A list of de-identified text messages, with the same length and order as the `text` argument.

    """
    # only used if convert_response
    redactions = []

    modified_texts = []
    for t, entities, chars_processed, langs in zip(
        text,
        response.entities,
        response.characters_processed,
        response.languages_detected,
    ):
        offset = 0
        modified_text = t
        # only used if convert_response
        converted_entities = []

        for entity in sorted(entities, key=lambda e: e["location"]["stt_idx"]):
            start_idx = entity["location"]["stt_idx"] + offset
            end_idx = entity["location"]["end_idx"] + offset

            # each processor is associated with the entity it should be used for using the dict key
            processor = entity_processors.get(entity["best_label"], default_processor)
            modified_entity_text = processor(entity)

            length_diff = len(modified_entity_text) - len(entity["text"])
            offset += length_diff

            modified_text = (
                modified_text[:start_idx]
                + modified_entity_text
                + modified_text[end_idx:]
            )

            # construct a new response, if client wants a text response for de-identification
            if convert_response:
                entity_details = dict(entity)
                modified_locations = entity_details["location"]
                modified_locations["stt_idx_processed"] = start_idx
                modified_locations["end_idx_processed"] = start_idx + len(
                    modified_entity_text
                )
                # add in the processed replacement text
                entity_details["processed_text"] = modified_entity_text
                converted_entities.append(entity_details)
        # add the processed text to the linked batch
        modified_texts.append(modified_text)

        if convert_response:
            redacted_msg_dtls = {
                "entities": converted_entities,
                "entities_present": len(converted_entities) > 0,
                "characters_processed": chars_processed,
                "languages_detected": langs,
                "processed_text": modified_text,
            }
            redactions.append(redacted_msg_dtls)
    # make a new response from the post-processed redaction
    if len(redactions) > 0:
        temp_response = requests.Response()
        temp_response.status_code = 200
        temp_response._content = json.dumps(redactions).encode("utf-8")
        response.response = temp_response
    return modified_texts


def post_redacted_text(
    response: TextResponse, entity_processors: dict[str, EntityProcessor]
) -> list[str]:
    """
    Post-process TextResponse from the process/text endpoint with replacement markers.

    Args:
        response: The response object returned by `PAIClient.process_text()` containing detected entities.
        entity_processors: A dictionary mapping entity types to processing functions in the format
            `{ENTITY_TYPE: entity_processor_fn}`, where `entity_processor_fn` takes an entity dictionary
            and returns modified text for all occurrences of that entity type.

    Returns:
         A list of de-identified text messages, with the transformations applied to entities specified by the entity_processor.
    """
    redactions = []
    for redacted_text_blk, entities_in_text_blk, chars_processed, langs in zip(
        response.processed_text,
        response.entities,
        response.characters_processed,
        response.languages_detected,
    ):
        offset = 0
        modified_txt_blk = redacted_text_blk
        for entity in sorted(
            entities_in_text_blk, key=lambda e: e["location"]["stt_idx"]
        ):
            curr_entity = entity["best_label"]
            # skip any entities that aren't specified by the entity_processors
            if curr_entity not in entity_processors:
                # adjust entity locations based on prior changes
                entity["location"]["stt_idx_processed"] += offset
                entity["location"]["end_idx_processed"] += offset
                continue

            start_idx = entity["location"]["stt_idx_processed"] + offset
            end_idx = entity["location"]["end_idx_processed"] + offset

            # each processor is associated with the entity it should be used for using the dict key
            processor = entity_processors.get(curr_entity)
            try:
                if processor.can_process_text_response():
                    modified_entity_text = processor(entity)

                    # use the span length, since the marker in the text includes brackets
                    length_diff = len(modified_entity_text) - (end_idx - start_idx)
                    offset += length_diff

                    modified_txt_blk = (
                        modified_txt_blk[:start_idx]
                        + modified_entity_text
                        + modified_txt_blk[end_idx:]
                    )

                    # modify the processed text response for de-identification
                    entity_locations = entity["location"]
                    entity_locations["stt_idx_processed"] = start_idx
                    entity_locations["end_idx_processed"] = start_idx + len(
                        modified_entity_text
                    )
                    # add in the processed replacement text
                    entity["processed_text"] = modified_entity_text
            except AttributeError as e:
                logging.warning(e)
                # since no changes occur when errors are raised, adjust entity
                # locations based on prior changes
                entity["location"]["stt_idx_processed"] += offset
                entity["location"]["end_idx_processed"] += offset
                continue
        # add the processed text to the linked batch
        redacted_msg_dtls = {
            "entities": entities_in_text_blk,
            "entities_present": len(entities_in_text_blk) > 0,
            "characters_processed": chars_processed,
            "languages_detected": langs,
            "processed_text": modified_txt_blk,
        }
        redactions.append(redacted_msg_dtls)
    # add all text blocks back to the response
    if len(redactions) > 0:
        temp_response = requests.Response()
        temp_response.status_code = 200
        temp_response._content = json.dumps(redactions).encode("utf-8")
        response.response = temp_response
    return response.processed_text


def reidentify_process_text(response: AnalyzeTextResponse | TextResponse) -> list[str]:
    """
    Rehydrate text that has PII removed.

    Args:
        response: The response object returned by `PAIClient.process_text()`, `PAIClient.process_files_base64()`,
            and `PAIClient.process_files_uri()`containing detected entities.
    """
    returned_text_msgs = []

    if isinstance(response, AnalyzeTextResponse):
        # if its an Analyze text response, convert it to a TextResponse
        redacted_text_key = "processed_text"
        json_resp_keys = response.body[0].keys()
        if redacted_text_key in json_resp_keys:
            response = response.to_text_response()
        else:
            err_msg = f"This response has no key '{redacted_text_key}'."
            raise KeyError(err_msg)

    # handle linked batches
    for text, entities in zip(response.processed_text, response.entities):
        rehydrated_text = text
        for entity in sorted(
            entities, key=lambda e: e["location"]["stt_idx"], reverse=True
        ):
            start_idx = entity["location"]["stt_idx_processed"]
            end_idx = entity["location"]["end_idx_processed"]
            orig_text = entity["text"]

            # put the text back together
            rehydrated_text = (
                rehydrated_text[:start_idx] + orig_text + rehydrated_text[end_idx:]
            )
        returned_text_msgs.append(rehydrated_text)
    return returned_text_msgs
