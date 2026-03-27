# Manual Alexa Skill Setup (Workaround for Console Issues)

If the Amazon Developer Console is having issues, you can try these alternatives:

## Option 1: Wait and Retry Console Access

The Amazon Developer Console may be experiencing temporary issues. Try these URLs in order:
1. https://developer.amazon.com/alexa/console/ask
2. https://developer.amazon.com/dashboard
3. https://developer.amazon.com/settings/console/registration

Once any of these load, navigate to the Alexa section and create your skill manually.

## Option 2: Contact Amazon Developer Support

If the console continues to have 404 errors:
1. Go to https://developer.amazon.com/support
2. Request help with "Unable to access Alexa Developer Console - getting 404 errors"
3. Ask them to verify your vendor ID is set up

## Option 3: Create Skill Manually in Console (when it works)

Once you can access the console:

### Create the Skill
1. Click "Create Skill"
2. Skill name: **Skylight Points**
3. Default language: **English (US)**
4. Choose model: **Custom**
5. Choose hosting: **Provision your own** (you have Lambda)
6. Click "Create skill"

### Configure Interaction Model
1. Click "JSON Editor" in left navigation
2. Paste contents from: `skill-package/interactionModels/custom/en-US.json`
3. Click "Save Model"
4. Click "Build Model"

### Configure Endpoint
1. Click "Endpoint" in left navigation
2. Select "AWS Lambda ARN"
3. Default Region: `arn:aws:lambda:us-east-1:582381606547:function:skylight-points`
4. Click "Save Endpoints"

### Enable Lambda Trigger
Run this command to allow Alexa to invoke your Lambda:

```bash
AWS_PROFILE=skylight-hack aws lambda add-permission \
  --function-name skylight-points \
  --statement-id alexa-skills-kit \
  --action lambda:InvokeFunction \
  --principal alexa-appkit.amazonaws.com \
  --event-source-token <YOUR_SKILL_ID_FROM_CONSOLE>
```

Replace `<YOUR_SKILL_ID_FROM_CONSOLE>` with the skill ID shown in the console (starts with `amzn1.ask.skill.`).

### Test the Skill
1. Click "Test" tab
2. Enable testing for "Development"
3. Type or say: "ask skylight points to give lily 3 points"

## Current Status

- ✅ Lambda function deployed: `skylight-points`
- ✅ Lambda code updated with `skylight_lambda.py`
- ✅ Deployment script created: `./deploy.sh`
- ❌ Alexa skill creation blocked by missing Vendor ID
- ❌ Amazon Developer Console returning 404 errors

## Files Created for ASK CLI (when console works)

- `ask-resources.json` - ASK CLI configuration
- `skill-package/skill.json` - Skill manifest with Lambda ARN
- `skill-package/interactionModels/custom/en-US.json` - Voice interaction model
- `deploy.sh` - Lambda deployment script

Once the console is accessible and you create the skill, you can use `ask deploy` to update it via CLI.
