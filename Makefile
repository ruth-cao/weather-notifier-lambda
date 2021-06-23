clean:		## delete pycache, build files
	@rm -rf deploy  
	@rm -rf layer 
	@rm -rf __pycache__

## prepares layer.zip archive for AWS Lambda Layer deploy 
lambda-layer-build: clean 
	rm -f layer.zip
	mkdir layer layer/python
	pip3 install -r requirements.txt -t layer/python
	cd layer; zip -9qr layer.zip .
	cp layer/layer.zip .
	rm -rf layer

## prepares deploy.zip archive for AWS Lambda Function deploy 
lambda-function-build: clean 
	rm -f deploy.zip
	mkdir deploy 
	cp -r src deploy/.
	cd deploy; zip -9qr deploy.zip .
	cp deploy/deploy.zip .
	rm -rf deploy

# upload AWS Lambda Layer to S3
deploy-layer:
	aws s3 cp layer.zip s3://${BUCKET}/WeatherNotifierLayer.zip

# upload AWS Lambda code to S3
deploy-code:	
	aws s3 cp deploy.zip s3://${BUCKET}/WeatherNotifierFunction.zip

## create CloudFormation stack with lambda function and role.
create-stack:	
	aws cloudformation create-stack --stack-name LambdaWeatherNotifier --template-body file://cloud.yaml --parameters ParameterKey=BucketName,ParameterValue=${BUCKET} ParameterKey=NotifyAlexURL,ParameterValue=${NotifyAlexURL} ParameterKey=NotifyAlexAccessCode,ParameterValue=${NotifyAlexAccessCode} ParameterKey=TopicArn,ParameterValue=${TopicArn} ParameterKey=WeatherApiKey,ParameterValue=${WeatherApiKey} ParameterKey=Latitude,ParameterValue=${Latitude} ParameterKey=Longtitude,ParameterValue=${Longtitude} ParameterKey=Units,ParameterValue=${Units} ParameterKey=Atmosphere,ParameterValue=${Atmosphere} ParameterKey=Probability,ParameterValue=${Probability} --capabilities CAPABILITY_IAM

## delete existing stack
delete-stack: 
	aws cloudformation delete-stack --stack-name LambdaWeatherNotifier

## update CloudFormation stack with lambda function and role.
update-stack: 	
	aws cloudformation update-stack --stack-name LambdaWeatherNotifier --template-body file://cloud.yaml --parameters ParameterKey=BucketName,ParameterValue=${BUCKET} ParameterKey=NotifyAlexURL,ParameterValue=${NotifyAlexURL} ParameterKey=NotifyAlexAccessCode,ParameterValue=${NotifyAlexAccessCode} ParameterKey=TopicArn,ParameterValue=${TopicArn} ParameterKey=WeatherApiKey,ParameterValue=${WeatherApiKey} ParameterKey=Latitude,ParameterValue=${Latitude} ParameterKey=Longtitude,ParameterValue=${Longtitude} ParameterKey=Units,ParameterValue=${Units} ParameterKey=Atmosphere,ParameterValue=${Atmosphere} ParameterKey=Probability,ParameterValue=${Probability} --capabilities CAPABILITY_IAM

deploy-lambda:
	aws lambda update-function-code --function-name ${FunctionName} --s3-bucket ${BUCKET} --s3-key WeatherNotifierFunction.zip