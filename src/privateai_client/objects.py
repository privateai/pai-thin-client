from .components import request_objects as req_objects


class request_objects:
    bleep_obj = req_objects.BleepRequest
    file_uri_obj = req_objects.ProcessFileUriRequest
    file_base64_obj = req_objects.ProcessFileBase64Request
    process_text_obj = req_objects.ProcessTextRequest
    ner_text_obj = req_objects.NerTextRequest
    analyze_text_obj = req_objects.AnalyzeTextRequest
    audio_options_obj = req_objects.AudioOptions
    image_options_obj = req_objects.ImageOptions
    entity = req_objects.Entity
    entity_type_selector_obj = req_objects.EntityTypeSelector
    object_entity_type_selector_obj = req_objects.ObjectEntityTypeSelector
    entity_detection_obj = req_objects.EntityDetection
    object_entity_detection_obj = req_objects.ObjectEntityDetection
    file_obj = req_objects.File
    filter_selector_obj = req_objects.FilterSelector
    pdf_options_obj = req_objects.PDFOptions
    ocr_options_obj = req_objects.OCROptions
    processed_text_obj = req_objects.ProcessedText
    reidentify_text_obj = req_objects.ReidentifyTextRequest
    timestamp_obj = req_objects.Timestamp
