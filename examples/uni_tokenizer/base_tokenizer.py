import logging
logger = logging.getLogger(__name__)
import os
from flagai.model.file_utils import _get_model_files
from flagai.data.tokenizer.glm_large_ch.glm_large_ch import get_encoder
from bak_wp_tokenizer import WordpieceTokenizer
from bpe_tokenizer import BPETokenizer
from flagai.data.tokenizer.glm_large_ch import glm_large_ch
class BaseTokenizer(object):
    @classmethod
    def from_pretrained(cls,
                        pretrained_model_name_or_path,
                        cache_dir=None, *inputs,
                        **kwargs):
        """
        Instantiate a PreTrainedBertModel from a pre-trained model file.
        Download and cache the pre-trained model file if needed.
        """
        vocab_file = 'vocab.txt'
        merges_file = 'merges.txt'
        sp_file = 'spm.model'
        if cache_dir is None:
            cache_dir = os.path.join(os.path.dirname(__file__), 'vocabs')

        tokenizer_class = ""
        # search the cache directory for certain files

        if os.path.exists(cache_dir):
            files = os.listdir(cache_dir)
            if "vocab.txt" in files:
                if "merges.txt" in files:
                    tokenizer_class = "bpe"
                else:
                    tokenizer_class = "wp"
            elif "spm.models" in files:
                tokenizer_class = "sp"
        if tokenizer_class == "":
            files = _get_model_files(pretrained_model_name_or_path)
            if "vocab.txt" in files:
                if "merges.txt" in files:
                    tokenizer_class = "bpe"
                else:
                    tokenizer_class = "wp"
            elif "spm.models" in files:
                tokenizer_class = "sp"
            else:
                raise FileNotFoundError("no tokenizer files")
        resolved_vocab_file = os.path.join(cache_dir, vocab_file)
        resolved_merges_file = os.path.join(cache_dir, merges_file)
        resolved_sp_file = os.path.join(cache_dir, sp_file)
        if tokenizer_class == "wp":
            return WordpieceTokenizer(vocab_file=resolved_vocab_file)
        elif tokenizer_class == "bpe":
            return BPETokenizer(vocab_file=resolved_vocab_file, merges_file=resolved_merges_file, *inputs, **kwargs)
        elif tokenizer_class == "sp":
            return glm_large_ch.from_pretrained(resolved_sp_file)

    def __init__(self,
                 tokenizer_model_type='GLM-large-en',
                 cache_dir=None,
                 add_block_symbols=True,
                 add_sentinel_token=0,
                 add_task_mask=True,
                 add_decoder_mask=False,
                 **kwargs):
        self.tokenizer_model_type = 'GLM-large-en'
        self.max_len = int(1e12)

if __name__ == '__main__':
    tokenizer = BaseTokenizer.from_pretrained('GLM-large-en')
    print(tokenizer.convert_tokens_to_ids(tokenizer.tokenize("fried chicken makes me happy")))