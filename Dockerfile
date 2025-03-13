ARG SELECT=production_no_tex

########################################
# Base stages
FROM python:3.13-slim as base_no_tex
WORKDIR /workspace
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install poetry \
    && poetry config virtualenvs.create false

FROM base_no_tex as base_tex
RUN apt-get update && apt-get install -y texlive-full && rm -rf /var/lib/apt/lists/*

########################################
# Production stages
FROM base_no_tex as production_no_tex
COPY . /workspace

ENV PATH="/root/.local/bin:$PATH"
RUN poetry install && aider-install

ENTRYPOINT ["/bin/bash"]

FROM base_tex as production_tex
COPY . /workspace

ENV PATH="/root/.local/bin:$PATH"
RUN poetry install && aider-install

ENTRYPOINT ["/bin/bash"]

########################################
# Selected stage: set SELECT to one of: base_no_tex, base_tex, production_no_tex, production_tex
FROM ${SELECT}