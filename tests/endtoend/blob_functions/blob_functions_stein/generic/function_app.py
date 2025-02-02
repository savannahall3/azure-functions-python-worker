# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import hashlib
import io
import json
import random
import string

import azure.functions as func

app = func.FunctionApp()


@app.function_name(name="blob_trigger")
@app.generic_trigger(
    arg_name="file",
    type="blobTrigger",
    path="python-worker-tests/test-blob-trigger.txt",
    connection="AzureWebJobsStorage")
@app.generic_output_binding(
    arg_name="$return",
    type="blob",
    path="python-worker-tests/test-blob-triggered.txt",
    connection="AzureWebJobsStorage")
def blob_trigger(file: func.InputStream) -> str:
    return json.dumps({
        'name': file.name,
        'length': file.length,
        'content': file.read().decode('utf-8')
    })


@app.function_name(name="get_blob_as_bytes")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="get_blob_as_bytes")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    connection="AzureWebJobsStorage",
    type="blob",
    data_type="BINARY",
    path="python-worker-tests/test-bytes.txt")
def get_blob_as_bytes(req: func.HttpRequest, file: bytes) -> str:
    assert isinstance(file, bytes)
    return file.decode('utf-8')


@app.function_name(name="get_blob_as_bytes_return_http_response")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="get_blob_as_bytes_return_http_response")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    connection="AzureWebJobsStorage",
    type="blob",
    data_type="BINARY",
    path="python-worker-tests/shmem-test-bytes.txt")
def get_blob_as_bytes_return_http_response(req: func.HttpRequest, file: bytes) \
        -> func.HttpResponse:
    """
    Read a blob (bytes) and respond back (in HTTP response) with the number of
    bytes read and the MD5 digest of the content.
    """
    assert isinstance(file, bytes)

    content_size = len(file)
    content_md5 = hashlib.md5(file).hexdigest()

    response_dict = {
        'content_size': content_size,
        'content_md5': content_md5
    }

    response_body = json.dumps(response_dict, indent=2)

    return func.HttpResponse(
        body=response_body,
        mimetype="application/json",
        status_code=200
    )


@app.function_name(name="get_blob_as_bytes_stream_return_http_response")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="get_blob_as_bytes_stream_return_http_response")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    connection="AzureWebJobsStorage",
    type="blob",
    data_type="BINARY",
    path="python-worker-tests/shmem-test-bytes.txt")
def get_blob_as_bytes_stream_return_http_response(req: func.HttpRequest,
                                                  file: func.InputStream) \
        -> func.HttpResponse:
    """
    Read a blob (as azf.InputStream) and respond back (in HTTP response) with
    the number of bytes read and the MD5 digest of the content.
    """
    file_bytes = file.read()

    content_size = len(file_bytes)
    content_md5 = hashlib.md5(file_bytes).hexdigest()

    response_dict = {
        'content_size': content_size,
        'content_md5': content_md5
    }

    response_body = json.dumps(response_dict, indent=2)

    return func.HttpResponse(
        body=response_body,
        mimetype="application/json",
        status_code=200
    )


@app.function_name(name="get_blob_as_str")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="get_blob_as_str")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    connection="AzureWebJobsStorage",
    type="blob",
    data_type="STRING",
    path="python-worker-tests/test-str.txt")
def get_blob_as_str(req: func.HttpRequest, file: str) -> str:
    assert isinstance(file, str)
    return file


@app.function_name(name="get_blob_as_str_return_http_response")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="get_blob_as_str_return_http_response")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    connection="AzureWebJobsStorage",
    type="blob",
    data_type="STRING",
    path="python-worker-tests/shmem-test-bytes.txt")
def get_blob_as_str_return_http_response(req: func.HttpRequest,
                                         file: str) -> func.HttpResponse:
    """
    Read a blob (string) and respond back (in HTTP response) with the number of
    characters read and the MD5 digest of the utf-8 encoded content.
    """
    assert isinstance(file, str)

    num_chars = len(file)
    content_bytes = file.encode('utf-8')
    content_md5 = hashlib.md5(content_bytes).hexdigest()

    response_dict = {
        'num_chars': num_chars,
        'content_md5': content_md5
    }

    response_body = json.dumps(response_dict, indent=2)

    return func.HttpResponse(
        body=response_body,
        mimetype="application/json",
        status_code=200
    )


