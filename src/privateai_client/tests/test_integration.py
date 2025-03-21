import base64
import os

from dotenv import load_dotenv

from ..objects import request_objects as rq
from ..pai_client import PAIClient

load_dotenv()


def _get_client():
    client = PAIClient(url=os.environ["PAI_API_URL"])
    if os.getenv("PAI_API_KEY"):
        client.add_api_key(os.getenv("PAI_API_KEY"))
    return client


def test_ping():
    client = _get_client()
    assert client.ping() == True


def test_text_only():
    client = _get_client()
    req = rq.process_text_obj(text=["Hey there!"])
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_default():
    client = _get_client()
    req = rq.process_text_obj(
        text=["Hey there!"], entity_detection=rq.entity_detection_obj()
    )
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_coref_model_prediction():
    client = _get_client()
    req = rq.process_text_obj(
        text=["Hey there!"],
        entity_detection=rq.entity_detection_obj(),
        processed_text=rq.processed_text_obj(
            type="MARKER", coreference_resolution="model_prediction"
        ),
    )
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_coref_heuristic():
    client = _get_client()
    req = rq.process_text_obj(
        text=["Hey there!"],
        entity_detection=rq.entity_detection_obj(),
        processed_text=rq.processed_text_obj(
            type="MARKER", coreference_resolution="heuristics"
        ),
    )
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_coref_combined():
    client = _get_client()
    req = rq.process_text_obj(
        text=["Hey there!"],
        entity_detection=rq.entity_detection_obj(),
        processed_text=rq.processed_text_obj(
            type="MARKER", coreference_resolution="combined"
        ),
    )
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_with_enable_entity_types():
    client = _get_client()
    selector = rq.entity_type_selector_obj(type="ENABLE", value=["HIPAA_SAFE_HARBOR"])
    req = rq.process_text_obj(
        text=["Hey there!"],
        entity_detection=rq.entity_detection_obj(entity_types=[selector]),
    )
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_with_disable_entity_types():
    client = _get_client()
    selector = rq.entity_type_selector_obj(type="DISABLE", value=["HIPAA_SAFE_HARBOR"])
    req = rq.process_text_obj(
        text=["Hey there!"],
        entity_detection=rq.entity_detection_obj(entity_types=[selector]),
    )
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_with_allow_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW", pattern="[A-Za-z0-9]*")
    req = rq.process_text_obj(
        text=["Hey there!"], entity_detection=rq.entity_detection_obj(filter=[filter])
    )
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_with_block_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(
        type="BLOCK", pattern="[A-Za-z0-9]*", entity_type="ANY_TEXT"
    )
    req = rq.process_text_obj(
        text=["Hey there!"], entity_detection=rq.entity_detection_obj(filter=[filter])
    )
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_with_allow_text_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW_TEXT", pattern="[A-Za-z0-9]*")
    req = rq.process_text_obj(
        text=["Hey there!"], entity_detection=rq.entity_detection_obj(filter=[filter])
    )
    resp = client.process_text(req)
    assert resp.ok


def test_full_entity_detection():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW", pattern="[A-Za-z0-9]*")
    selector = rq.entity_type_selector_obj(type="ENABLE", value=["HIPAA_SAFE_HARBOR"])
    req = rq.process_text_obj(
        text=["Hey there!"],
        entity_detection=rq.entity_detection_obj(
            filter=[filter], entity_types=[selector]
        ),
    )
    resp = client.process_text(req)
    assert resp.ok


def test_processed_text_default():
    client = _get_client()
    req = rq.process_text_obj(
        text=["Hey there!"], processed_text=rq.processed_text_obj()
    )
    resp = client.process_text(req)
    assert resp.ok


def test_processed_text_marker():
    client = _get_client()
    req = rq.process_text_obj(
        text=["Hey there!"], processed_text=rq.processed_text_obj(type="MARKER")
    )
    resp = client.process_text(req)
    assert resp.ok


def test_processed_text_marker_language():
    client = _get_client()
    req = rq.process_text_obj(
        text=["Hey there!"],
        processed_text=rq.processed_text_obj(type="MARKER", marker_language="de"),
    )
    resp = client.process_text(req)
    assert resp.ok


def test_processed_text_mask():
    client = _get_client()
    req = rq.process_text_obj(
        text=["Hey there!"], processed_text=rq.processed_text_obj(type="MASK")
    )
    resp = client.process_text(req)
    assert resp.ok


def test_processed_text_synthetic():
    client = _get_client()
    req = rq.process_text_obj(
        text=["Hey there!"], processed_text=rq.processed_text_obj(type="SYNTHETIC")
    )
    resp = client.process_text(req)
    assert resp.ok


