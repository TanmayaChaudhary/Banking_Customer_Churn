# step 1- Specify the hopst OS
# This will install a linx OS with Python3
FROM python:3.7

# creating a working directory with the name app
WORKDIR /app

# copy the files of current folder to the app folder inside the contianer
COPY . /app


RUN ls
# install the libraries
RUN apt-get update 
#&& apt-get install -y libgl1
RUN pip install -r requirements.txt

EXPOSE 8000
#ENTRYPOINT ["python"]
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
