FROM python:3.11

RUN apt-get update && apt-get install -y \
    redis \
    postgresql \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

ENV PYTHONPATH=/backend

# Copy project files
COPY . .


RUN pip install --upgrade pip && \
    pip install -r requirements.txt


EXPOSE 8000


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]
