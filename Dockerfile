# The Hivemind HTTP front (scripts/hivemind_api.py): standard library only, so the image needs no package index.
# Data (the ledger, the items database, the index, the archive) and the credentials file are mounted at run time,
# never copied into the image. The MCP front's image is Dockerfile.mcp (it adds the mcp package from local wheels).
FROM python:3.12-slim
WORKDIR /app
COPY src/ /app/src/
COPY scripts/hivemind_api.py scripts/hivemind_mcp.py /app/scripts/
COPY poc/universe.json /app/poc/universe.json
COPY poc/config/ /app/poc/config/
ENV PYTHONUNBUFFERED=1
EXPOSE 8788
CMD ["python3", "scripts/hivemind_api.py", "--host", "0.0.0.0", "--port", "8788"]
