"""source_channels

Revision ID: 0002
Revises: 0001
Create Date: 2025-05-11 12:40:39.051168

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO simplestream_sources (index_url)
        VALUES 
            ('https://images.maas.io/ephemeral-v3/stable/streams/v1/com.ubuntu.maas:stable:1:bootloader-download.json'),
            ('https://images.maas.io/ephemeral-v3/stable/streams/v1/com.ubuntu.maas:stable:centos-bases-download.json'),
            ('https://images.maas.io/ephemeral-v3/stable/streams/v1/com.ubuntu.maas:stable:v3:download.json'),
            ('https://images.maas.io/ephemeral-v3/candidate/streams/v1/com.ubuntu.maas:candidate:1:bootloader-download.json'),
            ('https://images.maas.io/ephemeral-v3/candidate/streams/v1/com.ubuntu.maas:candidate:centos-bases-download.json'),
            ('https://images.maas.io/ephemeral-v3/candidate/streams/v1/com.ubuntu.maas:candidate:v3:download.json')
            ;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM simplestream_sources
        WHERE index_url IN (
            'https://images.maas.io/ephemeral-v3/stable/streams/v1/com.ubuntu.maas:stable:1:bootloader-download.json',
            'https://images.maas.io/ephemeral-v3/stable/streams/v1/com.ubuntu.maas:stable:centos-bases-download.json',
            'https://images.maas.io/ephemeral-v3/stable/streams/v1/com.ubuntu.maas:stable:v3:download.json'
        );
    """)
