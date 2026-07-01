import asyncio
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from src.models.content import ContentIngestRequest, ContentIngestResponse
from src.services.llmService import generate_syllabus
from src.services.videoService import search_youtube
from src.services.paperService import search_arxiv
from src.services.resourceService import search_articles

router = APIRouter()

# Shared in-memory store for session course cache (kept for backward compatibility only)
course_store = {}

from src.services.verifierAgent import verify_and_map_resources
from src.services.authService import get_current_user
from src.models.user import User
from src.models.course import Course
from src.config.dbConfig import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

@router.post("/generate", response_model=ContentIngestResponse)
async def generate_course(
    payload: ContentIngestRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    request_id = str(uuid4())
    topic = payload.topic
    level = payload.level or "beginner"

    try:
        # Stage 1: Generate syllabus with queries
        syllabus = await generate_syllabus(topic, level)
        if not syllabus or "modules" not in syllabus:
            raise ValueError("Syllabus generation returned empty or malformed data.")

        # Stage 2: Fetch resources per module concurrently
        async def fetch_resources_for_module(module):
            queries = module.get("search_queries", {})
            yt_query = queries.get("youtube", f"{level} {module.get('title')} youtube")
            arxiv_query = queries.get("arxiv", f"{level} {module.get('title')} paper")
            wiki_query = queries.get("wikipedia", f"{level} {module.get('title')}")

            yt_res, arxiv_res, wiki_res = await asyncio.gather(
                search_youtube(yt_query, ""),
                search_arxiv(arxiv_query, ""),
                search_articles(wiki_query, "")
            )

            module["raw_resources"] = {
                "youtube": yt_res,
                "arxiv": arxiv_res,
                "wikipedia": wiki_res
            }

        await asyncio.gather(*(fetch_resources_for_module(mod) for mod in syllabus.get("modules", [])))

        # Stage 3: Verifier Agent to filter and map resources
        verified_syllabus = await verify_and_map_resources(syllabus, level)

        # Persist Course to PostgreSQL/SQLite database asynchronously
        new_course = Course(
            id=request_id,
            user_id=current_user.id,
            topic=topic,
            level=level,
            syllabus=verified_syllabus
        )
        db.add(new_course)
        await db.commit()

        # Cache in memory too just in case of any backward compatibility fallback
        flat_content = []
        for mod in verified_syllabus.get("modules", []):
            for res in mod.get("resources", []):
                flat_content.append(res)
        course_store[request_id] = {
            "syllabus": verified_syllabus,
            "content": flat_content
        }

        return ContentIngestResponse(
            status="completed",
            topic=topic,
            request_id=request_id,
            syllabus=verified_syllabus
        )
    except Exception as e:
        import traceback
        import logging
        logging.getLogger(__name__).error(f"Generation failed: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
