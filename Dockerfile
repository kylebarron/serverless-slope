FROM lambci/lambda:build-python3.8

WORKDIR /tmp

ENV PYTHONUSERBASE=/var/task

COPY serverless_slope/ serverless_slope/
COPY README.md README.md
COPY setup.py setup.py

# Install dependencies
RUN pip install . --user
RUN rm -rf serverless_slope setup.py
