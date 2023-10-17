
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.13
ENV PYTHONUNBUFFERED=1
RUN git clone https://github.com/Paillat-dev/Moderator.git
RUN pip install -r /Moderator/requirements.txt
WORKDIR /Moderator
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /Moderator
USER appuser
CMD ["python", "main.py"]