# ingest/ui.py
import chainlit as cl
from ingest.validators import validate_files, validate_role
from ingest.service import ingest_files, precheck_files
from ingest.validators import validate_access_level





ADMIN_ROLES = {"admin"}


@cl.action_callback("open_ingest")
async def open_ingest(action: cl.Action):
    user = cl.user_session.get("user_info")

    if not user or user["role"] not in ADMIN_ROLES:
        await cl.Message("❌ Bạn không có quyền ingest dữ liệu.").send()
        return

    # 1. Upload file
    files = await cl.AskFileMessage(
        content="📎 Upload tài liệu (pdf, docx, csv, txt)",
        accept=[
            "application/pdf",
            "text/plain",
            ".docx",
            ".csv",
        ],
        max_size_mb=20,
        max_files=5,
    ).send()

    if not files:
        await cl.Message("⚠️ Không có file nào được chọn.").send()
        return

    # validate file extension
    errors = validate_files(files)
    if errors:
        await cl.Message("❌ Lỗi file:\n" + "\n".join(errors)).send()
        return

    cl.user_session.set("ingest_files", files)

    # 2. Select role_scope
    await cl.Message(
        content="🔐 Chọn role áp dụng cho tài liệu:",
        actions=[
            cl.Action(name="select_ingest_role", label="HR", payload={"role": "hr"}),
            cl.Action(name="select_ingest_role", label="IT", payload={"role": "it"}),
            cl.Action(name="select_ingest_role", label="Staff", payload={"role": "staff"}),
            cl.Action(name="select_ingest_role", label="General", payload={"role": "general"}),
        ],
    ).send()

@cl.action_callback("select_access_level")
async def select_access_level(action: cl.Action):
    level = action.payload.get("level")

    if not validate_access_level(level):
        await cl.Message("❌ Access level không hợp lệ.").send()
        return

    cl.user_session.set("ingest_access_level", level)

    role_scope = cl.user_session.get("ingest_role_scope")

    await cl.Message(
        content=(
            f"✅ Đã chọn:\n"
            f"- Role scope: `{role_scope}`\n"
            f"- Access level: `{level}`\n\n"
            "Bạn có muốn bắt đầu build dữ liệu?"
        ),
        actions=[
            cl.Action(name="confirm_ingest", label="🚀 Build dữ liệu"),
            cl.Action(name="cancel_ingest", label="❌ Huỷ"),
        ],
    ).send()

@cl.action_callback("select_ingest_role")
async def select_ingest_role(action: cl.Action):
    role_scope = action.payload.get("role")

    if not validate_role(role_scope):
        await cl.Message("❌ Role không hợp lệ.").send()
        return

    cl.user_session.set("ingest_role_scope", role_scope)

    # 👇 CHỌN ACCESS LEVEL
    await cl.Message(
        content="🔐 Chọn mức độ nhạy cảm của tài liệu:",
        actions=[
            cl.Action(
                name="select_access_level",
                label="🌐 Public (mọi role được xem)",
                payload={"level": "public"},
            ),
            cl.Action(
                name="select_access_level",
                label="🏢 Internal (HR / IT)",
                payload={"level": "internal"},
            ),
            cl.Action(
                name="select_access_level",
                label="🔒 Sensitive (chỉ HR)",
                payload={"level": "sensitive"},
            ),
        ],
    ).send()

    
async def _run_ingest(files, role_scope, user):
    access_level = cl.user_session.get("ingest_access_level")

    await cl.Message("⏳ Đang ingest dữ liệu...").send()

    result = await ingest_files(
        files=files,
        role_scope=role_scope,
        uploaded_by=user["id"],
        access_level=access_level,   # 👈 TRUYỀN XUỐNG
    )

    await cl.Message(
        content=(
            "✅ **Hoàn tất ingest**\n"
            f"- File xử lý: {result['files']}\n"
            f"- Chunk tạo: {result['chunks']}\n"
            f"- Access level: `{access_level}`"
        )
    ).send()




@cl.action_callback("confirm_ingest")
async def confirm_ingest(action: cl.Action):
    files = cl.user_session.get("ingest_files")
    role_scope = cl.user_session.get("ingest_role_scope")
    user = cl.user_session.get("user_info")

    # 🔍 PRECHECK TRÙNG TÊN FILE
    check = precheck_files(files, role_scope)

    if check["has_duplicate"]:
        cl.user_session.set("duplicated_files", check["duplicated_files"])

        await cl.Message(
            content=(
                "⚠️ **Phát hiện file trùng tên**:\n"
                + "\n".join(f"- {f}" for f in check["duplicated_files"])
                + "\n\nBạn có chắc muốn tiếp tục ingest?"
            ),
            actions=[
                cl.Action(name="force_ingest", label="⚠️ Tiếp tục ingest"),
                cl.Action(name="cancel_ingest", label="❌ Huỷ"),
            ],
        ).send()
        return

    # Không trùng → ingest luôn
    await _run_ingest(files, role_scope, user)

@cl.action_callback("force_ingest")
async def force_ingest(action: cl.Action):
    files = cl.user_session.get("ingest_files")
    role_scope = cl.user_session.get("ingest_role_scope")
    user = cl.user_session.get("user_info")

    await _run_ingest(files, role_scope, user)


