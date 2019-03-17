def pytest_addoption(parser):
    parser.addoption('--aws', action='store_true', dest="aws",
                 default=False, help="enable tests needing aws lambda")

def pytest_configure(config):
    if not config.option.aws:
        setattr(config.option, 'markexpr', 'not aws')

