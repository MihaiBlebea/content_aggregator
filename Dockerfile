FROM python:3

ENV VIRTUAL_ENV=/virtualenv

WORKDIR /app

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

RUN pip3 install -r requirements.txt

VOLUME [ "/app/store" ]

EXPOSE 5000

COPY . .

CMD ["python", "./src/api.py"]