def test_project_id():
    client = _get_client()
    req = rq.process_text_obj(text=["Hey there!"], project_id="test")
    resp = client.process_text(req)
    assert resp.ok


def test_full_text_request():
    client = _get_client()
    selector = rq.entity_type_selector_obj(type="ENABLE", value=["HIPAA_SAFE_HARBOR"])
    filter = rq.filter_selector_obj(type="ALLOW", pattern="[A-Za-z0-9]*")
    req = rq.process_text_obj(
        text=["Hey there!"],
        processed_text=rq.processed_text_obj(type="MARKER"),
        entity_detection=rq.entity_detection_obj(
            filter=[filter], entity_types=[selector]
        ),
    )
    resp = client.process_text(req)
    assert resp.ok


def test_reidentify_text():
    client = _get_client()
    reid_req = rq.reidentify_text_obj(
        processed_text=["this", "is", "test", "data"],
        entities=[
            rq.entity(processed_text="this", text="that"),
            rq.entity(processed_text="is", text="was"),
            rq.entity(processed_text="test", text="real"),
            rq.entity(processed_text="data", text="nonsense"),
        ],
    )
    resp = client.reidentify_text(reid_req)
    assert resp.ok


def test_process_file_base64():
    client = _get_client()
    test_dir = "/".join(__file__.split("/")[:-1])
    with open(f"{test_dir}/test_files/simpsons_wiki.txt", "rb") as b64_file:
        file_data = base64.b64encode(b64_file.read())
        file_data = file_data.decode("ascii")
    file_obj = rq.file_obj(data=file_data, content_type="text/plain")
    request_obj = rq.file_base64_obj(file=file_obj)
    resp = client.process_files_base64(request_object=request_obj)
    assert resp.ok


