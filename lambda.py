from main.LambdaHandler import LambdaHandler


def handler(event, context):
    hdl = LambdaHandler()
    return hdl.handle(event, context)
