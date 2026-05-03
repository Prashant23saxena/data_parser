import _bootstrap  # noqa: F401

from kriyax_workbench.llm import runtime_status


for key, value in runtime_status().items():
    print(f"{key}: {value}")
