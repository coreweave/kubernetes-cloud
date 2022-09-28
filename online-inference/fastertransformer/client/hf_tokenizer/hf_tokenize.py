# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
from tokenizers import Tokenizer
from typing import List, Union

class HFTokenizer:
    def __init__(self, vocab_file):
        self.tokenizer = Tokenizer.from_file(vocab_file)

    def tokenize(self, text: str):
        return self.tokenizer.encode(text).ids

    def tokenize_batch(self, text_batch: Union[List[str], str]):
        return self.tokenizer.encode_batch(text_batch)

    def detokenize(self, token_ids):
        return self.tokenizer.decode(token_ids)