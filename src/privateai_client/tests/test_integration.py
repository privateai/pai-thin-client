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
    req = rq.process_text_obj(text=["Hey there!"], entity_detection=rq.entity_detection_obj())
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_with_enable_entity_types():
    client = _get_client()
    selector = rq.entity_type_selector_obj(type="ENABLE", value=["HIPAA"])
    req = rq.process_text_obj(text=["Hey there!"], entity_detection=rq.entity_detection_obj(entity_types=[selector]))
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_with_disable_entity_types():
    client = _get_client()
    selector = rq.entity_type_selector_obj(type="DISABLE", value=["HIPAA"])
    req = rq.process_text_obj(text=["Hey there!"], entity_detection=rq.entity_detection_obj(entity_types=[selector]))
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_with_allow_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW", pattern="[A-Za-z0-9]*")
    req = rq.process_text_obj(text=["Hey there!"], entity_detection=rq.entity_detection_obj(filter=[filter]))
    resp = client.process_text(req)
    assert resp.ok


def test_entity_detection_with_block_filter():
    client = _get_client()
    filter = rq.filter_selector_obj(type="BLOCK", pattern="[A-Za-z0-9]*", entity_type="ANY_TEXT")
    req = rq.process_text_obj(text=["Hey there!"], entity_detection=rq.entity_detection_obj(filter=[filter]))
    resp = client.process_text(req)
    assert resp.ok


def test_full_entity_detection():
    client = _get_client()
    filter = rq.filter_selector_obj(type="ALLOW", pattern="[A-Za-z0-9]*")
    selector = rq.entity_type_selector_obj(type="ENABLE", value=["HIPAA"])
    req = rq.process_text_obj(
        text=["Hey there!"], entity_detection=rq.entity_detection_obj(filter=[filter], entity_types=[selector])
    )
    resp = client.process_text(req)
    assert resp.ok


def test_processed_text_default():
    client = _get_client()
    req = rq.process_text_obj(text=["Hey there!"], processed_text=rq.processed_text_obj())
    resp = client.process_text(req)
    assert resp.ok


def test_processed_text_marker():
    client = _get_client()
    req = rq.process_text_obj(text=["Hey there!"], processed_text=rq.processed_text_obj(type="MARKER"))
    resp = client.process_text(req)
    assert resp.ok


def test_processed_text_mask():
    client = _get_client()
    req = rq.process_text_obj(text=["Hey there!"], processed_text=rq.processed_text_obj(type="MASK"))
    resp = client.process_text(req)
    assert resp.ok


def test_processed_text_synthetic():
    client = _get_client()
    req = rq.process_text_obj(text=["Hey there!"], processed_text=rq.processed_text_obj(type="SYNTHETIC"))
    resp = client.process_text(req)
    assert resp.ok


def test_project_id():
    client = _get_client()
    req = rq.process_text_obj(text=["Hey there!"], project_id="test")
    resp = client.process_text(req)
    assert resp.ok


def test_full_text_request():
    client = _get_client()
    selector = rq.entity_type_selector_obj(type="ENABLE", value=["HIPAA"])
    filter = rq.filter_selector_obj(type="ALLOW", pattern="[A-Za-z0-9]*")
    req = rq.process_text_obj(
        text=["Hey there!"],
        processed_text=rq.processed_text_obj(type="MARKER"),
        entity_detection=rq.entity_detection_obj(filter=[filter], entity_types=[selector]),
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
