run:
\tstreamlit run streamlit_app/Home.py

install:
\tpython -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

fmt:
\tpython -m pip install ruff && ruff check --fix .

