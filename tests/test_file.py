import os

from pytest import raises

from app import app, core, error, util


def test_post_video_200(test_client):
    with open(os.path.join("tests/file_test", "video.mp4"), "rb") as f:
        response = test_client.post(
            "/api/v1/file/",
            data={"type": "video"},
            files={"file": f},
        )

    assert response.status_code == 200


def test_post_video_unsupported_type(test_client):
    with open(os.path.join("tests/file_test", "video.mp4"), "rb") as f:
        response = test_client.post(
            "/api/v1/file/",
            data={"type": "image"},
            files={"file": f},
        )
    assert response.json()["detail"] == "Formato de media invalido"


def test_post_video_422(test_client):
    with open(os.path.join("tests/file_test", "video.mp4"), "rb") as f:
        response = test_client.post(
            "/api/v1/file/",
            data={"type": "erro"},
            files={"file": f},
        )
    assert response.status_code == 422


def test_get_file_200(test_client):
    response = test_client.get(
        f"/api/v1/file/{util.list_files(core.settings.UPLOAD_DIR)[0]}"
    )
    assert response.status_code == 200


def test_get_file_422(test_client):
    response = test_client.get(f"/api/v1/file/123")
    assert response.status_code == 422


def test_get_file_404(test_client):
    response = test_client.get(f"/api/v1/file/3fa85f64-5717-4562-b3fc-2c963f66afa6")
    assert response.status_code == 404
