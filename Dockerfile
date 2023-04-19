FROM python:3.9-alpine
WORKDIR /app
COPY ./ ./
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["python", "vk_scam_searcher.py"]