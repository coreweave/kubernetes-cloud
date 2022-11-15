import json
import torch
import time
import google.protobuf.json_format
import multiprocessing as mp
import numpy as np
import tritonclient.grpc as grpcclient
import tritonclient.http as httpclient

from tritonclient.grpc.service_pb2 import ModelInferResponse
from functools import partial
from argparse import ArgumentParser
from collections.abc import Mapping
from tritonclient.utils import np_to_triton_dtype

import os
import sys

# GPT_BPE Tokenizer
import gpt_bpe.gpt_token_encoder as encoder

merge_file = "/workspace/gpt_bpe/gpt2-merges.txt"
vocab_file = "/workspace/gpt_bpe/gpt2-vocab.json"

enc = encoder.get_encoder(vocab_file, merge_file)

def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source

def encode_data(text="Hello, I am Jane. Nice to meet you!"):
    all_ids = [torch.IntTensor(enc.encode(text))]
    return all_ids[0].numpy()


def decode_data(array):
    sentence = enc.decode(array)
    return sentence

def generate_parameters(args):
    DEFAULT_CONFIG = {
        'protocol': args.protocol,
        'url': f'{args.url}:80',
        'model_name': 'fastertransformer',
        'verbose': False,
    }

    params = {'config': DEFAULT_CONFIG}

    with open('/workspace/sample_request.json') as f:
        file_params = json.load(f)

    deep_update(params, file_params)

    input_lengths = len(encode_data(text=args.prompt))

    for index, value in enumerate(params['request']):
        if value['name'] == 'input_ids':
            value['data'] = [encode_data(text=args.prompt)] 
        if value['name'] == 'input_lengths':
            value['data'] = [[input_lengths]]
        params['request'][index] = {
            'name': value['name'],
            'data': np.array(value['data'], dtype=value['dtype']),
        }
    
    return params['config'], params['request']


def prepare_tensor(client, name, input):
    t = client.InferInput(name, input.shape, np_to_triton_dtype(input.dtype))
    t.set_data_from_numpy(input)
    return t

def stream_consumer(queue):
    print(f"queue: {queue}")
    start_time = None
    while True:
        result = queue.get()
        if result is None:
            break

        if isinstance(result, float):
            start_time = result
            continue

        message = ModelInferResponse()
        google.protobuf.json_format.Parse(json.dumps(result), message)
        result = grpcclient.InferResult(message)

        print(f"result GRPC : {result}")
        idx = result.as_numpy("sequence_length")[0, 0]
        tokens = result.as_numpy("output_ids")[0, 0, :idx]
        prob = result.as_numpy("cum_log_probs")[0, 0]
        print("[After {:.2f}s] Partial result (probability {:.2e}):\n{}\n".format(
            time.perf_counter() - start_time, np.exp(prob), tokens))

        for output in result.get_response().outputs:
            if output.name == "output_ids":
                print(f"Ouput: {decode_data(list(result.as_numpy(output.name)[0][0]))}")

def stream_callback(queue, result, error):
    if error:
        queue.put(error)
    else:
        queue.put(result.get_response(as_json=True))


def main_grpc(config, request):
    result_queue = mp.Queue()

    consumer = mp.Process(target=stream_consumer, args=(result_queue,))
    consumer.start()

    with grpcclient.InferenceServerClient(config['url'], verbose=config["verbose"]) as cl:
        payload = [prepare_tensor(grpcclient, field['name'], field['data'])
            for field in request]
        
        print(f"payload : {payload}")
        cl.start_stream(callback=partial(stream_callback, result_queue))
        result_queue.put(time.perf_counter())
        cl.async_stream_infer(config['model_name'], payload)
    result_queue.put(None)
    consumer.join()

def main_http(config, request):
    client_type = httpclient if config['protocol'] == 'http' else grpcclient
    with client_type.InferenceServerClient(config['url'], verbose=config['verbose']) as cl:
        payload = [prepare_tensor(client_type, field['name'], field['data'])
            for field in request]

        result = cl.infer(config['model_name'], payload)

    for output in result.get_response()['outputs']:
        if output['name'] == "output_ids":
            print(f"Ouput: {decode_data(list(result.as_numpy(output['name'])[0][0]))}")

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--url", help="InferenceService URL for Fastertransfomer", required=True)
    parser.add_argument("--prompt", help="Prompt to generate based of.", required=True)
    parser.add_argument("--protocol", help="Prompt to generate based of.", required=True)
    
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()
    config, request = generate_parameters(args)
    if args.protocol == "http":
        main_http(config, request)
    elif args.protocol == "grpc":
        main_grpc(config, request)