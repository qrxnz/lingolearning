from setuptools import setup, find_packages

setup(
    name="lingolearning",
    version="1.0.1",
    author="ninjawoda",
    license="MIT",
    # author_email="",
    description="Aplikacja tłumacząca zbudowana przy użyciu Flask. Pozwala użytkownikom na tłumaczenie tekstu pomiędzy różnymi językami oraz zapisywanie przetłumaczonych fraz w osobistym słowniku",
    url="https://github.com/ninjawoda/lingolearning",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["Flask", "requests", "langdetect", "Werkzeug"],
    python_requires=">=3.6",
    entry_points={
        "flask.commands": [
            "run = app:create_app",
        ],
    },
)
