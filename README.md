# City of Haverhill QAlert Data Pipeline

[![ci Actions Status](https://github.com/CityOfHaverhill/qalert/workflows/ci/badge.svg)](https://github.com/CityOfHaverhill/qalert/actions) [![cd Actions Status](https://github.com/CityOfHaverhill/qalert/workflows/cd/badge.svg)](https://github.com/CityOfHaverhill/qalert/actions)

This project contains source code and supporting files for a serverless application built for the City of Haverhill.
The serverless application connects to QAlert a CRM tool for citizens requests and copies data into a GIS enabled PostgreSQL instance. This project is developed and deployed using the SAM tool -- AWS's own **S**erverless **A**pplication **M**odel framework.

## Project Structure
- haverhill_311_function - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit and Integration tests for the application code. 
- template.yaml - A template that defines the application's AWS resources (SAM/CloudFormation).
- alembic - Database migration files
- mock_qalert - A mock QAlert API (built with Flask) meant to replicate the behavior of the real QAlert API for testing purposes.
- .github - CI/CD pipeline definitions
- Makefile - used for automating tasks when working in this project

## Getting started
1. Install project dependencies:
    - `git`
    - `sam` - follow instruction for your operating system: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html
    - `docker` - follow instructions for your operating system https://docs.docker.com/engine/install/. Version must be 19.03.0+
    - `docker-compose` - this is usually installed together with `docker` but if not, you need to install this as well.
    - `python 3.6`
    - `virtualenv` - follow instructions: https://virtualenv.pypa.io/en/latest/installation.html. **Make sure to install it under python3.6 so that virtual environment created will also be under 3.6**
    - `psql` - command line tool to connect to postgres: https://blog.timescale.com/tutorials/how-to-install-psql-on-mac-ubuntu-debian-windows/
2. Clone the repository
    ```bash
    $ git clone https://github.com/CityOfHaverhill/qalert.git
    ```
3. Create python virtual environment
    ```bash
    # create the environment in the project root
    virtualenv haverhill_qalert_venv
    # activate it in the project root
    source haverhill_qalert_venv/bin/activate
    ```
4. Install python dependencies

    Ensure your virtual environment was activated before this step
    ```bash
    # from root of project
    pip install -r requirements.txt
    ```
5. Start docker

## Running tests
Tests are defined in the `tests` folder in this project.
### Unit tests

```bash
$ make unit-tests
```
### Integration tests

```bash
$ make integration-tests
```

## Run the function locally
Ensure docker daemon is running.

Run the application in a single command:
```bash
$ make run-function
```

This will startup all the dependent services for the function locally in a dockerized form orchestrated with docker-compose. The dependent services include:
- PostgreSQL
- Mock QAlert API

And will then build the serverless function using SAM and run it within a special Lambda container which replicates the production environment.

After running the function, a nice way to validate that it worked is to display the QAlert requests which were copied into the Postgres instance on a map interface. We built a simple utility to do just that in the form of a python notebook. See instruction in the `utils/visualize_db` directory on how to run it.

## Notes on AWS and SAM
The application uses several AWS resources, including Lambda functions and an RDS. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS Toolkit.  
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS. The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code. See the following links to get started.

* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
## Deploy the haverhill 311 lambda function

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
haverhill-311$ sam logs -n PipelineFunction --stack-name haverhill-311-stack --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).