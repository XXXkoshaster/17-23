FROM python:3.13.3

COPY requirements.txt .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .env

COPY . .



# RUN flask db migrate
# RUN flask db upgrade
# RUN flask gen_api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5005"]
