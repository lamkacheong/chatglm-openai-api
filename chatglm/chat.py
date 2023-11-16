#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def init_model_args(model_args = None):
    if model_args is None:
        model_args = {}
    model_args['temperature'] = model_args['temperature'] if model_args.get('temperature') != None else 0.95
    if model_args['temperature'] <= 0:
        model_args['temperature'] = 0.1
    if model_args['temperature'] > 1:
        model_args['temperature'] = 1
    model_args['top_p'] = model_args['top_p'] if model_args.get('top_p') else 0.7
    model_args['max_tokens'] = model_args['max_tokens'] if model_args.get('max_tokens') != None else 512

    return model_args

def do_chat_stream(model, tokenizer, question, history, role, model_args = None):
    model_args = init_model_args(model_args)
    sends = 0
    for response, _ in model.stream_chat(
            tokenizer, question, history, role,
            temperature=model_args['temperature'],
            top_p=model_args['top_p'],
            max_length=max(2048, model_args['max_tokens'])):
        ret = response[sends:]
        # https://github.com/THUDM/ChatGLM-6B/issues/478
        # 修复表情符号的输出问题
        if "\uFFFD" == ret[-1:]:
            continue
        sends = len(response)

        yield ret


def do_chat(model, tokenizer, question, history, role, model_args = None):
    model_args = init_model_args(model_args)
    response, _ = model.chat(
            tokenizer, question, history, role,
            temperature=model_args['temperature'],
            top_p=model_args['top_p'],
            max_length=max(2048, model_args['max_tokens']))
    return response

def do_batch_chat(model, tokenizer, prompts, model_args = None):
    model_args = init_model_args(model_args)
    response = model.chat_batch_no_history(tokenizer,
                                           prompts,
                                           max_length=max(20000, model_args['max_tokens']),
                                           top_p=model_args['top_p'],
                                           temperature=model_args['temperature']
                                           )
    return response
