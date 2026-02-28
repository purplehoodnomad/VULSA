# from clickhouse_sqlalchemy import engines
# from sqlalchemy import Column, Integer, DateTime, UUID, text
# from infrastructure.sqlalchemy.base import Base


# class ClicksByDateCH(Base):
#     __tablename__ = "clicks_by_date"
#     __table_args__ = (
#         engines.MergeTree(
#             partition_by=text("toYYYYMM(date)"),
#             order_by=("link_id", "date", "hour"),
#         ),
#         {"extend_existing": True}
#     )

#     link_id = Column(UUID, primary_key=True)
#     date = Column(DateTime, primary_key=True)
#     hour = Column(Integer, primary_key=True)
#     clicks_count = Column(Integer)