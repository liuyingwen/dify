"""Functionality for splitting text."""
from __future__ import annotations

from typing import (
    Any,
    List,
    Optional,
)

from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter, TS, Type, Union, AbstractSet, Literal, Collection

from core.model_runtime.model_providers.__base.tokenizers.gpt2_tokenzier import GPT2Tokenizer

class EnhanceRecursiveCharacterTextSplitter(RecursiveCharacterTextSplitter):
    """
        This class is used to implement from_gpt2_encoder, to prevent using of tiktoken
    """
    @classmethod
    def from_gpt2_encoder(
        cls: Type[TS],
        encoding_name: str = "gpt2",
        model_name: Optional[str] = None,
        allowed_special: Union[Literal["all"], AbstractSet[str]] = set(),
        disallowed_special: Union[Literal["all"], Collection[str]] = "all",
        **kwargs: Any,
    ):
        def _token_encoder(text: str) -> int:
            return GPT2Tokenizer.get_num_tokens(text)

        if issubclass(cls, TokenTextSplitter):
            extra_kwargs = {
                "encoding_name": encoding_name,
                "model_name": model_name,
                "allowed_special": allowed_special,
                "disallowed_special": disallowed_special,
            }
            kwargs = {**kwargs, **extra_kwargs}

        return cls(length_function=_token_encoder, **kwargs)

class FixedRecursiveCharacterTextSplitter(EnhanceRecursiveCharacterTextSplitter):
    def __init__(self, fixed_separator: str = "\n\n", separators: Optional[List[str]] = None, **kwargs: Any):
        """Create a new TextSplitter."""
        super().__init__(**kwargs)
        self._fixed_separator = fixed_separator
        self._separators = separators or ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> List[str]:
        """Split incoming text and return chunks."""
        if self._fixed_separator:
            chunks = text.split(self._fixed_separator)
        else:
            chunks = list(text)

        final_chunks = []
        for chunk in chunks:
            if self._length_function(chunk) > self._chunk_size:
                final_chunks.extend(self.recursive_split_text(chunk))
            else:
                final_chunks.append(chunk)

        return final_chunks

    def recursive_split_text(self, text: str) -> List[str]:
        """Split incoming text and return chunks."""
        final_chunks = []
        # Get appropriate separator to use
        separator = self._separators[-1]
        for _s in self._separators:
            if _s == "":
                separator = _s
                break
            if _s in text:
                separator = _s
                break
        # Now that we have the separator, split the text
        if separator:
            splits = text.split(separator)
        else:
            splits = list(text)
        # Now go merging things, recursively splitting longer texts.
        _good_splits = []
        for s in splits:
            if self._length_function(s) < self._chunk_size:
                _good_splits.append(s)
            else:
                if _good_splits:
                    merged_text = self._merge_splits(_good_splits, separator)
                    final_chunks.extend(merged_text)
                    _good_splits = []
                other_info = self.recursive_split_text(s)
                final_chunks.extend(other_info)
        if _good_splits:
            merged_text = self._merge_splits(_good_splits, separator)
            final_chunks.extend(merged_text)
        return final_chunks