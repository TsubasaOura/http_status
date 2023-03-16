FROM python:3.10-buster
WORKDIR /python
RUN pip install poetry && \
    poetry config --local virtualenvs.create true && \
    poetry config --local cache-dir .cache/pypoetry && \
    poetry config --local virtualenvs.in-project true
ENV PATH=/python/.venv/bin:$PATH
