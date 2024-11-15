from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk, LLMResult
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, TypeVar, Union
import logging


# LCEL: langchain expression language(langchain表达式语言)
class LCELEventHandler(BaseCallbackHandler):

    def on_chain_error(
        self,
        error: BaseException,
        **kwargs: Any,
    ) -> None:
        # print(f"on_chain_error,kwargs:{kwargs}")
        logging.error(f"on_chain_error, error: {error}, kwargs:{kwargs}",
                      exc_info=True)

    def on_llm_error(
        self,
        error: BaseException,
        **kwargs: Any,
    ) -> None:
        # print(f"on_llm_error,kwargs:{kwargs}")
        logging.error(f"on_llm_error, error: {error}, kwargs:{kwargs}",
                      exc_info=True)
