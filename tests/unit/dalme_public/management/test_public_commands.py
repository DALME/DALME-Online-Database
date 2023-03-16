"""Test the dalme_public.management module."""
import os
from unittest import mock

from dalme_public.management.commands.generate_tree import Command as GenerateTree


@mock.patch.dict(os.environ, {'ENV': 'production'})
@mock.patch('dalme_public.management.commands.generate_tree.logger')
def test_generate_tree_production(mock_logger):
    GenerateTree().handle()

    assert mock_logger.mock_calls == [
        mock.call.error('This command should never be run in production'),
    ]
