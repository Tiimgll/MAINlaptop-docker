FROM python:3.12

WORKDIR /app

RUN apt-get update
RUN apt-get install -y libgl1

RUN pip install pip==24.2

COPY requirements_app.txt .

RUN pip install --no-cache-dir -r requirements_app.txt

COPY . .

CMD ["python", "app.py"]