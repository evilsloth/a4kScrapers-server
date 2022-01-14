FROM python

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8091

CMD ["python", "-m", "api.server"]