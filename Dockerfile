# pull official base image
# syntax=docker/dockerfile:1
FROM python:3

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
WORKDIR /app/project-management-service
COPY requirements.txt /app/project-management-service
RUN pip install -r requirements.txt

# copy project
COPY ./ /app/project-management-service