FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the application files
COPY . /app

# install requirements
RUN pip install -r requirements.txt

# Expose port for the Flask app
EXPOSE 7755

# Set environment variable for Flask app
ENV FLASK_APP=./core/server.py

# Reset DB
RUN rm ./core/store.sqlite3

# Apply database migration
RUN flask db upgrade -d ./core/migrations/

# Command to run the application
CMD ["bash", "./run.sh"]
