FROM python:3.10.2-slim-bullseye AS base

RUN apt-get update && apt-get install libgomp1 python3-opencv ffmpeg libsnappy-dev -y
RUN pip install --upgrade pip

FROM base AS builder

RUN mkdir /install
WORKDIR /install

COPY pip.conf /root/.config/pip/pip.conf
COPY requirements.txt /requirements.txt

ENV PYTHONUSERBASE=/install
RUN pip install --user -r /requirements.txt


FROM base

WORKDIR /code
ENV HOME /code

COPY *.py ./
COPY --from=builder /install /usr/local

# Set environment
ENV PYTHONPATH $PYTHONPATH:/code

ENTRYPOINT ["python", "main.py"]
