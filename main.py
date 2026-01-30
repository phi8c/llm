import chainlit as cl
import asyncio


from concurrent.futures import ThreadPoolExecutor
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import json


import ingest.ui  # 👈 BẮT BUỘC để Chainlit register action callbacks

from llm.ollama_llm import load_llm
from router.chat import run_chat_sync
from db.users import get_user_role
from db.feedback import add_rule
from db.chat import save_chat
from chainlit.types import ThreadDict
from db.data_layer import SupabaseDataLayer
import sys
from router.classifier import classify_question
from rag.retriever import retrieve_context


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()


supabase_url = os.environ.get("SUPABASE_PROJECT_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


cl.data_layer = SupabaseDataLayer()

executor = ThreadPoolExecutor(max_workers=1)

from llm.ollama_llm import call_llm

print(f"DEBUG: Current Data Layer: {cl.data_layer}")
print(f"DEBUG: Has get_user attr: {hasattr(cl.data_layer, 'get_user')}")

@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": username, 
            "password": password
        })
        
        if res.user:
            user_id = res.user.id
            
            role = get_user_role(user_id)
            print(f">>> [AUTH SUCCESS] User ID: {user_id}")
           
            return cl.User(identifier=str(user_id), metadata={"role": role, "email": username})
    except Exception as e:
        print(f"Login error: {e}")
        return None

@cl.on_chat_start
async def start():
    load_llm()
    user = cl.user_session.get("user")
    
    if not user:
        await cl.ErrorMessage(content="Vui lòng đăng nhập lại.").send()
        return

    cl.user_session.set("user_info", {
        "id": user.identifier,
        "email": user.metadata.get("email"),
        "role": user.metadata.get("role"),
    })

    await cl.Message(
        content=f"✅ **Đã kết nối**\n👤 `{user.metadata.get('email'), {user.metadata.get('role')}}`",
        actions=[
            # 👇 CHỈ ADMIN MỚI THẤY
            *(
                [
                    cl.Action(
                        name="open_ingest",
                        label="📥 Build dữ liệu (Admin)",
                        payload={},   
                    )
                ]
                if user.metadata.get("role") == "admin"
                else []
            )
        ],
    ).send()

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
   
    user = cl.user_session.get("user")
    if user:
        cl.user_session.set("user_info", {
            "id": user.identifier,
            "email": user.metadata.get("email"),
            "role": user.metadata.get("role"),
        })
    print(f"--- [RESUME] Thread ID: {thread.get('id')}")

@cl.on_message
async def main(message: cl.Message):
    user_info = cl.user_session.get("user_info")

    if not user_info:
        await cl.Message("❌ Session error").send()
        return

   
    cl.user_session.set("rag_mode", False)
    

    current_thread_id = cl.context.session.thread_id
    loop = asyncio.get_running_loop()

    try:
      
        question_type = classify_question(
            role=user_info["role"],
            question=message.content,
        )
        cl.user_session.set("question_type", question_type)
        print("📘 Question type:", question_type)
        if user_info["role"] == "model_only":
           
            msg = call_llm(message.content)
            rag_mode = False
            similarity = 0.0

        else:
            cl.user_session.set("question_type", question_type) 
            raw = await loop.run_in_executor(
                executor,
                run_chat_sync,
                message.content,
                {
        **user_info,
        "question_type": question_type,  
    }
                
                 
            )
            print("📦 RAW BACKEND =", raw)
            
            
            if isinstance(raw, dict):
                msg = raw.get("answer", "")
                rag_mode = raw.get("rag_mode", False)
                similarity = raw.get("similarity", 0.0)
                question_type = raw.get("question_type")   
                cl.user_session.set("question_type", question_type)  
                
            else:
                msg = str(raw)
                rag_mode = False
                similarity = 0.0
            
            
            
            
        
        cl.user_session.set("rag_mode", rag_mode)
        print("✅ FINAL rag_mode =", rag_mode)

       
        display_content = f"✅ {msg}" if msg else "⚠️ Không có nội dung trả lời."

        
        cl.user_session.set("last_question", message.content)
        cl.user_session.set("last_answer", msg)

        await cl.Message(
            content=display_content,
            actions=[
                cl.Action(name="answer_correct", label="👍 Đúng", payload={"msg": "correct"}),
                cl.Action(name="answer_wrong", label="👎 Sai", payload={"msg": "wrong"}),
            ],
        ).send()

       
        try:
            save_chat(
                thread_id=current_thread_id,
                user_id=user_info["id"],
                role=user_info["role"],
                question=message.content,
                result_data=msg,
            )
        except Exception as db_err:
            print(f"❌ Lỗi lưu DB: {db_err}")

    except Exception as e:
        await cl.Message(f"❌ Lỗi: {e}").send()

        




