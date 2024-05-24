from package_layer import package_layer

config = {
    'lambda_layer_fpl_common_deps': {
        "pypi_files": [
            'https://files.pythonhosted.org/packages/1a/5e/71bb0eef0dc543f7516d9ddeca9ee8dc98207043784e3f7e6c08b4a6b3d9/pandas-2.2.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl',
            'https://files.pythonhosted.org/packages/54/30/c2a907b9443cf42b90c17ad10c1e8fa801975f01cb9764f3f8eb8aea638b/numpy-1.26.4-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
        ],
        "pip_commands": [
            "pip install --only-binary=:all: --platform=manylinux1_x86_64 --implementation=cp --python-version=39 \
            pytz==2024.1 requests==2.25.1 psycopg2-binary SQLAlchemy==2.0.29  python-dotenv==1.0.1"
        ],
        "helper_files": ['../utilities/db_helpers.py']
    },
    'lambda_layer_lightgbm': {
        "pypi_files": [],
        "pip_commands": [
            "pip install lightgbm==4.3.0"
        ],
        "helper_files": []
    }
}

if __name__ == '__main__':
    for output_zip_file, v in config.items():
        package_layer(
            output_zip_file=output_zip_file,
            pypi_files=v['pypi_files'],
            helper_files=v['helper_files'],
            pip_commands=v['pip_commands']
        )