from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base

class MovieRating(Base):
    __tablename__ = "movie_ratings"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("score >= 1 AND score <= 10", name="ck_rating_score_range"),
    )

    movie = relationship("Movie", back_populates="ratings")
