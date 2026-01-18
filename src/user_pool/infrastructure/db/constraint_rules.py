import re

from sqlalchemy.exc import IntegrityError

from user_pool.application.common.exceptions.base import ApplicationError


class IntegrityConstraintRule:
    def __init__(
        self,
        err_msg: str,
        returned_err: type[ApplicationError],
        returned_err_msg: str,
    ) -> None:
        self.err_msg = err_msg
        self.returned_err = returned_err
        self.returned_err_msg = returned_err_msg

    def try_map(self, exc: Exception) -> ApplicationError | None:
        if not isinstance(exc, IntegrityError):
            return None

        error_str = str(exc)
        orig_error = getattr(exc, "orig", None)

        search_texts = []

        search_texts.append(error_str)

        if orig_error:
            search_texts.append(str(orig_error))

        if hasattr(exc, "args") and exc.args:
            for arg in exc.args:
                if isinstance(arg, str):
                    search_texts.append(arg)

        constraint_patterns = [
            r'constraint "([^"]+)"',
            r"constraint ([^\s]+)",
        ]

        for text in search_texts:
            if self.err_msg in text:
                return self.returned_err(self.returned_err_msg)

            for pattern in constraint_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    found_constraint = (
                        match.group(1) if match.lastindex else match.group(0)
                    )
                    if (
                        self.err_msg in found_constraint
                        or found_constraint in self.err_msg
                    ):
                        return self.returned_err(self.returned_err_msg)

        return None
