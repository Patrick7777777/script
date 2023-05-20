import logging
import math
import textwrap

import numpy as np
# import triton_python_backend_utils as pb_utils
import ujson


class TritonPythonModel:
    number_of_words_in_phrase: int
    number_of_lines_in_phrase: int
    number_of_chars_in_line: int
    number_of_seconds_max_of_phrase: float
    number_of_seconds_min_of_phrase: float
    gap_in_seconds_between_phrases: float
    enhance_text: bool

    def initialize(self, args):
        self.model_config = model_config = ujson.loads(args['model_config'])
        out0_config = pb_utils.get_output_config_by_name(model_config, 'json__0')
        self.out0_dtype = pb_utils.triton_string_to_numpy(out0_config['data_type'])
        self.number_of_words_in_phrase = int(self.get_config_parameter_by_key(model_config, 'number_of_words_in_phrase'))
        self.number_of_lines_in_phrase = int(self.get_config_parameter_by_key(model_config, 'number_of_lines_in_phrase'))
        self.number_of_chars_in_line = int(self.get_config_parameter_by_key(model_config, 'number_of_chars_in_line'))
        self.number_of_seconds_max_of_phrase = float(self.get_config_parameter_by_key(model_config, 'number_of_seconds_max_of_phrase'))
        self.number_of_seconds_min_of_phrase = float(self.get_config_parameter_by_key(model_config, 'number_of_seconds_min_of_phrase'))
        self.gap_in_seconds_between_phrases = float(self.get_config_parameter_by_key(model_config, 'gap_in_seconds_between_phrases'))
        self.enhance_text = bool(int(self.get_config_parameter_by_key(model_config, 'enhance_text')))
        assert self.number_of_words_in_phrase > 0
        assert self.number_of_lines_in_phrase > 0
        assert self.number_of_chars_in_line > 0
        assert self.number_of_seconds_max_of_phrase > 0
        assert self.number_of_seconds_min_of_phrase > 0
        assert self.gap_in_seconds_between_phrases > 0
        assert self.number_of_seconds_max_of_phrase > \
               self.number_of_seconds_min_of_phrase >= \
               self.gap_in_seconds_between_phrases

    @staticmethod
    def auto_complete_config(auto_complete_model_config):
        inputs = [{
            'name': 'json__0',
            'data_type': 'TYPE_STRING',
            'dims': [1]
        }]
        outputs = [{
            'name': 'json__0',
            'data_type': 'TYPE_STRING',
            'dims': [1]
        }]

        config = auto_complete_model_config.as_dict()
        input_names = []
        output_names = []
        for i in config['input']:
            input_names.append(i['name'])
        for o in config['output']:
            output_names.append(o['name'])

        for i in inputs:
            if i['name'] not in input_names:
                auto_complete_model_config.add_input(i)
        for o in outputs:
            if o['name'] not in output_names:
                auto_complete_model_config.add_output(o)
        auto_complete_model_config.set_max_batch_size(0)

        return auto_complete_model_config

    @staticmethod
    def get_config_parameter_by_key(model_config, key):
        if 'parameters' in model_config:
            parameters = model_config['parameters']
            if key in parameters:
                parameter = parameters[key]
                return parameter['string_value']
        return None

    @staticmethod
    async def split_phrase_in_text(
        start: float, end: float, text: str, num_words: int, num_lines: int,
        num_chars_in_line: int, num_seconds_max:float, num_seconds_min: float,
        gap_between_sec: float
    ):
        text = ' '.join(text.splitlines())
        words_list = text.split()
        length = end - start
        words_count = len(words_list)

        if length < num_seconds_max and words_count < num_words:
            text = textwrap.fill(
                text,
                width=num_chars_in_line
            )
            yield start, end, text
            return

        ratio = max(
            1.0,
            length / num_seconds_max
        )

        if not int(math.ceil(ratio)):
            chunk_size = 0
        else:
            chunk_size = int(max(0, round(words_count / ratio)))

        text_lines = textwrap.fill(
            text,
            width=num_chars_in_line
        ).splitlines()
        if len(text_lines) > num_lines:
            words_in_lines = ' '.join(text_lines[0:num_lines]).split()
            chunk_size = min(chunk_size, len(words_in_lines))

        if not chunk_size:
            text = textwrap.fill(
                text,
                width=num_chars_in_line
            )
            if num_seconds_min <= length <= num_seconds_max:
                yield start, end, text
            elif length < num_seconds_min:
                yield start, start + num_seconds_min, text
            else:
                yield start, end, text
            return

        logging.debug(
            f'Splitting phrase to chunks... '
            f'words count: {int(words_count)}, '
            f'chunk_size: {int(chunk_size)}, '
            f'length: {float(length)}, '
            f'ratio: {float(ratio)}, '
            f'start: {float(start)}, '
            f'end: {float(end)}'
        )

        last_end = start
        for i, c in enumerate(range(0, words_count, chunk_size)):
            max_end = ((i + 1) * num_seconds_max)
            p_start = max(start, last_end + (gap_between_sec * i))
            p_end = max(p_start + num_seconds_min, min(end, last_end + max_end))
            assert p_start < p_end, (p_start, p_end)

            p_text = ' '.join(words_list[c:c + chunk_size])
            if num_chars_in_line > 0:
                p_text = textwrap.fill(
                    p_text,
                    width=num_chars_in_line
                )

            yield p_start, p_end, p_text
            last_start = p_start
            last_end = p_end
            assert last_start < last_end, (last_start, last_end)

    @staticmethod
    async def iter_transcribed(transcribed: list, num_words: int):
        for r in transcribed:
            chunked_list = []
            curr_voice = None
            curr_word_n = 0
            for i in r.get('result', []):
                if (
                    len(chunked_list) > 0 and
                    ((curr_voice and curr_voice != i.get('voice', None)) or
                     curr_word_n >= num_words)
                ):
                    yield (
                        chunked_list[0]['start'],
                        chunked_list[-1]['end'],
                        ' '.join([w['word'] for w in chunked_list]),
                        curr_voice
                    )
                    chunked_list = []
                    curr_word_n = 0

                chunked_list.append(i)
                curr_voice = i.get('voice', None)
                curr_word_n += 1

            if len(chunked_list) > 0:
                yield (
                    chunked_list[0]['start'],
                    chunked_list[-1]['end'],
                    ' '.join([w['word'] for w in chunked_list]),
                    curr_voice
                )

    @staticmethod
    async def enhance_text_punct(text: str, lan_id: str = 'ru'):
        text = np.asarray(text.encode('utf-8')).reshape([1])
        lan_id = np.asarray(lan_id.encode('utf-8')).reshape([1])

        in0 = pb_utils.Tensor(
            'txt__0', text.astype(np.object_)
        )
        in1 = pb_utils.Tensor(
            'lan__1', lan_id.astype(np.object_)
        )
        inference_request = pb_utils.InferenceRequest(
            model_name='punctuation',
            requested_output_names=['txt__0'],
            inputs=[in0, in1]
        )
        infer_resp = await inference_request.async_exec()
        if infer_resp.has_error():
            raise pb_utils.TritonModelException(
                infer_resp.error().message()
            )
        assert len(infer_resp.output_tensors()) > 0

        output1 = pb_utils.get_output_tensor_by_name(infer_resp, 'txt__0')
        return bytes(output1.as_numpy()[0]).decode('utf-8')

    async def normalize(self, transcribed: list):
        num_words = self.number_of_words_in_phrase
        num_lines = self.number_of_lines_in_phrase
        num_chars_in_line = self.number_of_chars_in_line
        num_seconds_max = self.number_of_seconds_max_of_phrase
        num_seconds_min = self.number_of_seconds_min_of_phrase
        gap_between_sec = self.gap_in_seconds_between_phrases
        enhance_text = self.enhance_text

        _l_end = None
        _result = list()
        async for start, end, text, voice in self.iter_transcribed(
            transcribed, num_words
        ):
            if enhance_text:
                text = await self.enhance_text_punct(text)
            if _l_end and _l_end >= start:
                duration = end - start
                start = _l_end + gap_between_sec
                end = start + duration
                assert duration > 0

            async for _start, _end, _text in self.split_phrase_in_text(
                start, end, text, num_words, num_lines, num_chars_in_line,
                num_seconds_max, num_seconds_min, gap_between_sec
            ):
                _result.append({
                    'start': _start,
                    'end': _end,
                    'text': _text,
                    'voice': voice
                })
                _l_end = _end

        return _result

    async def execute(self, requests):
        out0_dtype = self.out0_dtype
        responses = []

        for request in requests:
            in_0 = pb_utils.get_input_tensor_by_name(request, 'json__0')
            in_0 = bytes(in_0.as_numpy()[0]).decode('utf-8')
            in_0 = ujson.loads(in_0)
            normalized = await self.normalize(in_0)
            normalized = ujson.dumps(normalized, ensure_ascii=True)
            normalized = np.asarray(normalized.encode('utf-8')).reshape([1])
            out_0 = pb_utils.Tensor('json__0', normalized.astype(out0_dtype))
            inference_response = pb_utils.InferenceResponse(output_tensors=[out_0])
            responses.append(inference_response)

        return responses
