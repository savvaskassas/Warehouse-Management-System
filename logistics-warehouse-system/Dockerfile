# Dockerfile
FROM python:3.9-slim

# Ορισμός του working directory
WORKDIR /app

# Αντιγραφή του requirements.txt και εγκατάσταση dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Αντιγραφή του application code
COPY app/ ./app/

# Expose το port που θα τρέχει η Flask εφαρμογή
EXPOSE 5000

# Ορισμός environment variables
ENV FLASK_APP=app.main
ENV FLASK_ENV=production

# Εκτέλεση της εφαρμογής
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]