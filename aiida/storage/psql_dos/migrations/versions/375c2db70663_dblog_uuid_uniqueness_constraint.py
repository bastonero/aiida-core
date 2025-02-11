# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
# pylint: disable=invalid-name,no-member
"""This migration adds uniqueness constraint to the UUID column.

This migration corresponds to the 0024_dblog_update Django migration.

Revision ID: 375c2db70663
Revises: ea2f50e7f615
Create Date: 2019-01-30 20:26:16.550071

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '375c2db70663'
down_revision = 'ea2f50e7f615'
branch_labels = None
depends_on = None


def upgrade():
    """Migrations for the upgrade."""
    op.create_unique_constraint('db_dblog_uuid_key', 'db_dblog', ['uuid'])


def downgrade():
    """Migrations for the downgrade."""
    op.drop_constraint('db_dblog_uuid_key', 'db_dblog')
