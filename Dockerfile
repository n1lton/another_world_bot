FROM python:3.12.4-bookworm


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

WORKDIR /src/
CMD python3 main.py