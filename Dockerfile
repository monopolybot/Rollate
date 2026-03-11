FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# إنشاء مجلد للبيانات ليتم ربطه بالـ Volume
RUN mkdir -p /app/data
CMD ["python", "main.py"]
