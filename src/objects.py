from .components import request_objects as req_objects

class request_objects:

    bleep_obj = req_objects.BleepRequest
    file_uri_obj = req_objects.ProcessFileUriRequest
    file_base64_obj = req_objects.ProcessFileBase64Request
    process_text_obj = req_objects.ProcessTextRequest
    audio_options_obj = req_objects.AudioOptions
    entity_type_selector_obj = req_objects.EntityTypeSelector
    entity_detection_obj = req_objects.EntityDetection
    file_obj = req_objects.File
    filter_selector_obj = req_objects.FilterSelector
    pdf_options_obj = req_objects.PDFOptions
    processed_text_obj = req_objects.ProcessedText
    timestamp_obj = req_objects.Timestamp

