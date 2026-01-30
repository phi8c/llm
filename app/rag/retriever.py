# from core.rbac import allowed_scopes


# from core.rbac import allowed_scopes
from rag.index import get_index

from llama_index.core.vector_stores import (
    MetadataFilters,
    ExactMatchFilter,
)

def retrieve_context(question: str, role: str) -> str:
    index = get_index()

    filters = MetadataFilters(
        filters=[
            ExactMatchFilter(
                key="role_scope",
                value=role
            )
        ]
    )

    retriever = index.as_retriever(
        similarity_top_k=1,
        filters=filters
    )

    nodes = retriever.retrieve(question)

    return "\n\n".join(n.text for n in nodes)
