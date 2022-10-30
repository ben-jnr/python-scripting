# list-ecs-services

## python script to list all ecs services

### setup
Requires python3 
```
pip3 install -r requirements.txt
```

Create an environment file .env and add the following
```
region_name='["us-east-1", "us-east-2"]'
aws_access_key_id="xxxxxxxxxxx"
aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
      
### execution   
Run the program as:   

**python3 list-ecs-services.py**

example:

```
python3 list-ecs-services.py
```

