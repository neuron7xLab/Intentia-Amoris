FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN addgroup --system intentia && adduser --system --ingroup intentia intentia

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e .

COPY seeds ./seeds
COPY docs ./docs
COPY contracts ./contracts

RUN mkdir -p /app/data && chown -R intentia:intentia /app
USER intentia

EXPOSE 8000
CMD ["uvicorn", "intentia_amoris.api:app", "--host", "0.0.0.0", "--port", "8000"]
