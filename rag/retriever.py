


from rag.index import get_index
from llama_index.core.vector_stores import (
    MetadataFilters,
    ExactMatchFilter,
)


def _adaptive_top_k(question: str) -> int:
    """
    Điều chỉnh top-K theo độ dài câu hỏi
    (tránh nhiễu + tránh miss)
    """
    length = len(question.split())

    if length <= 4:
        return 3
    if length <= 10:
        return 5
    return 8


def retrieve_context(question: str, role: str):
    index = get_index()

    top_k = _adaptive_top_k(question)

    retriever = index.as_retriever(
        similarity_top_k=top_k,
        use_mmr=False,
        filters=MetadataFilters(
            filters=[
                ExactMatchFilter(
                    key="role_scope",
                    value=role)
            ]
        ),
    )

    nodes = retriever.retrieve(question)

    contexts = [
        n.node.get_content()
        for n in nodes
        if n.node.get_content() and len(n.node.get_content()) > 120
    ]
    print("in ra context", contexts)

    return contexts


