## The challenge

In AI models we want to find the thoughts and concepts and planning. It should be possible: unlike humans, we have every single byte of "brain activity" available in giant inscrutable tensors. The problem is that we don't understand them. If we could understand them, we could increase the model's virtue to give it a better character, see if it's eval aware (and make it not aware in a game or test), we could turn up honesty to find true values, and many other alignment tools to help us develop good, kind, deeply aligned models. 

Here we have a nice setup. In the famous paper ["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588) they showed that a model translating from X to Y thinks in English. In this setting we know that many of the inner concepts correspond to English, so this gives us a really nice way to read the model's mind and find the parts of their activations that correspond to English words.

Of course we can't cheat and find the English words by looking up English words. We are searching for a calculation that precisely isolates the activation subspace that corresponds to English words, but not to other languages. This way any winning calculation will generalise to other settings.

We test on translation between Russian, Korean, Arabic, Hindi and Thai. Qwen is trained mostly on English
and Chinese, so we use neither as the input or the output, and count the hidden word if it is
found in English or Chinese.

## Leaderboard

Each row is a transform: one forward pass in, a score for every token out. The model translates between two
languages that share no letters with English or Chinese (Russian, Korean, Arabic, Hindi, Thai). A row
passes a prompt if its top 8 words include the English word for the meaning, or its Chinese translation, and
none of the 8 is from the input or output language or is the word the model is about to say.

