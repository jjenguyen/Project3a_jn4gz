# use an official python runtime as a parent image
FROM python:3.12-slim

# set working directory in the container
WORKDIR /app

# copy the current directory contents into the container at /app
COPY . /app

# copy requirements file
COPY requirements.txt .

# upgrade pip
RUN pip install --upgrade pip

# install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# make port 5000 available
EXPOSE 5000

# run app.py when the container launches
CMD ["python", "app.py"]