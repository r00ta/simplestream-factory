from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey, JSON
)
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()


# Enums
class SimplestreamProductArch(enum.Enum):
    AMD64 = "AMD64"
    ARM64 = "ARM64"
    ARMHF = "ARMHF"
    I386 = "I386"
    PPC64EL = "PPC64EL"
    S390X = "S390X"


class SimplestreamChannel(enum.Enum):
    STABLE = "STABLE"
    CANDIDATE = "CANDIDATE"
    DAILY = "DAILY"


class ManifestSelection(Base):
    __tablename__ = "manifest_selection"

    id = Column(Integer, primary_key=True)
    selector_id = Column(String, nullable=False, index=True)
    version_id = Column(Integer, ForeignKey("simplestream_product_versions.id"), nullable=False)

# Models
class SimplestreamProductVersion(Base):
    __tablename__ = "simplestream_product_versions"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    properties = Column(JSON, default={})
    channel = Column(Enum(SimplestreamChannel), nullable=False)

    product_id = Column(Integer, ForeignKey("simplestream_products.id"), nullable=False)
    product = relationship("SimplestreamProduct", back_populates="versions", lazy='raise')

class SimplestreamProduct(Base):
    __tablename__ = "simplestream_products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    arch = Column(Enum(SimplestreamProductArch), nullable=False)
    os = Column(String, nullable=False)
    properties = Column(JSON, default={})

    versions = relationship(
        "SimplestreamProductVersion",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy='raise'
    )


class SimplestreamSource(Base):
    __tablename__ = "simplestream_sources"

    id = Column(Integer, primary_key=True)
    index_url = Column(String, nullable=False)
