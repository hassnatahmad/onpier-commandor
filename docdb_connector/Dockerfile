FROM python:3.11.4-slim as builder
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# setup venv and download or build dependencies
ENV VENV="/venv"
ENV PATH="${VENV}/bin:${PATH}"
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN python -m venv ${VENV}  && pip install --no-cache-dir -r requirements.txt

FROM python:3.11.4-slim

# setup venv with dependencies from the builder stage
ENV VENV="/venv"
ENV PATH="${VENV}/bin:$PATH"
COPY --from=builder ${VENV} ${VENV}
COPY src /src
# export PYTHONPATH=src:$PYTHONPATH
ENV PYTHONPATH "src:${PYTHONPATH}"

EXPOSE 80
CMD ["sh","-c","python /src/run.py"]