"""Blueprint chỉ đọc/kiểm kết quả offline, không mở đường hosted ngoài release."""
from __future__ import annotations

from pathlib import Path

from flask import Blueprint, Response, jsonify, render_template, request

from core.unified_contracts import ExperimentSpec, digest
from core.variant_registry import registry_document
from utils.experiment_io import export_bytes, run_path
from utils.i18n import normalize_lang
from utils.research_i18n import messages
from core.serving_registry import registry_document as serving_registry

ROOT = Path(__file__).resolve().parents[1]
experiments = Blueprint("experiments", __name__)


@experiments.get("/experiments")
def experiment_page() -> str:
    """Danh mục và bộ lọc dùng cùng IDs với CLI/evaluator."""
    base = ROOT / "outputs/unified_integration"
    runs = [p.name for p in sorted(base.iterdir()) if p.is_dir() and (p / "identity.json").is_file() and (p / "result.json").is_file()] if base.exists() else []
    language = normalize_lang(request.args.get("lang") or request.cookies.get("qa_lang")
                              or request.accept_languages.best_match(("vi", "en")))
    return render_template("experiments.html", registry=registry_document(), runs=runs,
                           serving_registry=serving_registry(), LANG=language, E=messages(language))


@experiments.get("/api/experiments/registry")
def experiment_registry() -> Response:
    """Chỉ metadata, không import hoặc nạp student/bank."""
    return jsonify(registry_document())


@experiments.post("/api/experiments/validate")
def experiment_validate() -> Response | tuple[Response, int]:
    """Kiểm cấu trúc không tạo run, không cấp quyền inference."""
    try:
        spec = ExperimentSpec.create(request.get_json())
        return jsonify({"status": "VALID_SPEC_ONLY", "identity_sha256": digest(spec.identity), "hosted_release": False})
    except (ValueError, TypeError, KeyError):
        return jsonify({"error": "Cấu hình thí nghiệm không hợp lệ"}), 400


@experiments.get("/api/experiments/<identifier>")
@experiments.get("/api/experiments/<identifier>/export")
def experiment_result(identifier: str) -> Response | tuple[Response, int]:
    """Mọi JSON/CSV phải qua cùng cold evaluator trước khi gửi trình duyệt."""
    from core.unified_experiment import verify_run
    try:
        path = run_path(ROOT, identifier)
        if not (path / "result.json").is_file():
            return jsonify({"error": "Không có kết quả đã seal"}), 404
        result = verify_run(path, root=ROOT)
        if request.path.endswith("/export"):
            format_name = request.args.get("format", "csv")
            raw, content_type = export_bytes(result, format_name)
            return Response(raw, content_type=content_type,
                headers={"Content-Disposition": f'attachment; filename="{identifier}.{format_name}"'})
        return jsonify(result)
    except (ValueError, TypeError, KeyError, OSError):
        return jsonify({"error": "Kết quả không khớp nguồn hoặc hợp đồng đã khóa"}), 400