def test_process_pptx_file_base64():
    client = _get_client()
    test_dir = "/".join(__file__.split("/")[:-1])
    with open(f"{test_dir}/test_files/demo-simple.pptx", "rb") as b64_file:
        file_data = base64.b64encode(b64_file.read())
        file_data = file_data.decode("ascii")
    file_obj = rq.file_obj(
        data=file_data,
        content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
    request_obj = rq.file_base64_obj(file=file_obj)
    resp = client.process_files_base64(request_object=request_obj)
    assert resp.ok


def test_process_dcm_file_base64():
    client = _get_client()
    test_dir = "/".join(__file__.split("/")[:-1])
    with open(f"{test_dir}/test_files/demo-sequence.dcm", "rb") as b64_file:
        file_data = base64.b64encode(b64_file.read())
        file_data = file_data.decode("ascii")
    file_obj = rq.file_obj(data=file_data, content_type="application/dicom")
    request_obj = rq.file_base64_obj(file=file_obj)
    resp = client.process_files_base64(request_object=request_obj)
    assert resp.ok


def test_process_audio_file_base64():
    client = _get_client()

    test_dir = "/".join(__file__.split("/")[:-1])
    file_name = "test_audio.mp3"
    filepath = os.path.join(f"{test_dir}", "test_files", file_name)
    file_type = "audio/mp3"

    with open(filepath, "rb") as b64_file:
        file_data = base64.b64encode(b64_file.read())
        file_data = file_data.decode("ascii")

    file_obj = rq.file_obj(data=file_data, content_type=file_type)
    audio_option_obj = rq.audio_options_obj(bleep_gain=-50, bleep_frequency=300)
    request_obj = rq.file_base64_obj(file=file_obj, audio_options=audio_option_obj)
    resp = client.process_files_base64(request_object=request_obj)
    assert resp.ok


def test_process_image_file_base64():
    client = _get_client()

    test_dir = "/".join(__file__.split("/")[:-1])
    file_name = "test_image.jpg"
    filepath = os.path.join(f"{test_dir}", "test_files", file_name)
    file_type = "image/jpg"

    with open(filepath, "rb") as b64_file:
        file_data = base64.b64encode(b64_file.read())
        file_data = file_data.decode("ascii")

    file_obj = rq.file_obj(data=file_data, content_type=file_type)
    image_option_obj = rq.image_options_obj(masking_method="blur", palette=True)
    request_obj = rq.file_base64_obj(file=file_obj, image_options=image_option_obj)
    resp = client.process_files_base64(request_object=request_obj)
    assert resp.ok


def test_process_ocr_image_file_base64():
    client = _get_client()

    test_dir = "/".join(__file__.split("/")[:-1])
    file_name = "test_image.jpg"
    filepath = os.path.join(f"{test_dir}", "test_files", file_name)
    file_type = "image/jpg"

    with open(filepath, "rb") as b64_file:
        file_data = base64.b64encode(b64_file.read())
        file_data = file_data.decode("ascii")

    file_obj = rq.file_obj(data=file_data, content_type=file_type)
    image_option_obj = rq.image_options_obj(masking_method="blur", palette=True)
    ocr_option_obj = rq.ocr_options_obj(ocr_system="azure_doc_intelligence")
    request_obj = rq.file_base64_obj(
        file=file_obj, image_options=image_option_obj, ocr_options=ocr_option_obj
    )
    resp = client.process_files_base64(request_object=request_obj)
    assert resp.ok


def test_object_entity_detection_default():
    client = _get_client()

    test_dir = "/".join(__file__.split("/")[:-1])
    file_name = "test_image.jpg"
    filepath = os.path.join(f"{test_dir}", "test_files", file_name)
    file_type = "image/jpg"

    with open(filepath, "rb") as b64_file:
        file_data = base64.b64encode(b64_file.read())
        file_data = file_data.decode("ascii")

    file_obj = rq.file_obj(data=file_data, content_type=file_type)
    request_obj = rq.file_base64_obj(
        file=file_obj, object_entity_detection=rq.object_entity_detection_obj()
    )
    resp = client.process_files_base64(request_object=request_obj)
    assert resp.ok


def test_object_entity_detection_with_enable_entity_types():
    client = _get_client()

    test_dir = "/".join(__file__.split("/")[:-1])
    file_name = "test_image.jpg"
    filepath = os.path.join(f"{test_dir}", "test_files", file_name)
    file_type = "image/jpg"

    with open(filepath, "rb") as b64_file:
        file_data = base64.b64encode(b64_file.read())
        file_data = file_data.decode("ascii")

    file_obj = rq.file_obj(data=file_data, content_type=file_type)
    selector = rq.object_entity_type_selector_obj(type="ENABLE", value=["LOGO"])
    request_obj = rq.file_base64_obj(
        file=file_obj,
        object_entity_detection=rq.object_entity_detection_obj(
            object_entity_types=[selector]
        ),
    )
    resp = client.process_files_base64(request_object=request_obj)
    assert resp.ok


def test_object_entity_detection_with_disable_entity_types():
    client = _get_client()

    test_dir = "/".join(__file__.split("/")[:-1])
    file_name = "test_image.jpg"
    filepath = os.path.join(f"{test_dir}", "test_files", file_name)
    file_type = "image/jpg"

    with open(filepath, "rb") as b64_file:
        file_data = base64.b64encode(b64_file.read())
        file_data = file_data.decode("ascii")

    file_obj = rq.file_obj(data=file_data, content_type=file_type)
    selector = rq.object_entity_type_selector_obj(type="DISABLE", value=["SIGNATURE"])
    request_obj = rq.file_base64_obj(
        file=file_obj,
        object_entity_detection=rq.object_entity_detection_obj(
            object_entity_types=[selector]
        ),
    )
    resp = client.process_files_base64(request_object=request_obj)
    assert resp.ok


def test_bleep():
    client = _get_client()

    test_dir = "/".join(__file__.split("/")[:-1])
    file_name = "test_audio.mp3"
    filepath = os.path.join(f"{test_dir}", "test_files", file_name)
    file_type = "audio/mp3"

    with open(filepath, "rb") as b64_file:
        file_data = base64.b64encode(b64_file.read())
        file_data = file_data.decode("ascii")

    file_obj = rq.file_obj(data=file_data, content_type=file_type)
    timestamp = rq.timestamp_obj(start=1.0, end=2.0)

    request_obj = rq.bleep_obj(
        file=file_obj, timestamps=[timestamp], bleep_frequency=500, bleep_gain=-30
    )
    resp = client.bleep(request_object=request_obj)
    assert resp.ok


def test_ner_text_only():
    client = _get_client()
    req = rq.ner_text_obj(text=["Hey there!"])
    resp = client.ner_text(req)
    assert resp.ok


def test_ner_entity_detection_default():
    client = _get_client()
    req = rq.ner_text_obj(
        text=["Hey there!"], entity_detection=rq.entity_detection_obj()
    )
    resp = client.ner_text(req)
    assert resp.ok


def test_ner_entity_detection_with_enable_entity_types():
    client = _get_client()
    selector = rq.entity_type_selector_obj(type="ENABLE", value=["HIPAA_SAFE_HARBOR"])
    req = rq.ner_text_obj(
        text=["Hey there!"],
        entity_detection=rq.entity_detection_obj(entity_types=[selector]),
    )
    resp = client.ner_text(req)
    assert resp.ok


def test_ner_entity_detection_with_disable_entity_types():
    client = _get_client()
    selector = rq.entity_type_selector_obj(type="DISABLE", value=["HIPAA_SAFE_HARBOR"])
    req = rq.ner_text_obj(
        text=["Hey there!"],
        entity_detection=rq.entity_detection_obj(entity_types=[selector]),
    )
    resp = client.ner_text(req)
    assert resp.ok


def test_ner_entity_detection_with_allow_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW", pattern="[A-Za-z0-9]*")
    req = rq.ner_text_obj(
        text=["Hey there!"], entity_detection=rq.entity_detection_obj(filter=[filter])
    )
    resp = client.ner_text(req)
    assert resp.ok


def test_ner_entity_detection_with_block_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(
        type="BLOCK", pattern="[A-Za-z0-9]*", entity_type="ANY_TEXT"
    )
    req = rq.ner_text_obj(
        text=["Hey there!"], entity_detection=rq.entity_detection_obj(filter=[filter])
    )
    resp = client.ner_text(req)
    assert resp.ok


def test_ner_entity_detection_with_allow_text_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW_TEXT", pattern="[A-Za-z0-9]*")
    req = rq.ner_text_obj(
        text=["Hey there!"], entity_detection=rq.entity_detection_obj(filter=[filter])
    )
    resp = client.ner_text(req)
    assert resp.ok


def test_ner_full_entity_detection():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW", pattern="[A-Za-z0-9]*")
    selector = rq.entity_type_selector_obj(type="ENABLE", value=["HIPAA_SAFE_HARBOR"])
    req = rq.ner_text_obj(
        text=["Hey there!"],
        entity_detection=rq.entity_detection_obj(
            filter=[filter], entity_types=[selector]
        ),
    )
    resp = client.ner_text(req)
    assert resp.ok


def test_analyze_text_only():
    client = _get_client()
    req = rq.analyze_text_obj(
        text=["Hey there!"],
        locale="en",
    )
    resp = client.analyze_text(req)
    assert resp.ok


def test_analyze_entity_detection_default():
    client = _get_client()
    req = rq.analyze_text_obj(
        text=["Hey there!"], locale="en", entity_detection=rq.entity_detection_obj()
    )
    resp = client.analyze_text(req)
    assert resp.ok


def test_analyze_entity_detection_with_enable_entity_types():
    client = _get_client()
    selector = rq.entity_type_selector_obj(type="ENABLE", value=["HIPAA_SAFE_HARBOR"])
    req = rq.analyze_text_obj(
        text=["Hey there!"],
        locale="en",
        entity_detection=rq.entity_detection_obj(entity_types=[selector]),
    )
    resp = client.analyze_text(req)
    assert resp.ok


def test_analyze_entity_detection_with_disable_entity_types():
    client = _get_client()
    selector = rq.entity_type_selector_obj(type="DISABLE", value=["HIPAA_SAFE_HARBOR"])
    req = rq.analyze_text_obj(
        text=["Hey there!"],
        locale="en",
        entity_detection=rq.entity_detection_obj(entity_types=[selector]),
    )
    resp = client.analyze_text(req)
    assert resp.ok


def test_analyze_entity_detection_with_allow_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW", pattern="[A-Za-z0-9]*")
    req = rq.analyze_text_obj(
        text=["Hey there!"],
        locale="en",
        entity_detection=rq.entity_detection_obj(filter=[filter]),
    )
    resp = client.analyze_text(req)
    assert resp.ok


def test_analyze_entity_detection_with_block_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(
        type="BLOCK", pattern="[A-Za-z0-9]*", entity_type="ANY_TEXT"
    )
    req = rq.analyze_text_obj(
        text=["Hey there!"],
        locale="en",
        entity_detection=rq.entity_detection_obj(filter=[filter]),
    )
    resp = client.analyze_text(req)
    assert resp.ok


def test_analyze_entity_detection_with_allow_text_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW_TEXT", pattern="[A-Za-z0-9]*")
    req = rq.analyze_text_obj(
        text=["Hey there!"],
        locale="en",
        entity_detection=rq.entity_detection_obj(filter=[filter]),
    )
    resp = client.analyze_text(req)
    assert resp.ok


def test_analyze_full_entity_detection():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW", pattern="[A-Za-z0-9]*")
    selector = rq.entity_type_selector_obj(type="ENABLE", value=["HIPAA_SAFE_HARBOR"])
    req = rq.analyze_text_obj(
        text=["Hey there!"],
        locale="en",
        entity_detection=rq.entity_detection_obj(
            filter=[filter], entity_types=[selector]
        ),
    )
    resp = client.analyze_text(req)
    assert resp.ok
