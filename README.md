# langchain-schemagate

A LangChain retriever for text-to-SQL. Each question gets only the tables it needs, picked from
the tables the caller may read. A table the caller can't read is never a candidate, so it can't
reach the prompt.

```bash
pip install langchain-schemagate
```

```python
from schemagate import Catalog, Principal
from langchain_schemagate import SchemagateRetriever, prompt_fragment

cat = Catalog().bootstrap("postgresql://localhost/app")
retriever = SchemagateRetriever(catalog=cat, top_k=6,
                                principal=Principal("okta:jdoe", roles={"finance"}))

docs = retriever.invoke("revenue by month")      # one Document of DDL per selected table
schema_for_prompt = prompt_fragment(docs)
```

It is a `BaseRetriever`, so it composes:
`retriever | RunnableLambda(prompt_fragment) | prompt | llm`. Selection runs offline (BM25 plus a
small embedder) and calls no model.

On Spider 2.0's public BigQuery and Snowflake schemas, the median database with 50+ tables went from
the full schema to a selection 91.1% smaller, in prompt tokens. On small databases there is little to
cut: 8.8% on BIRD's seven-table ones. The script and the recall trade-off are in
[schemagate's BENCHMARKS.md](https://github.com/ashishsinha1602/schemagate/blob/main/BENCHMARKS.md#prompt-tokens-on-public-schemas-the-saving-grows-with-the-schema).

The retriever itself is maintained in [schemagate](https://github.com/ashishsinha1602/schemagate),
which also has the full guide: [docs/langchain.md](https://github.com/ashishsinha1602/schemagate/blob/main/docs/langchain.md).
This package is the `langchain-<name>` distribution LangChain lists integrations under, and it runs
LangChain's standard retriever tests.

Apache-2.0.
