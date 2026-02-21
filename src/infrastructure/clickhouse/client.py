from typing import Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.engine import Connection


class ClickHouseClient:
    def __init__(self):
        self._engine: Optional[Engine] = None

    def init(self, dsn: str) -> None:
        if self._engine is None:
            self._engine = create_engine(dsn)

    def _ensure(self) -> Engine:
        if self._engine is None:
            raise RuntimeError("ClickHouseClient is not initialized")
        return self._engine

    @property
    def engine(self) -> Engine:
        return self._ensure()

    def connect(self) -> Connection:
        return self.engine.connect()

    def close(self) -> None:
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None