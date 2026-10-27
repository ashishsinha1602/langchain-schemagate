# Copyright 2026 Ashish Sinha. Licensed under the Apache License, Version 2.0.
"""LangChain integration for schemagate: an identity-scoped schema retriever for text-to-SQL.

    from schemagate import Catalog, Principal
    from langchain_schemagate import SchemagateRetriever

    cat = Catalog().bootstrap("postgresql://localhost/app")
    retriever = SchemagateRetriever(catalog=cat, top_k=6,
                                    principal=Principal("okta:jdoe", roles={"finance"}))
    docs = retriever.invoke("revenue by month")   # one Document of DDL per selected table

The retriever is maintained in schemagate itself (``schemagate.integrations.langchain``); this
package is the ``langchain-<name>`` distribution LangChain lists integrations under.
"""
from schemagate.integrations.langchain import SchemagateRetriever, prompt_fragment

__all__ = ["SchemagateRetriever", "prompt_fragment"]