from feedbacks.mapper import map_feedback_to_error_type, map_error_type_to_semantic
from feedbacks.error import ERROR_TO_POLICY
from feedbacks.rule_generator import generate_rule


async def process_feedback(level1: str, level2: str | None):
    user_info = cl.user_session.get("user_info")

    error_type = map_feedback_to_error_type(level1, level2)
    action = ERROR_TO_POLICY.get(error_type, "IGNORE")
    
    
    
    

    if action != "GENERATE_RULE":
        await cl.Message("📌 Đã ghi nhận phản hồi.").send()
        return
    error_semantic = map_error_type_to_semantic(error_type)
    
    print("in ra error_semantic", error_semantic)
    question_type=cl.user_session.get("question_type")
    print("in ra question_type", question_type)

    rule = generate_rule(
        question=cl.user_session.get("last_question"),
        answer=cl.user_session.get("last_answer"),
        reason=error_semantic,
        question_type=cl.user_session.get("question_type"),
    )

    if not rule:
        await cl.Message("⚠️ Không tạo được rule.").send()
        return
    

    add_rule(
        role=user_info["role"],
        rule=rule,
        rule_type=error_type,
        question_type=cl.user_session.get("question_type"),
    )

    await cl.Message(
        content=f"📌 Đã ghi nhận nguyên tắc chung:\n- {rule}"
    ).send()



        
        
@cl.action_callback("answer_wrong")
async def answer_wrong(action: cl.Action):
    await cl.Message(
        content="Theo bạn, câu trả lời sai ở điểm nào?",
        actions=[
            cl.Action(
                name="feedback_general",
                label="❌ Lấy sai kiến thức",
                payload={"level1": "F1"},
            ),
            cl.Action(
                name="feedback_general",
                label="❌ Thiếu thông tin cần thiết",
                payload={"level1": "F2"},
            ),
            cl.Action(
                name="feedback_general",
                label="❌ Trả lời suy diễn",
                payload={"level1": "F3"},
            ),
            cl.Action(
                name="feedback_general",
                label="❌ Trả lời không đúng trọng tâm",
                payload={"level1": "F5"},
            ),
        ],
    ).send()
@cl.action_callback("feedback_general")
async def feedback_general(action: cl.Action):
    level1 = action.payload.get("level1")
    cl.user_session.set("feedback_level_1", level1)

    # Chỉ F1 mới hỏi tiếp
    if level1 == "F1":
        await cl.Message(
            content="Theo bạn, hệ thống lấy sai kiến thức ở đâu?",
            actions=[
                cl.Action(
                    name="feedback_detail",
                    label="Sai lĩnh vực (HR / IT)",
                    payload={"level2": "F1.1"},
                ),
                cl.Action(
                    name="feedback_detail",
                    label="Không đúng loại chính sách",
                    payload={"level2": "F1.2"},
                ),
                cl.Action(
                    name="feedback_detail",
                    label="Không rõ dựa trên tài liệu nào",
                    payload={"level2": "F1.3"},
                ),
            ],
        ).send()
    else:
        await process_feedback(level1, None)
@cl.action_callback("feedback_detail")
async def feedback_detail(action: cl.Action):
    level2 = action.payload.get("level2")
    level1 = cl.user_session.get("feedback_level_1")

    await process_feedback(level1, level2)









