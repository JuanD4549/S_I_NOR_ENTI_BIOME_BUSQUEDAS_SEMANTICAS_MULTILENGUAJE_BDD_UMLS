FROM alvarouya/cudaubuntu:v5

EXPOSE 3000

WORKDIR /app
COPY awesome-align awesome-align
RUN cd awesome-align && \
	pip install -r requirements.txt && \
	pip install Flask && \
    python setup.py install

CMD ["python", "awsAig.py"]
