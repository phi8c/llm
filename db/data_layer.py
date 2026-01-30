import chainlit as cl
from chainlit.data import BaseDataLayer
from chainlit.types import (
    ThreadDict,
    ThreadFilter,
    Pagination,
    PaginatedResponse,
    PageInfo,
)
from supabase import create_client
from typing import Optional, Dict, Any, List
import os
import json


supabase = create_client(
    os.environ["SUPABASE_PROJECT_URL"],
    os.environ["SUPABASE_KEY"],
)


class SupabaseDataLayer(BaseDataLayer):
    """
    Chainlit 2.9.5
    - NO DATABASE_URL
    - NO asyncpg
    - ONLY Supabase REST
    """

    # ======================
    # USER (bắt buộc)
    # ======================
    async def get_user(self, identifier: str) -> Optional[cl.User]:
        # Chainlit chỉ cần != None để cho sidebar chạy
        return cl.User(identifier=identifier, metadata={})

    async def create_user(self, user: cl.User):
        return user

    # ======================
    # SIDEBAR – LIST THREADS
    # ======================
    async def list_threads(
        self,
        pagination: Pagination,
        filter: ThreadFilter,
    ) -> PaginatedResponse[ThreadDict]:

        user_id = getattr(filter, "userIdentifier", None)
        if not user_id:
            return PaginatedResponse([], PageInfo(False, None, None))

        limit = pagination.first or 40

        res = (
            supabase.table("chat_history")
            .select("thread_id, question, created_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit * 3)  # phòng trùng thread_id
            .execute()
        )

        seen = set()
        threads: List[ThreadDict] = []

        for row in res.data or []:
            tid = row["thread_id"]
            if tid in seen:
                continue

            seen.add(tid)

            threads.append(
                ThreadDict(
                    id=str(tid),
                    name=(row.get("question") or "Chat")[:50],
                    userIdentifier=user_id,
                    createdAt=row["created_at"],
                    metadata={},
                )
            )

            if len(threads) >= limit:
                break

        return PaginatedResponse(
            threads,
            PageInfo(False, None, None),
        )

    # ======================
    # LOAD THREAD
    # ======================
    async def get_thread(self, thread_id: str) -> Optional[ThreadDict]:

        res = (
            supabase.table("chat_history")
            .select("*")
            .eq("thread_id", thread_id)
            .order("created_at", desc=False)
            .execute()
        )

        rows = res.data or []
        if not rows:
            return None

        steps = []

        for r in rows:
            # USER
            steps.append(
                {
                    "id": f"user_{r['id']}",
                    "threadId": thread_id,
                    "type": "human",
                    "output": r["question"],
                    "createdAt": r["created_at"],
                }
            )

            # ASSISTANT
            ans = r["answer"]
            if isinstance(ans, dict):
                ans = ans.get("message", json.dumps(ans))
            else:
                try:
                    parsed = json.loads(ans)
                    ans = parsed.get("message", ans)
                except:
                    pass

            steps.append(
                {
                    "id": f"ai_{r['id']}",
                    "threadId": thread_id,
                    "type": "assistant",
                    "output": ans,
                    "createdAt": r["created_at"],
                }
            )

        first = rows[0]

        return ThreadDict(
            id=thread_id,
            name=(first["question"] or "Chat")[:50],
            userIdentifier=first["user_id"],
            createdAt=first["created_at"],
            steps=steps,
            metadata={},
        )

    # ======================
    # STUBS (bắt buộc)
    # ======================
    async def create_thread(self, thread: ThreadDict): pass
    async def update_thread(self, thread_id: str, **kwargs): pass
    async def delete_thread(self, thread_id: str): pass

    async def create_step(self, step_dict: Dict): pass
    async def update_step(self, step_dict: Dict): pass
    async def delete_step(self, step_id: str): pass

    async def create_element(self, element_dict: Dict): pass
    async def get_element(self, thread_id: str, element_id: str): return None
    async def delete_element(self, element_id: str): pass

    async def upsert_feedback(self, feedback: Any): pass
    async def delete_feedback(self, feedback_id: str): pass

    async def get_favorite_steps(self, user_identifier: str): return []
    async def get_thread_author(self, thread_id: str) -> str: return ""
    async def build_debug_url(self) -> str: return ""
    async def close(self): pass
