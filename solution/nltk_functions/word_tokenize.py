import re

class Word_Tokenize:

	_re_word_start    = r"[^\(\"\`{\[:;&\#\*@\)}\]\-,]"
	"""Excludes some characters from starting word tokens"""

	_re_non_word_chars = r"(?:[?!)\";}\]\*:@\'\({\[])"
	"""Characters that cannot appear within words"""

	_re_multi_char_punct = r"(?:\-{2,}|\.{2,}|(?:\.\s){2,}\.)"
	"""Hyphen and ellipsis are multi-character punctuation"""
	
	_word_tokenize_fmt = r'''(
        %(MultiChar)s
        |
        (?=%(WordStart)s)\S+?  # Accept word characters until end is found
        (?= # Sequences marking a word's end
            \s|                                 # White-space
            $|                                  # End-of-string
            %(NonWord)s|%(MultiChar)s|          # Punctuation
            ,(?=$|\s|%(NonWord)s|%(MultiChar)s) # Comma if at end of word
        )
        |
        \S
    )'''
	"""Format of a regular expression to split punctuation from words,
    excluding period."""
	
	def word_tokenize(self, s):
		"""Tokenize a string to split off punctuation other than periods"""
		return self._word_tokenizer_re().findall(s)
		
	def _word_tokenizer_re(self):
			"""Compiles and returns a regular expression for word tokenization"""
			try:
				return self._re_word_tokenizer
			except AttributeError:
				self._re_word_tokenizer = re.compile(
					self._word_tokenize_fmt %
					{
						'NonWord':   self._re_non_word_chars,
						'MultiChar': self._re_multi_char_punct,
						'WordStart': self._re_word_start,
					},
					re.UNICODE | re.VERBOSE
				)
				return self._re_word_tokenizer
	