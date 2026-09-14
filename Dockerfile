# Proposal Builder image: Streamlit builder + combine.py, with LibreOffice for
# table-of-contents page numbers. Build with scripts/package.sh (or `docker build .`).
FROM python:3.13-slim-bookworm

ARG GIT_SHA=unknown
LABEL org.opencontainers.image.title="Verto Wave Proposal Builder" \
      org.opencontainers.image.revision="${GIT_SHA}"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# LibreOffice renders the draft once to read heading page numbers; Carlito is
# metric-compatible with Calibri so the page numbers match Word.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libreoffice-writer-nogui poppler-utils fontconfig \
      fonts-crosextra-carlito fonts-crosextra-caladea fonts-liberation2 \
 && rm -rf /var/lib/apt/lists/*

RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin builder

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
# The image is only produced when the full test suite passes inside it.
RUN python -B -m unittest discover -s tests \
 && rm -rf tests \
 && mkdir -p /data/library \
 && chown builder:builder /data/library

ENV PROPOSAL_LIBRARY_DIR=/data/library \
    PROPOSAL_BUILDER_REVISION=${GIT_SHA}
VOLUME ["/data/library"]
USER builder
EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=4)"

CMD ["streamlit", "run", "apps/proposal_builder.py", \
     "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true", \
     "--browser.gatherUsageStats", "false", "--server.enableXsrfProtection", "true"]
