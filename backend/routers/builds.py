from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import os

router = APIRouter()


@router.get("/builds")
async def list_builds():
    builds_dir = Path(__file__).parent.parent / "assets" / "builds"
    if not builds_dir.exists():
        return {"builds": []}

    builds = []
    for file in builds_dir.glob("pm_assistant_*.zip"):
        builds.append(
            {
                "name": file.name,
                "size": file.stat().st_size,
                "created_at": file.stat().st_mtime,
            }
        )

    return {"builds": sorted(builds, key=lambda x: x["created_at"], reverse=True)}


@router.get("/builds/{build_name}")
async def download_build(build_name: str):
    builds_dir = Path(__file__).parent.parent / "assets" / "builds"
    build_path = builds_dir / build_name

    if not build_path.exists():
        raise HTTPException(status_code=404, detail="Build not found")

    return FileResponse(
        path=build_path, filename=build_name, media_type="application/zip"
    )