@app.function_name(name="get_blob_bytes")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="get_blob_bytes")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    connection="AzureWebJobsStorage",
    type="blob",
    path="python-worker-tests/test-bytes.txt")
def get_blob_bytes(req: func.HttpRequest, file: func.InputStream) -> str:
    return file.read().decode('utf-8')


@app.function_name(name="get_blob_filelike")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="get_blob_filelike")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    connection="AzureWebJobsStorage",
    type="blob",
    path="python-worker-tests/test-filelike.txt")
def get_blob_filelike(req: func.HttpRequest, file: func.InputStream) -> str:
    return file.read().decode('utf-8')


@app.function_name(name="get_blob_return")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="get_blob_return")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    connection="AzureWebJobsStorage",
    type="blob",
    path="python-worker-tests/test-return.txt")
def get_blob_return(req: func.HttpRequest, file: func.InputStream) -> str:
    return file.read().decode('utf-8')


@app.function_name(name="get_blob_str")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="get_blob_str")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    connection="AzureWebJobsStorage",
    type="blob",
    path="python-worker-tests/test-str.txt")
def get_blob_str(req: func.HttpRequest, file: func.InputStream) -> str:
    return file.read().decode('utf-8')


@app.function_name(name="get_blob_triggered")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="get_blob_triggered")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    connection="AzureWebJobsStorage",
    type="blob",
    path="python-worker-tests/test-blob-triggered.txt")
def get_blob_triggered(req: func.HttpRequest, file: func.InputStream) -> str:
    return file.read().decode('utf-8')


