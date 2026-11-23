"""API đọc U09 có kiểm hash; legacy U04 tiếp tục dùng reader và schema riêng."""
from __future__ import annotations

from pathlib import Path

from flask import Blueprint, Response, jsonify, request

from core.research_results import PACKAGE, RUN_ID, ResearchResults
from utils.experiment_io import run_path
from utils.research_view import export_bytes, view

ROOT = Path(__file__).resolve().parents[1]
research = Blueprint("research_results", __name__, url_prefix="/api/research-results")


@research.get("/runs")
def catalog() -> Response | tuple[Response, int]:
    """Chỉ nhận U09 đã verify và namespace legacy nằm trong workspace."""
    runs = []
    try:
        if (ROOT / PACKAGE).is_file():
            reader = ResearchResults(ROOT)
            runs.append({"id": RUN_ID, "kind": "paper_evidence", "label": "U09 · Research102",
                         "status": "completed", "points": 102, "repeats": 3,
                         "package_sha256": reader.provenance()["package_sha256"]})
        base = ROOT / "outputs/unified_integration"
        if not base.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError("Namespace legacy thoát workspace")
        for path in sorted(base.iterdir()) if base.exists() else []:
            if (path.is_dir() and (path / "identity.json").is_file() and (path / "result.json").is_file()
                    and run_path(ROOT, path.name).resolve() == path.resolve()):
                runs.append({"id": path.name, "kind": "legacy_offline", "label": path.name, "status": "sealed"})
        return jsonify({"version": "research_results_catalog_v1", "default": RUN_ID if any(
            r["kind"] == "paper_evidence" for r in runs) else None, "runs": runs})
    except (ValueError, KeyError, OSError):
        return jsonify({"error": "Không kiểm được gói kết quả đã khóa", "code": "RESULT_INTEGRITY_FAILURE"}), 400


@research.get("/<identifier>")
@research.get("/<identifier>/export")
def research_result(identifier: str) -> Response | tuple[Response, int]:
    """Filter chỉ chi phối projection; không gọi LLM, evaluator hoặc runtime archive."""
    if identifier != RUN_ID:
        return jsonify({"error": "Không có run U09 được công bố", "code": "RUN_NOT_FOUND"}), 404
    try:
        if any(len(request.args.getlist(key)) != 1 for key in request.args):
            raise ValueError("Filter trùng")
        query = request.args.to_dict()
        exporting = request.path.endswith("/export")
        format_name = query.pop("format", "json") if exporting else "json"
        export_table = query.pop("export_table", "summary") if exporting else "summary"
        if export_table not in ("summary", "contrasts", "bridge", "per_repeat", "classification_by_repeat", "details"):
            raise ValueError("Bảng export không hợp lệ")
        result = view(ResearchResults(ROOT), query, export=exporting)
        if exporting:
            raw, content_type = export_bytes(result, format_name, export_table)
            return Response(raw, content_type=content_type, headers={
                "Content-Disposition": f'attachment; filename="{RUN_ID}-{export_table}.{format_name}"',
                "X-Content-Type-Options": "nosniff"})
        return jsonify(result)
    except (ValueError, KeyError, OSError):
        return jsonify({"error": "Bộ lọc hoặc gói kết quả không hợp lệ", "code": "INVALID_RESULT_REQUEST"}), 400


@research.get("/<identifier>/artifacts/<name>")
def research_artifact(identifier: str, name: str) -> Response | tuple[Response, int]:
    """Chỉ artifact whitelist nguyên byte; JSON/CSV dùng attachment và nosniff."""
    if identifier != RUN_ID:
        return jsonify({"error": "Không có run được công bố"}), 404
    try:
        reader = ResearchResults(ROOT)
        raw = reader.artifact(name)
        content_type = "image/png" if name.endswith(".png") else "application/octet-stream"
        return Response(raw, content_type=content_type, headers={
            "Content-Disposition": f'attachment; filename="{name}"', "X-Content-Type-Options": "nosniff"})
    except (ValueError, KeyError, OSError):
        return jsonify({"error": "Artifact không hợp lệ"}), 400
