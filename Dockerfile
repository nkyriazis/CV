ARG SELECT=production

########################################
# Development stage
FROM python:3.13-slim as base

# Set the working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    git \
    texlive-full \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Disable virtual environments in Poetry
RUN poetry config virtualenvs.create false

########################################
# Production stage
FROM base as production

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock* /workspace/


# Install dependencies
RUN poetry install

# Copy the rest of the application code
COPY . /workspace

# Set the entrypoint to bash
ENTRYPOINT ["/bin/bash"]

########################################
# Selected stage
FROM ${SELECT}