@app.function_name(name="put_blob_as_bytes_return_http_response")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="put_blob_as_bytes_return_http_response")
@app.generic_output_binding(
    arg_name="file",
    type="blob",
    data_type="BINARY",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/shmem-test-bytes-out.txt")
def put_blob_as_bytes_return_http_response(req: func.HttpRequest,
                                           file: func.Out[
                                               bytes]) -> func.HttpResponse:
    """
    Write a blob (bytes) and respond back (in HTTP response) with the number of
    bytes written and the MD5 digest of the content.
    The number of bytes to write are specified in the input HTTP request.
    """
    content_size = int(req.params['content_size'])

    # When this is set, then 0x01 byte is repeated content_size number of
    # times to use as input.
    # This is to avoid generating random input for large size which can be
    # slow.
    if 'no_random_input' in req.params:
        content = b'\x01' * content_size
    else:
        content = bytearray(random.getrandbits(8) for _ in range(content_size))
    content_md5 = hashlib.md5(content).hexdigest()

    file.set(content)

    response_dict = {
        'content_size': content_size,
        'content_md5': content_md5
    }

    response_body = json.dumps(response_dict, indent=2)

    return func.HttpResponse(
        body=response_body,
        mimetype="application/json",
        status_code=200
    )


@app.function_name(name="put_blob_as_str_return_http_response")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="put_blob_as_str_return_http_response")
@app.generic_output_binding(
    arg_name="file",
    type="blob",
    data_type="STRING",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/shmem-test-str-out.txt")
def put_blob_as_str_return_http_response(
        req: func.HttpRequest, file: func.Out[str]) -> func.HttpResponse:
    """
    Write a blob (string) and respond back (in HTTP response) with the number of
    characters written and the MD5 digest of the utf-8 encoded content.
    The number of characters to write are specified in the input HTTP request.
    """
    num_chars = int(req.params['num_chars'])

    content = ''.join(random.choices(string.ascii_uppercase + string.digits,
                                     k=num_chars))
    content_bytes = content.encode('utf-8')
    content_size = len(content_bytes)
    content_md5 = hashlib.md5(content_bytes).hexdigest()

    file.set(content)

    response_dict = {
        'num_chars': num_chars,
        'content_size': content_size,
        'content_md5': content_md5
    }

    response_body = json.dumps(response_dict, indent=2)

    return func.HttpResponse(
        body=response_body,
        mimetype="application/json",
        status_code=200
    )


@app.function_name(name="put_blob_bytes")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="put_blob_bytes")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_output_binding(
    arg_name="file",
    type="blob",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/test-bytes.txt")
def put_blob_bytes(req: func.HttpRequest, file: func.Out[bytes]) -> str:
    file.set(req.get_body())
    return 'OK'


@app.function_name(name="put_blob_filelike")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="put_blob_filelike")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_output_binding(
    arg_name="file",
    type="blob",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/test-filelike.txt")
def put_blob_filelike(req: func.HttpRequest,
                      file: func.Out[io.StringIO]) -> str:
    file.set(io.StringIO('filelike'))
    return 'OK'


@app.function_name(name="put_blob_return")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="put_blob_return")
@app.generic_output_binding(
    arg_name="$return",
    type="blob",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/test-return.txt")
def put_blob_return(req: func.HttpRequest) -> str:
    return 'FROM RETURN'


@app.function_name(name="put_blob_str")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="put_blob_str")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_output_binding(
    arg_name="file",
    type="blob",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/test-str.txt")
def put_blob_str(req: func.HttpRequest, file: func.Out[str]) -> str:
    file.set(req.get_body())
    return 'OK'


@app.function_name(name="put_blob_trigger")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_trigger(arg_name="req", type="httpTrigger",
                     route="put_blob_trigger")
@app.generic_output_binding(
    arg_name="file",
    type="blob",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/test-blob-trigger.txt")
def put_blob_trigger(req: func.HttpRequest, file: func.Out[str]) -> str:
    file.set(req.get_body())
    return 'OK'


def _generate_content_and_digest(content_size):
    content = bytearray(random.getrandbits(8) for _ in range(content_size))
    content_md5 = hashlib.md5(content).hexdigest()
    return content, content_md5


@app.function_name(name="put_get_multiple_blobs_as_bytes_return_http_response")
@app.generic_trigger(
    arg_name="req", type="httpTrigger",
    route="put_get_multiple_blobs_as_bytes_return_http_response")
@app.generic_input_binding(
    arg_name="inputfile1",
    connection="AzureWebJobsStorage",
    type="blob",
    data_type="BINARY",
    path="python-worker-tests/shmem-test-bytes-1.txt")
@app.generic_input_binding(
    arg_name="inputfile2",
    connection="AzureWebJobsStorage",
    type="blob",
    data_type="BINARY",
    path="python-worker-tests/shmem-test-bytes-2.txt")
@app.generic_output_binding(
    arg_name="outputfile1",
    connection="AzureWebJobsStorage",
    type="blob",
    data_type="BINARY",
    path="python-worker-tests/shmem-test-bytes-out-1.txt")
@app.generic_output_binding(
    arg_name="outputfile2",
    connection="AzureWebJobsStorage",
    type="blob",
    data_type="BINARY",
    path="python-worker-tests/shmem-test-bytes-out-2.txt")
def put_get_multiple_blobs_as_bytes_return_http_response(
        req: func.HttpRequest,
        inputfile1: bytes,
        inputfile2: bytes,
        outputfile1: func.Out[bytes],
        outputfile2: func.Out[bytes]) -> func.HttpResponse:
    """
    Read two blobs (bytes) and respond back (in HTTP response) with the number
    of bytes read from each blob and the MD5 digest of the content of each.
    Write two blobs (bytes) and respond back (in HTTP response) with the number
    bytes written in each blob and the MD5 digest of the content of each.
    The number of bytes to write are specified in the input HTTP request.
    """
    input_content_size_1 = len(inputfile1)
    input_content_size_2 = len(inputfile2)

    input_content_md5_1 = hashlib.md5(inputfile1).hexdigest()
    input_content_md5_2 = hashlib.md5(inputfile2).hexdigest()

    output_content_size_1 = int(req.params['output_content_size_1'])
    output_content_size_2 = int(req.params['output_content_size_2'])

    output_content_1, output_content_md5_1 = \
        _generate_content_and_digest(output_content_size_1)
    output_content_2, output_content_md5_2 = \
        _generate_content_and_digest(output_content_size_2)

    outputfile1.set(output_content_1)
    outputfile2.set(output_content_2)

    response_dict = {
        'input_content_size_1': input_content_size_1,
        'input_content_size_2': input_content_size_2,
        'input_content_md5_1': input_content_md5_1,
        'input_content_md5_2': input_content_md5_2,
        'output_content_size_1': output_content_size_1,
        'output_content_size_2': output_content_size_2,
        'output_content_md5_1': output_content_md5_1,
        'output_content_md5_2': output_content_md5_2
    }

    response_body = json.dumps(response_dict, indent=2)

    return func.HttpResponse(
        body=response_body,
        mimetype="application/json",
        status_code=200
    )
