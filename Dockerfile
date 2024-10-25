FROM python:3.10-slim
WORKDIR QueryForge
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD cd src/backend folder && python -m app.app
