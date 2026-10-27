"""LangChain's own standard retriever tests, plus the one property this retriever exists for."""
from typing import Type

import pytest
from langchain_tests.integration_tests import RetrieversIntegrationTests
from schemagate import Principal
from schemagate.demo_schema import demo_catalog

from langchain_schemagate import SchemagateRetriever, prompt_fragment

CATALOG = demo_catalog()   # 42 tables and views; hr_compensation readable by the payroll role only


class TestSchemagateRetriever(RetrieversIntegrationTests):
    @property
    def retriever_constructor(self) -> Type[SchemagateRetriever]:
        return SchemagateRetriever

    @property
    def retriever_constructor_params(self) -> dict:
        # without foreign-key expansion the count is exactly top_k, which the standard tests check
        return {"catalog": CATALOG, "expand_fks": False}

    @property
    def retriever_query_example(self) -> str:
        return "which customers owe us money"

    @property
    def num_results_arg_name(self) -> str:
        return "top_k"


@pytest.mark.parametrize("roles, visible", [((), False), (("payroll",), True)])
def test_a_table_the_caller_may_not_read_never_reaches_the_prompt(roles, visible):
    r = SchemagateRetriever(catalog=CATALOG, principal=Principal("okta:x", roles=set(roles)))
    assert ("hr_compensation" in prompt_fragment(r.invoke("salary and pay grade by employee"))) is visible
