"""How the ladder step reaches the model: production's `model.call`, through the spending limit it is given, with the answer's own
text kept as it arrives (DESIGN.md §5.3, checks 4 and 8).

`model.call` parses an answer with `json.loads`, which turns numbers into floats, and raises before it archives anything on an
answer it cannot read. So the transport passed to it is wrapped: the wrapper sends through the limit, which charges the response's
own token counts, and keeps the text of `choices[0].message.content` for the step's exact parse.
"""


def model_caller(model, archive, call_config, setting, limit, purpose='clean-ladder'):
    """A `call_model(system_text, user_text, schema)` for `ladder_step.ladder_for_thesis`. `model` is production's model module,
    `limit` an object whose `send(provider, request)` sends one request under the spending cap."""

    def call_model(system_text, user_text, schema):
        received = {}

        def transport(provider, request):
            response = limit.send(provider, request)
            received['response'] = True
            try:
                received['text'] = response['choices'][0]['message']['content']
            except (KeyError, IndexError, TypeError):
                received['text'] = None
            usage = response.get('usage') if isinstance(response, dict) else None
            received['usage'] = usage if isinstance(usage, dict) else {}
            return response

        request = model.build_request(setting, system_text, user_text, schema, 'clean_ladder', call_config.provider)
        result = {'answer_text': None, 'input_tokens': None, 'output_tokens': None, 'cached': False, 'error': None,
                  'request_sha256': model.request_identity(request)[1]}
        try:
            answer = model.call(archive, call_config, setting, system_text, user_text, schema, 'clean_ladder', purpose, transport=transport)
            result['cached'] = answer.cached
        except model.SchemaError as error:
            result['error'] = f'the answer does not fit the schema: {error}'
        except (ValueError, RecursionError) as error:
            if not received.get('response'):
                raise                                    # no response arrived: not an answer's fault
            result['error'] = f'the answer could not be read: {type(error).__name__}'
        result['answer_text'] = received.get('text')
        result['input_tokens'] = received.get('usage', {}).get('prompt_tokens')
        result['output_tokens'] = received.get('usage', {}).get('completion_tokens')
        return result

    return call_model
