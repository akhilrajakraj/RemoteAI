"""Desktop capabilities are intentionally not enabled in the initial scaffold.

Add narrowly scoped, user-approved actions here. Never expose unrestricted shell
execution or arbitrary filesystem access through the assistant API.
"""


def available_tools() -> list[dict[str, str]]:
    return []
