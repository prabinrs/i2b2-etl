
# Copyright 2023 Massachusetts General Hospital.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    apt-utils \
    vim \
    postgresql-client \
    unixodbc-dev \
    freetds-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
RUN python3 -m venv .venv

COPY requirements.txt requirements.txt
RUN .venv/bin/pip install --upgrade pip setuptools Cython && \
    .venv/bin/pip install -r requirements.txt && \
    .venv/bin/pip install -U imbalanced-learn mlflow xgboost scikit-learn pandas && \
    .venv/bin/pip uninstall --yes scikit-learn && \
    .venv/bin/pip install scikit-learn==1.3.2

COPY . .

CMD ["/bin/bash"]