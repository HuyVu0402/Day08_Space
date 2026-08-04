# RAG Evaluation Results

## Overall Scores

| Metric | Score |
|---|---:|
| faithfulness | 0.117 |
| relevance | 0.145 |
| context_recall | 0.073 |
| context_precision | 0.422 |

## A/B Comparison

| Config | Faithfulness | Relevance | Context Recall | Context Precision |
|---|---:|---:|---:|---:|
| hybrid_rerank | 0.113 | 0.136 | 0.072 | 0.422 |
| compact_context | 0.115 | 0.141 | 0.072 | 0.422 |

## Notes

- Evaluation uses a lightweight overlap-based heuristic rather than a full LLM judge, so it is a practical proxy for lab submission.
- The pipeline runs the current retrieval + generation flow over the golden questions to produce a reproducible report.
