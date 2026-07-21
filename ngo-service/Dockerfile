FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt \
 && PIP_USER=1 PATH=/root/.local/bin:$PATH opentelemetry-bootstrap -a install

FROM python:3.11-slim
WORKDIR /app
ENV PYTHONPATH=/app
ENV PATH=/root/.local/bin:$PATH
COPY --from=builder /root/.local /root/.local
COPY . .
EXPOSE 8005
# Auto-instrumentacao OpenTelemetry (traces -> OTel Collector -> New Relic)
CMD ["opentelemetry-instrument", "python", "app.py"]
