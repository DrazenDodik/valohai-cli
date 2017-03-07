import os

import pytest

from tests.commands.execution.utils import get_execution_data_mock
from tests.fixture_data import EXECUTION_DATA
from valohai_cli.commands.execution.outputs import outputs


@pytest.mark.parametrize('download', (False, True))
def test_execution_outputs(runner, logged_in_and_linked, tmpdir, download):
    tmpdir = str(tmpdir)

    with get_execution_data_mock() as m:
        for output in EXECUTION_DATA['outputs']:
            m.get(output['url'], content=b'0' * 100)
        params = ['7']
        if download:
            params.append('--download=%s' % tmpdir)
        output = runner.invoke(outputs, params, catch_exceptions=False).output
        assert all(o['name'] in output for o in EXECUTION_DATA['outputs'])
        if download:
            # See that things were downloaded
            for output in EXECUTION_DATA['outputs']:
                assert os.path.exists(os.path.join(tmpdir, output['name']))
