import os
import re
import json
import textwrap
import os.path as osp
from typing import Union


class NotebookUtil():



    def t5_generate(prompt, tokenizer, base_model):
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
        t5_output = base_model.generate(input_ids, max_length=612)
        return tokenizer.decode(t5_output[0], skip_special_tokens=True)


    def wrap_text_preserve_newlines(text, width=110):
        # Split the input text into lines based on newline characters
        lines = text.split('\n')

        # Wrap each line individually
        wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

        # Join the wrapped lines back together using newline characters
        wrapped_text = '\n'.join(wrapped_lines)
        return wrapped_text


    def load_raw_data_text():
        raw_text = ''
        try:
            f = open('../dataset/raw.text')
            raw_text = f.read()
        except:
            raw_text = ''

        text_cases = re.split("\n---\n", raw_text, 0, re.MULTILINE)

        print(json.dumps(text_cases, indent=4))
        return text_cases


    def load_dataset(dataset_name):
        dataset_path = osp.join('../dataset/', f"{dataset_name}.json")

        try:
            fp = open(dataset_path)
            dataset = json.load(fp)
        except:
            dataset = []

        return dataset


    def save_dataset(dataset_path, dataset):
        with open(dataset_path, 'w') as fp:
            json.dump(dataset, fp, ensure_ascii=False, indent=2)


    def extract_response(text: str, model_type='alpaca'):
        if model_type == 'alpaca':
            splitted = text.split('### Response:\n')
            return splitted[1].strip()

        print('TODO: adds support for t5-flan')


    def fix_encoding_output(text: str):
        start_encode_pattern = r"\<ol start=\"(\d)\"\>\<li\>"
        end_encode_pattern = r"\<\/li\>\<\/ol\>"

        text = re.sub(start_encode_pattern, r"\1.   ", text)
        text = re.sub(end_encode_pattern, "", text)

        return text


    def response_to_array(text: str):
        splitter_pattern = r"^\d.\s{3}"
        responses_cleand = re.split(splitter_pattern, text, 0, re.MULTILINE);
        return responses_cleand


    def t5_generate(prompt, tokenizer, base_model):
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
        t5_output = base_model.generate(input_ids, max_length=612)
        return tokenizer.decode(t5_output[0], skip_special_tokens=True)





class Prompter(object):
    __slots__ = ("template", "_verbose")

    def __init__(self, template_name: str = "", verbose: bool = False, runner: str = 'google-colab'):
        self._verbose = verbose

        base_path = '../templates/'
        if runner == 'google-colab':
            base_path = '/content/'


        if not template_name:
            # Enforce the default here, so the constructor can be called with '' and will not break.
            template_name = "alpaca"
        file_name = osp.join(base_path, f"{template_name}.json")
        if not osp.exists(file_name):
            raise ValueError(f"Can't read {file_name}")
        with open(file_name) as fp:
            self.template = json.load(fp)
        if self._verbose:
            print(
                f"Using prompt template {template_name}: {self.template['description']}"
            )

    def generate_prompt(
        self,
        instruction: str,
        input: Union[None, str] = None,
        label: Union[None, str] = None,
    ) -> str:
        # returns the full prompt from instruction and optional input
        # if a label (=response, =output) is provided, it's also appended.
        if input:
            res = self.template["prompt_input"].format(
                instruction=instruction, input=input
            )
        else:
            res = self.template["prompt_no_input"].format(
                instruction=instruction
            )
        if label:
            res = f"{res}{label}"
        if self._verbose:
            print(res)
        return res

    def get_response(self, output: str) -> str:
        return output.split(self.template["response_split"])[1].strip()