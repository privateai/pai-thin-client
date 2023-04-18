from .components import request_objects as req_objects

class request_objects:

    bleep = req_objects.BleepRequest
    file_url = req_objects.ProcessFileUriRequest
    file_base64 = req_objects.ProcessFileBase64Request
    process_text = req_objects.ProcessTextRequest
    audio_options = req_objects.AudioOptions
    entity_type_selector = req_objects.EntityTypeSelector
    entity_detection = req_objects.EntityDetection
    file = req_objects.File
    filter_selector = req_objects.FilterSelector
    pdf_options = req_objects.PDFOptions
    processed_text = req_objects.ProcessedText
    timestamp = req_objects.Timestamp

