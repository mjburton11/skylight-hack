#!/bin/bash

set -e

AWS_PROFILE="skylight-hack"
FUNCTION_NAME=$(AWS_PROFILE=$AWS_PROFILE aws lambda list-functions --query 'Functions[0].FunctionName' --output text)

if [ "$FUNCTION_NAME" == "None" ] || [ -z "$FUNCTION_NAME" ]; then
    echo "Error: No Lambda function found in AWS account"
    echo "Please create a Lambda function first following the README instructions"
    exit 1
fi

echo "Found Lambda function: $FUNCTION_NAME"
echo "Packaging code..."

# Create a temporary directory for packaging
rm -rf package
mkdir -p package

# Copy the Lambda function code
cp skylight_lambda.py package/

# Create deployment package
cd package
zip -r ../lambda-deployment.zip .
cd ..

echo "Deploying to Lambda..."

# Update the Lambda function code
AWS_PROFILE=$AWS_PROFILE aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file fileb://lambda-deployment.zip

echo "Deployment successful!"

# Clean up
rm -rf package lambda-deployment.zip
